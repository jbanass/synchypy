'''Syncy.py synchronizes a local directory with a remote ftp server'''
import os
import argparse
import ftplib
import sys

def get_credentials(key_file):
    '''Obtains credentials from key_file'''
    creds = []

    if os.path.exists(key_file) and os.path.isfile(key_file):
        credential_file = open(key_file, 'r')
        creds = credential_file.readline()
        credential_file.close()
    else:
        raise FileNotFoundError("Key File {} not found.".format(key_file))

    creds = creds.split(',')
    return creds[0], creds[1], creds[2]

def wipe_ftp(connection):
    '''Delete all files within destination_directory'''
    return

def translate_local_to_ftp(files_dict: dict, distribution_directory: str):
    '''Performs directory translation between a nested directory locally to \
     a normalized directory remotely'''
    return_dict = {}

    for key in files_dict:
        if key == distribution_directory:
            return_dict['/'] = files_dict[key]
        else:
            translated_key = '/' + key.replace('\\', '/')[len(distribution_directory):len(key)] + '/'
            return_dict[translated_key] = files_dict[key]

    return return_dict

def populate_ftp(connection, distribution_directory):
    '''Populate a FTP destination with files from distribution'''
    files_dict = {}

    for root, dirs, files in os.walk(distribution_directory):
        files_dict[root] = (dirs, files)

    ftp_dict = translate_local_to_ftp(files_dict, distribution_directory)

    #make folders
    for folders in ftp_dict:
        for folder in ftp_dict[folders][0]:
            print("Making folder: {}{}".format(folders, folder))
            connection.mkd(folders + folder)
    #transfer files
    for folders in ftp_dict:
        for files in ftp_dict[folders][1]:
            normalized_path = distribution_directory +  \
                folders[1:len(folders)].replace("/", "\\") + files
            normalized_ftp_path = folders + files
            print("Transferring file from {} to {}".format(normalized_path, normalized_ftp_path))
            myfile = open(normalized_path, 'rb')
            connection.storbinary("STOR {}".format(normalized_ftp_path), myfile)
            myfile.close()


def deploy(distribution_directory, key_file):
    '''Deploys files from distribution_directory to destination_directory \
    with credentials supplied by key_file'''
    user = ''
    key = ''
    addr = ''
    user, key, addr = get_credentials(key_file)

    connection = None
    try:
        print("Establishing connection to {}".format(addr))
        connection = ftplib.FTP(addr, user, key)
        print("Successfully connected.")

        wipe_ftp(connection)
        populate_ftp(connection, distribution_directory)

        connection.close()
    except Exception:
        print("Unexpected error:", sys.exc_info())

def list_files(distribution_directory):
    '''Lists files in distribution_directory'''
    for dirpath, dirnames, filenames in os.walk(distribution_directory):
        for filename in filenames:
            print(os.path.join(dirpath, filename))


PARSER = argparse.ArgumentParser(description="Deploy files and folders to a remote webserver.")

PARSER.add_argument('s', help="Source directory", type=str)
PARSER.add_argument('keyfile', help="Keyfile directory", type=str)

ARGS = PARSER.parse_args()

deploy(ARGS.s, ARGS.keyfile)
