import os
from shutil import copyfile
import logging


feature = "tvnet"
log = logging.getLogger(feature)

def setup_directory(directory):
    '''
    This function will help with setting up directory structure.
    '''
    folder_list = ['logs', 'data', 'bin']
    if not os.path.exists(directory):
        os.makedirs(directory)
    for folder in folder_list:
        folder_path = os.path.join(directory, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

def copy_custom_data_file(file, tvnet_home):
    dest = os.path.join(tvnet_home, 'customdata.txt')
    print(dest)

    if not os.path.exists(dest):
        if os.path.exists(file):
            copyfile(file, dest)
        else:
            log.error('FATAL ERROR: No custom data file found!')
            return False
    return dest