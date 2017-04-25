import os, argparse, ftplib, sys

def GetCredentials(keyFile):
    creds = []

    if os.path.exists(keyFile) and os.path.isfile(keyFile):
        credFile = open(keyFile, 'r')
        creds = credFile.readline()
        credFile.close()
    else:
        raise FileNotFoundError("Key File {} not found.".format(keyFile))
        quit(-1)

    creds = creds.split(',')
    
    return creds[0], creds[1], creds[2]

def WipeFTP(connection, destinationDirectory):
    '''Delete all files within destinationDirectory'''
    return

def PopulateFTP(connection, distributionDirectory, destinationDirectory):
    '''Populate a FTP destination with files from distribution'''
    return

def Deploy(distributionDirectory, destinationDirectory, keyFile):
    user = ''
    key = ''
    addr = ''
    user, key, addr = GetCredentials(keyFile)

    connection = None
    try:
        print("Establishing connection to {}".format(addr))
        connection = ftplib.FTP(addr, user, key)
        print("Successfully connected.")

        WipeFTP(connection, destinationDirectory)
        PopulateFTP(connection, distributionDirectory, destinationDirectory)

        connection.close()
    except Exception:
        print("Unexpected error:", sys.exc_info())

def ListFiles(distributionDirectory):
    for dirpath, dirnames, filenames in os.walk(distributionDirectory):
        for filename in filenames:
            print(os.path.join(dirpath, filename))


parser = argparse.ArgumentParser(description="Deploy files and folders to a remote webserver.")

parser.add_argument('s', help="Source directory", type=str)
parser.add_argument('t', help="Target directory", type=str)
parser.add_argument('b', help="Backup directory", type=str)
parser.add_argument('keyfile', help="Keyfile directory", type=str)

args = parser.parse_args()

Deploy(args.s, args.t, args.b, args.keyfile)