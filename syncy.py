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

def wipe_ftp(connection, destination_directory):
    '''Delete all files within destination_directory'''
    return

def populate_ftp(connection, distribution_directory, destination_directory):
    '''Populate a FTP destination with files from distribution'''
    return

def deploy(distribution_directory, destination_directory, key_file):
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

        wipe_ftp(connection, destination_directory)
        populate_ftp(connection, distribution_directory, destination_directory)

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
PARSER.add_argument('t', help="Target directory", type=str)
PARSER.add_argument('b', help="Backup directory", type=str)
PARSER.add_argument('keyfile', help="Keyfile directory", type=str)

ARGS = PARSER.parse_args()

deploy(ARGS.s, ARGS.t, ARGS.keyfile)
