import logging
import re
import time
import ipaddress
from utilities import setup_directory, copy_custom_data_file

feature = "tvnet"
log = logging.getLogger(feature)
tvnet_home = '/home/guestshell/' + feature

class base_csr_transit():
    def __init__(self, customDataFileName):
        self.section_dict = {}
        setup_directory(tvnet_home)

        self.cd_file = copy_custom_data_file(customDataFileName, tvnet_home)
        if not self.cd_file:
            raise IOError("Failed to load Custom Data File")

    def setup_dmvpn_dict(self):
        param_list = ['TunnelKey', 'RoutingProtocol', 'transitvnetname']
        dmvpn_dict = {}
        for param in param_list:
            dmvpn_dict[param] = self.section_dict[param]
        return dmvpn_dict

    # todo: make keyword generic
    def parse_decoded_custom_data(self, keyword='AzureTransitVNET'):
        section_flag = False
        try:
            with open(self.cd_file) as filecontents:
                for line in filecontents:
                    if 'section:' in line:
                        if keyword.lower() in line.lower():
                            section_flag = True
                        else:
                            section_flag = False

                    if section_flag:
                        split_line = line.split(' ')

                        if len(split_line) == 2:
                            self.section_dict[split_line[0].strip(
                            )] = split_line[1].strip()

                        else:
                            log.info(
                                '[ERROR] command parsing failed for %s' %
                                str(split_line))
        except IOError as e:
            log.exception('[ERROR] %s' % e)
            return False

        log.info(self.section_dict)

        return True

    def setup_file_dict(self):
        self.section_dict['folder'] = 'config'
        self.section_dict['file_names'] = {
            'hub-1': 'hub1.json',
            'hub-2': 'hub2.json',
            'spoke': 'spokes.json',
            'dmvpn': 'dmvpn.json',
            'onprem': 'onprem.json'
        }
        try:
            role = self.section_dict['role']
        except KeyError:
            log.error('FATAL ERROR: No ROLE found!')

        try:
            self.section_dict['onpremoption']
            if 'spoke' in role.lower():
                self.section_dict['onpremoption'] = 'false'
        except KeyError:
            self.section_dict['onpremoption'] = 'false'


        if 'hub' in role.lower():
            result = re.search('hub-(\d+)', role)
            if result is not None:
                self.section_dict['hub_number'] = int(result.groups()[0])
            else:
                result = re.search('(\d+)', role)
                self.section_dict['hub_number'] = int(result.groups()[0])
                role = 'hub-' + str(int(result.groups()[0]))
                self.section_dict['role'] = role

            if role not in self.section_dict['file_names'].keys():
                self.section_dict['file_names'][role] = role.replace('-', '') + '.json'
        try:
            file_share = self.section_dict['transitvnetname'].lower()
            self.section_dict['file_share'] = file_share
        except KeyError:
            file_share = 'new'
            self.section_dict['file_share'] = file_share

    def setup_default_dict(self):

        if 'dmvpn' not in self.section_dict:
            self.section_dict['dmvpn'] = {}

        '''
        Below double KeyError is essential for the sequence of where we take 
        in DMVPN tunnel Ipaddress from.
        3. Get CIDR from custom data.
        2. if not found replace with 1.1.1.0/24
        1. Override previous two if data is present in Storage accounts 'dmvpn.json'
        '''
        try:
            DMVPNTunnelIpCidrStr = self.section_dict['DMVPNTunnelIpCidr']

        except KeyError:
            DMVPNTunnelIpCidrStr = u'1.1.1.0/24'
        try:
            DMVPNTunnelIpCidrStr = self.section_dict['dmvpn']['DMVPNTunnelIpCidr']
        except KeyError:
            pass

        try:
            DMVPNTunnelIpCidr = ipaddress.IPv4Network(DMVPNTunnelIpCidrStr.decode('utf-8'))
        except AttributeError:
            DMVPNTunnelIpCidr = ipaddress.IPv4Network(DMVPNTunnelIpCidrStr)

        self.section_dict['DMVPNTunnelIpCidr'] = DMVPNTunnelIpCidr

        default_dict = {
            "ConnectionName": "tvnet",
            "RoutingProtocol": "EIGRP",
            "TunnelID": 11,
            "TunnelKey": 12210,
            "SharedKey": 'ciscokey',
            "IpsecCipher": "esp-aes",
            "IpsecAuthentication": "esp-sha-hmac",
            "RoutingProtocolASN": 64512,
            "NHRPAuthString": 'cisco',
            "NHRPNetworkId": 1024
        }

        for key, value in default_dict.items():
            try:
                self.section_dict[key]
                self.section_dict['dmvpn'][key] = self.section_dict[key]
            except KeyError:
                try:
                    self.section_dict['dmvpn'][key]
                    self.section_dict[key] = self.section_dict['dmvpn'][key]
                except KeyError:
                    self.section_dict[key] = value
                    self.section_dict['dmvpn'][key] = value

        try:
            self.section_dict['onpremoption']
            self.section_dict['onprem'] = {}
            if 'spoke' in self.section_dict['role'].lower():
                self.section_dict['onpremoption'] = 'false'
        except KeyError:
            self.section_dict['onpremoption'] = 'false'

        if 'hub' in self.section_dict['role'] and 'true' in self.section_dict['onpremoption'].lower():
            onpremise_dict = {
                "onpremConnectionName": "onprem",
                "onpremRoutingProtocol": "BGP",
                "onpremTunnelID": 12,
                "onpremTunnelKey": 14440,
                "onpremSharedKey": 'onpremkey',
                "onpremIpsecCipher": "esp-aes",
                "onpremIpsecAuthentication": "esp-sha-hmac",
                "onpremRoutingProtocolASN": 60000,
                "onpremNHRPAuthString": 'onprem',
                "onpremNHRPNetworkId": 999
            }
            for key, value in onpremise_dict.items():
                try:
                    self.section_dict[key]
                    self.section_dict['onprem'][key] = self.section_dict[key]
                except KeyError:
                    try:
                        self.section_dict['onprem'][key]
                        self.section_dict[key] = self.section_dict['onprem'][key]
                    except KeyError:
                        self.section_dict[key] = value
                        self.section_dict['onprem'][key] = value

            # Missing any of the item from below list will result in stale config. Strictly error check.
            onpremise_list_mandatory = ['onpremTunnelStartAddress','onpremTunnelEndAddress',
                                        'onpremTunnelIp1', 'onpremPublicIp1', 'onpremTunnelMask']
            for item in onpremise_list_mandatory:
                try:
                    try:
                        if 'Mask' in item:
                            dummyip = u'10.0.0.0/'
                            dummyip += str(self.section_dict[item])
                            dummyip = ipaddress.IPv4Network(dummyip.decode('utf-8'))
                            self.section_dict['onprem'][item] = dummyip.netmask
                        else:
                            self.section_dict['onprem'][item] = ipaddress.IPv4Address(
                                self.section_dict[item].decode('utf-8'))
                    except AttributeError:
                        self.section_dict['onprem'][item] = ipaddress.IPv4Address(self.section_dict[item])
                except KeyError:
                    log.error(
                        '[ERROR] [Transit VNET] On Premise config key {} not found'.format(item))
                    self.section_dict['onpremoption'] = 'false'
                except ipaddress.AddressValueError:
                        log.error(
                            '[ERROR] [Transit VNET] On Premise config key {} has incorrect value {}'
                                .format(item, self.section_dict[item]))
                        self.section_dict['onpremoption'] = 'false'

            if self.section_dict['onpremoption'] == 'true':
                onpremise_list_optional = [ 'onpremTunnelIp2', 'onpremPublicIp2']
                for item in onpremise_list_optional:
                    try:
                        try:
                            self.section_dict['onprem'][item] = ipaddress.IPv4Address(
                                self.section_dict[item].decode('utf-8'))
                        except AttributeError:
                            self.section_dict['onprem'][item] = ipaddress.IPv4Address(self.section_dict[item])
                    except:
                        log.info(
                            '[INFO] [Transit VNET] Optional On Premise config key {} ignored'.format(item))

                onprem_tunnel_number = self.section_dict['hub_number'] - 1
                onprem_tunnel_ip = self.section_dict['onprem']['onpremTunnelStartAddress'] + onprem_tunnel_number
                if onprem_tunnel_ip > self.section_dict['onprem']['onpremTunnelEndAddress']:
                    log.info(
                        '[ERROR] [Transit VNET] Ran out of Tunnel IPs for On Premise Tunnel')
                    log.info(
                        '''[ERROR] [Transit VNET] Calculated on premise tunnel IP is beyond acceptable range                        
                                START: {}
                                END: {}
                                Calculated IP: {}
                        '''.format(str(self.section_dict['onprem']['onpremTunnelStartAddress']),
                                   str(self.section_dict['onprem']['onpremTunnelEndAddress']),
                                   str(onprem_tunnel_ip)))
                    self.section_dict['onpremoption'] = 'false'
                else:
                    self.section_dict['onprem']['onprem_tunnel_ip'] = onprem_tunnel_ip

                if not 'eigrp' in self.section_dict['dmvpn']["RoutingProtocol"].lower():
                    log.info(
                        '[ERROR] [Transit VNET] On Premise configuration supports only EIGRP on transit VNET side')

                    self.section_dict['onpremoption'] = 'false'

        tunnel_addressing_dict = {
            "DMVPNTunnelIpCidr": DMVPNTunnelIpCidr,
            "DMVPNHubTunnelIp1": DMVPNTunnelIpCidr.network_address + 1,
            "DMVPNHubTunnelIp2": DMVPNTunnelIpCidr.network_address + 2,
            "DMVPNTunnelIpMask": DMVPNTunnelIpCidr.netmask,
            "DMVPNTunnelIpNetworkNum": DMVPNTunnelIpCidr.network_address,
            "DMVPNTunnelIpHostMask": DMVPNTunnelIpCidr.hostmask,
            "DMVPNTunnelIpPrefixLen": DMVPNTunnelIpCidr.prefixlen
        }

        for key, value in tunnel_addressing_dict.items():
            self.section_dict[key] = value
            self.section_dict['dmvpn'][key] = value

    def write_all_files(self):
        if 'hub' in self.section_dict['role']:
            file_list = ['spoke', self.section_dict['role'], 'dmvpn', 'onprem']
        elif 'spoke' in self.section_dict['role']:
            file_list = ['spoke']

        for file_content in file_list:
            try:
                file_contents = self.section_dict[file_content]
                try:
                    file_name = self.section_dict['file_names'][file_content]
                except KeyError:
                    temp = file_content
                    file_name = temp.replace('-', '') + '.json'
                log.info(
                    '[INFO] Savings contents for {} in {} with {}'.format(
                        file_content, file_name, str(file_contents)))
                status = self.cloud.tvnet.write_file_contents(
                    self.section_dict['file_share'],
                    self.section_dict['folder'],
                    file_name,
                    file_contents)
                if not status:
                    log.error(
                        '[ERROR] Failed to save contents for {} in {} with {}'.format(
                        file_content, file_name, str(file_contents)))
                    return False
            except KeyError:
                log.info(
                    '[ERROR] could not save file for {}'.format(file_content))
        return True

    def get_all_files(self):
        if 'spoke' in self.section_dict['role']:
            file_list = ['spoke', 'dmvpn']
            folder_contents = self.cloud.tvnet.get_list_directories_and_files(
                self.section_dict['file_share'],
                self.section_dict['folder'])
            if not folder_contents:
                log.error("[ERROR] Either Storage account is not present or Transit VNET name is incorrect!")
                return False
            for item in folder_contents:
                if 'hub' in item['name']:
                    result = re.search('(\d+)', item['name'])
                    hub_number = int(result.groups()[0])
                    if item['type'] == 'File':
                        hubname = 'hub-' + str(hub_number)
                        file_list.append(hubname)
                        try:
                            hubfile_name = self.section_dict['file_names'][hubname]
                            if hubfile_name != item['name']:
                                self.section_dict['file_names'][hubname] = item['name']
                        except KeyError:
                            self.section_dict['file_names'][hubname] = item['name']
        else:
            file_list = ['dmvpn']

        hub_flag = False
        if 'hub' in self.section_dict['role']:
            hub_flag = True

        for file_content in file_list:
            contents = None
            tries = 0
            while contents is None:
                log.info(
                    '{} {} {}'.format(
                        self.section_dict['file_share'],
                        self.section_dict['folder'],
                        self.section_dict['file_names'][file_content]))
                contents = self.cloud.tvnet.get_file_contents_json(
                    self.section_dict['file_share'],
                    self.section_dict['folder'],
                    self.section_dict['file_names'][file_content])
                if contents:
                    log.info(
                        '[INFO] Retrieved file contents for {}: {}'.format(
                            file_content, str(contents)))
                else:
                    if hub_flag:
                        break
                    log.info(
                        '[ERROR] Error while retrieving {}. Try num: {}'.format(
                            file_content, str(tries)))
                    time.sleep(50)
                    tries += 1
            if contents:
                self.section_dict[file_content] = contents

        return self.section_dict
