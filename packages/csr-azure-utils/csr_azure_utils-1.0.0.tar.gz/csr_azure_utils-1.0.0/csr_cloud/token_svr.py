#!/usr/bin/env python

import os
import sys
from os.path import expanduser
import socket
import requests
import subprocess
import urllib3.contrib.pyopenssl
import traceback
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta

base_dir = expanduser('~') + '/cloud/tokenSvr/'


# Specify files accessed by this script in guestshell
get_response_file = base_dir + "token_get_rsp"
debug_file = base_dir + "token_svr.log"
sock_file = base_dir + "sock_file"
cert_file = "/etc/ssl/certs/ca-bundle.trust.crt"
token_file = base_dir + "token_file"
msi_dir = "/var/log/azure/Microsoft.ManagedIdentity.ManagedIdentityExtensionForLinux"
msi_service_file = "/etc/systemd/system/azuremsixtn.service"



if not os.path.exists(base_dir):
    os.makedirs(base_dir)


logger = logging.getLogger("Token_svr")
handler = RotatingFileHandler(debug_file, maxBytes=1000000, backupCount=2)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)



def aad_get_token(cloud, tenantId, appId, appKey):
    if cloud == 'azure':
        url = "https://login.microsoftonline.com/%s/oauth2/token?api-version=1.1" % tenantId
        payload = {'grant_type': 'client_credentials',
                   'client_id': appId,
                   'resource': 'https://management.core.windows.net/',
                   'client_secret': appKey}

    elif cloud == 'azusgov':
        url = "https://login-us.microsoftonline.com/%s/oauth2/token?api-version=1.1" % tenantId
        payload = {'grant_type': 'client_credentials',
                   'client_id': appId,
                   'resource': 'https://management.core.usgovcloudapi.net/',
                   'client_secret': appKey}
    elif cloud == 'azchina':
        url = "https://login.chinacloudapi.cn/%s/oauth2/token?api-version=1.1" % tenantId
        payload = {'grant_type': 'client_credentials',
                   'client_id': appId,
                   'resource': 'https://management.core.chinacloudapi.cn/',
                   'client_secret': appKey}

    else:
        logger.error("Server: aad_get_token: invalid cloud name %s", cloud)
        return ''

    # Specify the HTTP POST request to obtain a token
    all_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': 'accept:application/json',
                   'Authorization': 'OAuth 2.0'}

    # Send the HTTP POST request for the token
    try:
        response = requests.post(url, data=payload, verify=cert_file, headers=all_headers)
    except requests.exceptions.RequestException as e:
        logger.exception("Server: aad_get_token: request had error %s", e)
        return ''

    if 200 != response.status_code:
        logger.error("Server: aad_get_token: request failed rc=%d", response.status_code)
        with open(get_response_file, 'wb') as token_fh:
            for chunk in response.iter_content(chunk_size=64):
                token_fh.write(chunk)
        return ''

    # Parse the HTTP GET response
    try:
        token = response.json()["access_token"]
        logger.info("Server: aad_get_token: obtained token")

    except Exception as e:
        logger.exception("Server: aad_get_token: caught exception %s", e)
        tb = traceback.format_exc()
        logger.exception("%s", tb)
        token = ''

    return token


def msi_get_token_by_http():
    # Specify the HTTP GET request to obtain a token
    url = "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01"
    payload = {'resource': 'https://management.azure.com/'}
    header = {'Metadata': 'true'}

    # Send the HTTP GET request for the token
    try:
        response = requests.get(url, params=payload, verify=False, headers=header)
    except requests.exceptions.RequestException as e:
        logger.exception("Server: msi_get_token: request had an error %s", e)
        return ''

    if 200 != response.status_code:
        logger.exception("Server: msi_get_token: request failed rc=%d", response.status_code)
        with open(token_file, 'w') as token_fh:
            token_fh.write(response.json())
        return ''

    # Parse the HTTP GET response
    try:
        token = response.json()["access_token"]
        logger.info("Server: msi_get_token: obtained token")


    except Exception as e:
        logger.exception("Server: msi_get_token: caught exception %s", e)
        tb = traceback.format_exc()
        logger.exception("%s", tb)
        token = ''

    return token


def msi_get_token_by_extension():
    # Check if user has successfully installed the Managed Identity Extension
    if not os.path.exists(msi_dir):
        # Directory does not exist.  Don't use MSI
        logger.info("Server: msi_get_token: MSI not installed")
        return ''

    # Check if the MSI service is running
    try:
        subprocess.check_output("pgrep -f msi-extension", shell=True)
    except:
        # Check if the Managed Identity Extension has been installed
        if os.path.exists(msi_service_file):
            # File has been installed.  Try to start the service.
            os.system("sudo systemctl enable azuremsixtn")
            os.system("sudo systemctl start azuremsixtn")
            logger.exception("Server: msi_get_token: started MSI service")
        else:
            # Directory does not exist.  Don't use MSI
            logger.exception("Server: msi_get_token: MSI not installed")
            return ''

    # Specify the HTTP GET request to obtain a token
    url = "http://localhost:50342/oauth2/token"
    payload = {'resource': 'https://management.azure.com/'}
    header = {'Metadata': 'true'}

    # Send the HTTP GET request for the token
    response = requests.get(url, params=payload, verify=False, headers=header)

    if 200 != response.status_code:
        logger.error("Server: msi_get_token: request failed rc=%d", response.status_code)
        with open(token_file, 'w') as token_fh:
            token_fh.write(response.json())
        return ''

    # Parse the HTTP GET response
    token = response.json()["access_token"]
    logger.info("Server: msi_get_token: obtained token")

    return token

def start_token_svr(): #pragma: no cover
    # Find out the process ID
    pid = os.getpid()

    # Open the debug log file
    logger.info("Token server started, pid=%d", pid)
    # Make sure the socket does not already exist
    try:
        os.unlink(sock_file)
    except OSError:
        if os.path.exists(sock_file):
            raise

    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Bind the socket to the port
    sock.bind(sock_file)

    # Use OpenSSL to check certificates for https
    urllib3.contrib.pyopenssl.inject_into_urllib3()

    # Listen for incoming connections
    sock.listen(1)

    token = ''
    token_expiry_time = datetime.utcnow() - timedelta(minutes=1)

    while True:
        # Wait for a connection
        connection, client_address = sock.accept()
        try:
            while True:
                # Read a command from the client
                line = connection.recv(255)
                if line == '':
                    break

                # Clearing the token if the token expiration time is less than 5 minutes
                if datetime.utcnow() > token_expiry_time:
                    token = ''

                command = line.rsplit(' ')
                if command[0] == "MSI_req":

                    if token == '':
                        # Get a new token
                        token = msi_get_token_by_http()
                        token_expiry_time = datetime.utcnow() + timedelta(minutes=5)
                    else:
                        logger.info("Server: MSI_req: using cached token")

                    # Send the number of bytes in the token
                    token_len = len(token)
                    token_len_as_str = str(token_len) + ' '
                    connection.sendall(token_len_as_str)

                    # Send the token
                    if token != '':
                        connection.sendall(token)
                    else:
                        logger.error("Server: no token returned by MSI")

                elif command[0] == "AAD_req":
                    if token == '':
                        # Get a new token
                        token = aad_get_token(command[1], command[2], command[3], command[4])
                        token_expiry_time = datetime.utcnow() + timedelta(minutes=5)
                    else:
                        logger.info("Server: AAD_req: using cached token")

                    # Send the number of bytes in the token
                    token_len = len(token)
                    token_len_as_str = str(token_len) + ' '
                    connection.sendall(token_len_as_str)

                    # Send the token
                    if token != '':
                        connection.sendall(token)
                    else:
                        logger.error("Server: no token returned by AAD")

                elif command[0] == "Ping":
                    connection.sendall("Ack")
                elif command[0] == 'Clear':
                    token = " "
                else:
                    logger.error("Token server unrecognized command %s", command)
                    err_msg = "Error: invalid command %s" % command
                    connection.sendall(err_msg)

            # Clean up the connection
            connection.close()

        except Exception as e:
            logger.error("Token server caught exception %s", e)
            tb = traceback.format_exc()
            logger.error("%s", tb)
            connection.sendall(e.message)
            connection.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Incorrect usage of token server script")
        logger.info("Usage: {} start".format(__file__))
        sys.exit(1)
    if sys.argv[1] == 'start':
        start_token_svr()