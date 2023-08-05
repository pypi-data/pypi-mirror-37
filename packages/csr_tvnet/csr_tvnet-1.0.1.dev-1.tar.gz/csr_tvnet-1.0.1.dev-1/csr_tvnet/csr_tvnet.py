#!/usr/bin/env python
import time
import random
import logging
import ipaddress
from shutil import copyfile
import os
import re
import binascii

from configs import *
from csr_cloud.csr_cloud import csr_cloud as cloud
from base_csr_tvnet import base_csr_transit
try:
    import cli
    guestshell = True
    CONTAINER = False
except IOError:
    guestshell = False
    CONTAINER = False
except ImportError:
    try:
        from netmiko import ConnectHandler
        CONTAINER = True
        guestshell = False
    except ImportError:
        guestshell = False
        CONTAINER = False

feature = "tvnet"
log = logging.getLogger(feature)
tvnet_home = '/home/guestshell/' + feature

class csr_transit(base_csr_transit):
    def __init__(self, customDataFileName,
                 configure_pubkey=False,
                 username_pubkey='automate',
                 private_storage_account= None,
                 private_storage_key=None): # pragma: no cover
        base_csr_transit.__init__(self, customDataFileName)

        if not self.parse_decoded_custom_data():
            raise IOError("Failed to parse Custom Data File")

        try:
            self.section_dict['cloudname']
        except:
            self.section_dict['cloudname'] = 'azure'

        self.cloud = cloud(
            feature,
            self.section_dict['strgacctname'],
            self.section_dict['strgacckey'],
            cloudname=self.section_dict['cloudname'])

        if private_storage_account and private_storage_key:
            self.section_dict['privatestrgacctname'] = private_storage_account
            self.section_dict['privatestrgacckey'] = private_storage_key

        self.section_dict['configure_pubkey'] = configure_pubkey
        self.section_dict['username_pubkey'] = username_pubkey
        self.setup_file_dict()
        status = self.get_all_files()
        if not status:
            log.exception("""[ERROR] Failed to retrieve files from Storage account. 
            Please check Storage Account name, Storage Key and Transit VNET Name""")
            self.cmd_execute(
                "send log [ERROR] [CSRTransitVNET] Failed to retrieve files")
            self.cmd_execute(
            "send log [ERROR] [CSRTransitVNET] Please check Storage Account name, Storage Key and Transit VNET Name")
            raise Exception("Incorrect Storage name or Transit VNET Name")
        self.setup_default_dict()

    def cmd_execute(self, command):
        '''
        Note: for some reason initial pull/show always results in broken or non existent result.
        Hence execute show commands TWICE always.
        '''
        if guestshell:
            output = cli.execute(command)
        else:
            output = command
        # output = commands
        log.info(output)
        return output

    def cmd_configure(self, config):
        log.info(config)
        if guestshell:
            output = cli.configure(config)
        else:
            output = config
        log.info(output)
        return output

    def configure_tunnel(self, tunn_addr):
        cmd = ''
        onprem_tunnel_config = None
        role = self.section_dict['role'].lower()

        if 'hub' in role:
            if 'eigrp' in self.section_dict['dmvpn']["RoutingProtocol"].lower(
            ):
                cmd = hub_tunnel_config_eigrp
                cmd = cmd.format(
                    TunnelId=self.section_dict['dmvpn']["TunnelID"],
                    TunnelIP=str(tunn_addr),
                    RoutingProtocolASN=str(
                        self.section_dict['dmvpn']["RoutingProtocolASN"]),
                    DMVPNTunnelIpMask=str(
                        self.section_dict['dmvpn']["DMVPNTunnelIpMask"]),
                    AuthString=self.section_dict['dmvpn']["NHRPAuthString"],
                    NHRPNetworkId=str(
                        self.section_dict['dmvpn']["NHRPNetworkId"]),
                    TunnelKey=str(
                        self.section_dict['dmvpn']["TunnelKey"]),
                    ConnName=self.section_dict['dmvpn']["ConnectionName"])
            elif 'bgp' in self.section_dict['dmvpn']["RoutingProtocol"].lower():
                cmd = hub_tunnel_config_bgp
                cmd = cmd.format(
                    TunnelId=self.section_dict['dmvpn']["TunnelID"],
                    TunnelIP=str(tunn_addr),
                    DMVPNTunnelIpMask=str(
                        self.section_dict['dmvpn']["DMVPNTunnelIpMask"]),
                    AuthString=self.section_dict['dmvpn']["NHRPAuthString"],
                    NHRPNetworkId=str(
                        self.section_dict['dmvpn']["NHRPNetworkId"]),
                    TunnelKey=str(
                        self.section_dict['dmvpn']["TunnelKey"]),
                    ConnName=self.section_dict['dmvpn']["ConnectionName"])

            #####
            # Here the on premise tunnel config is put in.
            #####
            if self.section_dict['onpremoption'] == 'true':
                nbma_onprem_list = [['onpremTunnelIp1', 'onpremPublicIp1'], ['onpremTunnelIp2', 'onpremPublicIp2']]
                onprem_nbma_config = ''
                for nbma in nbma_onprem_list:
                    try:
                        onprem_nbma_config += self.get_tunnel_nhsnbma_config_base(
                            self.section_dict['onprem'][nbma[0]],
                            self.section_dict['onprem'][nbma[1]])
                    except:
                        log.info(
                            '[INFO] [Transit VNET] OnPremise NBMA config {},{} not found'.format(nbma[0], nbma[1]))
                onprem_tunnel_config = spoke_tunnel_config_general.format(
                    TunnelId=self.section_dict['onprem']["onpremTunnelID"],
                    TunnelIP= str(
                        self.section_dict['onprem']["onprem_tunnel_ip"]),
                    DMVPNTunnelIpMask=str(
                        self.section_dict['onprem']["onpremTunnelMask"]),
                    AuthString=self.section_dict['onprem']["onpremNHRPAuthString"],
                    nbmaconfig=onprem_nbma_config,
                    NHRPNetworkId=str(
                        self.section_dict['onprem']["onpremNHRPNetworkId"]),
                    TunnelKey=str(
                        self.section_dict['onprem']["onpremTunnelKey"]),
                    ConnName=self.section_dict['onprem']["onpremConnectionName"])

        else:
            nbmaconfig = ''
            for key, value in self.section_dict.items():
                if 'hub-' in key:
                    if nbmaconfig != '':
                        nbmaconfig += '\n'
                    nbmaconfig += self.get_tunnel_nhsnbma_config_base(value['nbma'], value['pip'])
            cmd = spoke_tunnel_config_general
            cmd = cmd.format(
                TunnelId=self.section_dict['dmvpn']["TunnelID"],
                TunnelIP=str(tunn_addr),
                DMVPNTunnelIpMask=str(
                    self.section_dict['dmvpn']["DMVPNTunnelIpMask"]),
                AuthString=self.section_dict['dmvpn']["NHRPAuthString"],
                nbmaconfig=nbmaconfig,
                NHRPNetworkId=str(
                    self.section_dict['dmvpn']["NHRPNetworkId"]),
                TunnelKey=str(
                    self.section_dict['dmvpn']["TunnelKey"]),
                ConnName=self.section_dict['dmvpn']["ConnectionName"])
        output = self.cmd_configure(cmd)
        log.info(output)
        self.cmd_execute(
            "send log [INFO] [CSRTransitVNET] Configured {} tunnel ".format(role))
        if onprem_tunnel_config:
            onpremoutput = self.cmd_configure(onprem_tunnel_config)
            log.info(onpremoutput)
            self.cmd_execute(
                "send log [INFO] [CSRTransitVNET] Configured Onpremise tunnel ")
        return output

    def get_tunnel_nhsnbma_config_base(self, DMVPNHubTunnelIp, DMVPNHubIp):
        cmd = spoke_tunnel_nhsnbma_config_base
        cmd = cmd.format(
            DMVPNHubTunnelIp=str(DMVPNHubTunnelIp),
            DMVPNHubIp=DMVPNHubIp)
        return cmd

    def configure_tunnel_nhsnbma(self, DMVPNHubTunnelIp, DMVPNHubIp):
        cmd = spoke_tunnel_nhsnbma_config
        cmd = cmd.format(
            TunnelId=self.section_dict['dmvpn']["TunnelID"],
            DMVPNHubTunnelIp=str(DMVPNHubTunnelIp),
            DMVPNHubIp=DMVPNHubIp)
        output = self.cmd_configure(cmd)
        log.info(output)
        self.cmd_execute(
            "send log [INFO] [CSRTransitVNET] Configured tunnel's NBMA and \
            connected to Hub at {} IP ".format(DMVPNHubIp))
        return output

    def configure_routing(self, tunn_addr):

        role = self.section_dict['role'].lower()

        if 'eigrp' in self.section_dict['dmvpn']["RoutingProtocol"].lower():
            if 'hub' in role:
                cmd = routing_eigrp_vrf
                cmd = cmd.format(
                    RoutingProtocolASN=str(
                        self.section_dict['dmvpn']["RoutingProtocolASN"]),
                    ConnName=self.section_dict['dmvpn']["ConnectionName"],
                    DMVPNTunnelIpNetworkNum=str(
                        self.section_dict['dmvpn']["DMVPNTunnelIpNetworkNum"]),
                    DMVPNTunnelIpMask=str(
                        self.section_dict['dmvpn']["DMVPNTunnelIpMask"]),
                    TunnelId=self.section_dict['dmvpn']["TunnelID"],
                    TunnelIP=str(tunn_addr))
            else:
                cmd = routing_eigrp
                cmd = cmd.format(
                    RoutingProtocolASN=str(
                        self.section_dict['dmvpn']["RoutingProtocolASN"]),
                    DMVPNTunnelIpNetworkNum=str(
                        self.section_dict['dmvpn']["DMVPNTunnelIpNetworkNum"]),
                    DMVPNTunnelIpMask=str(
                        self.section_dict['dmvpn']["DMVPNTunnelIpMask"]),
                    TunnelId=self.section_dict['dmvpn']["TunnelID"],
                    TunnelIP=str(tunn_addr))
        elif 'bgp' in self.section_dict['dmvpn']["RoutingProtocol"].lower():
            if 'hub' in role:
                cmd = routing_bgp_vrf
                cmd = cmd.format(
                    RoutingProtocolASN=str(
                        self.section_dict['dmvpn']["RoutingProtocolASN"]),
                    ConnName=self.section_dict['dmvpn']["ConnectionName"],
                    DMVPNTunnelIpNetworkNum=str(
                        self.section_dict['dmvpn']["DMVPNTunnelIpNetworkNum"]),
                    DMVPNTunnelIpPrefixLen=str(
                        self.section_dict['dmvpn']["DMVPNTunnelIpPrefixLen"]),
                    DMVPNTunnelIpMask=str(
                        self.section_dict['dmvpn']["DMVPNTunnelIpMask"]),
                    TunnelId=self.section_dict['dmvpn']["TunnelID"],
                    TunnelIP=str(tunn_addr))
            else:
                # TODO Change the router neighbours
                cmd = routing_bgp
                cmd = cmd.format(
                    RoutingProtocolASN=str(self.section_dict['dmvpn']["RoutingProtocolASN"]),
                    DMVPNTunnelIpNetworkNum=str(
                        self.section_dict['dmvpn']["DMVPNTunnelIpNetworkNum"]),
                    TunnelIP=str(tunn_addr))

        output = self.cmd_configure(cmd)
        log.info("cfg routing output = %s" % output)

        self.cmd_execute(
            "send log [INFO] [CSRTransitVNET] Configured {} {} routing.".format(
                role, self.section_dict['dmvpn']["RoutingProtocol"].lower()))
        return output

    def configure_routing_onprem(self, tunn_addr):
        onprem_bgp_neighbours = ""
        for key,item in self.section_dict['onprem'].items():
            if 'onpremTunnelIp' in key:
                onprem_bgp_neighbours += routing_onprem_bgp_neighbours.format(
                    onpremRoutingProtocolASN=self.section_dict['onprem']["onpremRoutingProtocolASN"],
                    onpremIp=str(item)
                )

        routing_config = onprem_routing_eigrp_bgp.format(
            RoutingProtocolASN=str(
                        self.section_dict['dmvpn']["RoutingProtocolASN"]),
            ConnName=self.section_dict['dmvpn']["ConnectionName"],
            TunnelId=self.section_dict['dmvpn']["TunnelID"],
            DMVPNTunnelIpNetworkNum=str(
                        self.section_dict['dmvpn']["DMVPNTunnelIpNetworkNum"]),
            DMVPNTunnelIpMask=str(
                        self.section_dict['dmvpn']["DMVPNTunnelIpMask"]),
            TunnelIP=str(tunn_addr),
            onpremRoutingProtocolASN=str(
                        self.section_dict['onprem']["onpremRoutingProtocolASN"]),
            OnpremConnName=str(
                        self.section_dict['onprem']["onpremConnectionName"]),
            OnpremTunnelId=str(
                        self.section_dict['onprem']["onpremTunnelID"]),
            onpremBgpNeighbours=onprem_bgp_neighbours
        )

        output = self.cmd_configure(routing_config)
        log.info("cfg routing output = %s" % output)

        self.cmd_execute(
            "send log [INFO] [CSRTransitVNET] Configured {} {} routing.".format(
                self.section_dict['role'],
                self.section_dict['dmvpn']["RoutingProtocol"].lower()))
        return output

    def configure_routing_nbma(self, DMVPNHubTunnelIp):
        cmd = routing_bgp_nbma
        cmd = cmd.format(
            RoutingProtocolASN=str(self.section_dict['dmvpn']["RoutingProtocolASN"]),
            DMVPNHubTunnelIp=str(DMVPNHubTunnelIp))
        output = self.cmd_configure(cmd)
        log.info("cfg routing output = %s" % output)
        return output

    def configure_crypto_policy(self):
        '''
        This functions is responsible for configuring the router with appropriate Crypto Policy.
        Right now, we will be configuring the general crypto policy (See py variable crypto_policy_general)
        The config string is appended accordingly with fields from self.section_dict
        Args:
            ROLE, SECTION_DICT
        Returns:
            None
        '''
        role = self.section_dict['role'].lower()

        if 'hub' in role:
            vrf_config = hub_vrf_config.format(
                ConnName=self.section_dict['dmvpn']["ConnectionName"],
                TunnelId=self.section_dict['dmvpn']["TunnelID"],
                RoutingProtocolASN=str(
                    self.section_dict['dmvpn']["RoutingProtocolASN"]))
            output = self.cmd_configure(vrf_config)
            log.info("[INFO] [CSRTransitVNET] Configured HUB VRF successfully")
            log.info("output = %s" % output)
            self.cmd_execute(
                "send log [INFO] [CSRTransitVNET] Configured HUB VRF successfully")

            if 'true' in self.section_dict['onpremoption'].lower():
                '''
                If role is HUB and 'onprem' option is set to true then these below configuration are triggered.
                They help in getting connected to OnPremise DMVPN cloud.
                
                '''
                onprem_vrf = onprem_vrf_config.format(
                    ConnName=self.section_dict['dmvpn']["ConnectionName"],
                    TunnelId=self.section_dict['dmvpn']["TunnelID"],
                    RoutingProtocolASN=str(
                        self.section_dict['dmvpn']["RoutingProtocolASN"]),
                    OnpremConnName=self.section_dict['onprem']["onpremConnectionName"],
                    OnpremTunnelId=self.section_dict['onprem']["onpremTunnelID"],
                    OnpremRoutingProtocolASN=str(
                        self.section_dict['onprem']["onpremRoutingProtocolASN"]))

                output = self.cmd_configure(onprem_vrf)
                log.info("[INFO] [CSRTransitVNET] Configured OnPremise VRF successfully")
                log.info("output = %s" % output)
                self.cmd_execute(
                    "send log [INFO] [CSRTransitVNET] Configured OnPremise VRF successfully")

                onprem_crypto_config = crypto_policy_general.format(
                    ConnName=self.section_dict['onprem']["onpremConnectionName"],
                    TunnelId=self.section_dict['onprem']["onpremTunnelID"],
                    SharedKey=self.section_dict['onprem']["onpremSharedKey"],
                    IpsecCipher=self.section_dict['onprem']["onpremIpsecCipher"],
                    IpsecAuthentication=self.section_dict['onprem']["onpremIpsecAuthentication"])

                output = self.cmd_configure(onprem_crypto_config)
                log.info(
                    '[INFO] [CSRTransitVNET] Configured OnPremise crypto policy general successfully')
                log.info("crypto policy output = %s" % output)
                self.cmd_execute(
                    "send log [INFO] [CSRTransitVNET] Configured OnPremise crypto policy general successfully")

        crypto_config = crypto_policy_general.format(
            ConnName=self.section_dict['dmvpn']["ConnectionName"],
            TunnelId=self.section_dict['dmvpn']["TunnelID"],
            SharedKey=self.section_dict['dmvpn']["SharedKey"],
            IpsecCipher=self.section_dict['dmvpn']["IpsecCipher"],
            IpsecAuthentication=self.section_dict['dmvpn']["IpsecAuthentication"])

        output = self.cmd_configure(crypto_config)
        log.info(
            '[INFO] [CSRTransitVNET] Configured crypto policy general successfully')
        log.info("crypto policy output = %s" % output)

        self.cmd_execute(
            "send log [INFO] [CSRTransitVNET] Configured crypto policy general successfully")
        return output

    def get_tunnel_addr(self):
        tunn_addr = None
        role = self.section_dict['role'].lower()
        tunnel_network = self.section_dict['DMVPNTunnelIpCidr']
        if 'hub' in role:
            log.info('[INFO] Configuring router as {}'.format(role))
            hub_dict = {}
            hub_dict['pip'] = self.cloud.tvnet.get_pip()
            self.section_dict['spoke'] = {'count': 0}
            tunn_addr = tunnel_network.network_address + int(self.section_dict['hub_number'])
            hub_dict['nbma'] = str(tunn_addr)
            self.section_dict[role] = hub_dict
        elif role == 'spoke':
            log.info('[INFO] Configuring router as SPOKE')
            try:
                dmvpn_address_count = tunnel_network.num_addresses
                spoke_vmid = self.cloud.tvnet.get_vmid()
                spoke_pip = self.cloud.tvnet.get_pip()
                random.seed(spoke_vmid)
                rand_tunn_offset = random.randint(10, dmvpn_address_count)
                self.section_dict['spoke']['count'] = int(
                    self.section_dict['spoke']['count'])
                self.section_dict['spoke']['count'] += 1
                tunn_addr = tunnel_network.network_address + rand_tunn_offset
                self.section_dict['spoke'][spoke_vmid] = {
                    'pip': str(spoke_pip), 'tunnel_address': str(tunn_addr)}
            except KeyError:
                log.info(
                    '[ERROR] Spoke count is not found in spoke file contents.')
                return None
        else:
            log.info('[ERROR] Unrecognized role is assigned to the router!')

        return tunn_addr

    def configure_pub_key(self):
        fingerprint = binascii.hexlify(self.cloud.tvnet.create_pem_file(filename='privatekey'))
        cmd = username_pubkey_config.format(
            username=str(self.section_dict['username_pubkey']),
            fingerprint=str(fingerprint)
        )

        # Save the private key in the storage account
        priv_keys_folder = self.section_dict['folder'] + '/privatekeys'

        self.cloud.tvnet.create_directory(self.section_dict['file_share'],
                                            priv_keys_folder)

        vmid = self.cloud.tvnet.get_vmid()

        if 'privatestrgacctname' in self.section_dict and 'privatestrgacckey' in self.section_dict:
            private_cloud = cloud(feature,
                                self.section_dict['privatestrgacctname'],
                                self.section_dict['privatestrgacckey'],
                                cloudname=self.section_dict['cloudname'])
            private_cloud.tvnet.create_share(self.section_dict['file_share'])
            private_cloud.tvnet.create_directory(self.section_dict['file_share'],
                                                 self.section_dict['folder'])
            private_cloud.tvnet.create_directory(self.section_dict['file_share'],
                                                 priv_keys_folder)
            private_cloud.tvnet.copy_local_file_to_remote(self.section_dict['file_share'],
                                                            priv_keys_folder,
                                                            vmid + '.pem',
                                                            os.getcwd() + '/privatekey.pem')
        else:
            self.cloud.tvnet.copy_local_file_to_remote(self.section_dict['file_share'],
                                                            priv_keys_folder,
                                                            vmid + '.pem',
                                                            os.getcwd() + '/privatekey.pem')

        output = self.cmd_configure(cmd)
        log.info("cfg ssh key output = %s" % output)
        return output

    def configure_transit_vnet(self):
        """
        This method is responsible for:

        1. Munch the data from custom data.
        2. Get inputs from storage account or write storage account
        3. Configure required IOS CLIs,
        4. Get a PEM Key data
        5. Configure automate username
        6. Push the PEM key to private storage account.
        """

        #Get the tunnel address to be used for this device.
        tunn_addr = self.get_tunnel_addr()

        # Check if files and details are written to storage account.
        # If not bail configuring.
        if not self.write_all_files():
            log.error("Could not write files to storage account. Exiting out!")
            self.cmd_execute(
                "send log [ERROR] [CSRTransitVNET] Failed to write files to storage account. Exiting out!")
            return False

        self.configure_crypto_policy()
        self.configure_tunnel(tunn_addr)
        if self.section_dict['onpremoption'] == 'true':
            self.configure_routing_onprem(tunn_addr)
        else:
            self.configure_routing(tunn_addr)
        role = self.section_dict['role'].lower()
        if 'spoke' in role.lower():
            for key, value in self.section_dict.items():
                if 'hub-' in key:
                    #self.configure_tunnel_nhsnbma(value['nbma'], value['pip'])
                    if 'bgp' in self.section_dict['dmvpn']["RoutingProtocol"].lower():
                        self.configure_routing_nbma(value['nbma'])
        self.cmd_execute(
            "send log [INFO] [CSRTransitVNET] Success. Configured all the required IOS configs for role: {}.".format(
                self.section_dict['role'].lower()))
        if self.section_dict['configure_pubkey']:
            self.cmd_execute(
                "send log [INFO] [CSRTransitVNET] Configuring the public key for username {}.".format(
                    self.section_dict['username_pubkey']
                ))
            self.configure_pub_key()
