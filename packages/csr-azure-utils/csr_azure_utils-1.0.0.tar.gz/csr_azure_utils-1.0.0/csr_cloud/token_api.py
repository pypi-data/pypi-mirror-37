import os
import sys
import time
import logging
from logging.handlers import RotatingFileHandler
import socket
import subprocess
from os.path import expanduser

base_dir = expanduser('~') + '/cloud/tokenApi/'
sock_file = expanduser('~') + "/cloud/tokenSvr/sock_file"
log_file = base_dir+"tokenApi.log"


if not os.path.exists(base_dir):
    os.makedirs(base_dir)

logger = logging.getLogger("Token_api")
handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=2)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def open_socket(): #pragma : no cover
    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    try:
        sock.connect(sock_file)
    except socket.error, msg:
        logger.error("API: open_socket connect error %s" % msg)
        return (1, msg)
    return (0, sock)


def ping_server(sock):
    sock.settimeout(3)
    try:
        # Send data
        message = 'Ping'
        sock.sendall(message)

        # Receive the response
        data = sock.recv(8)
        if data == "Ack":
            return 0
        logger.error("API: ping_server: unexpected server response %s" % data)
        return 1

    except socket.error as (value, message):
        logger.error("API: ping_server: socket error %s" % message)
        return 2
    except socket.timeout:
        logger.error("API: ping_server: socket timeout")
        return 3
    except Exception as (value, message):
        logger.error("API: ping_server: other socket error %s" % message)
        return 4


def connect():
    global sock

    (rc, sock) = open_socket()
    if rc != 0:
        return rc

    rc = ping_server(sock)
    if rc != 0:
        logger.error("API: connect: ping failed")

    return rc

def clear_token(): # pragma: no cover
    global sock

    try:
        # Send data
        message = 'Clear'
        sock.sendall(message)

        # Receive the response
        data = sock.recv(32)
        if data == "OK":
            return 0
        logger.error("API: clear_token: unexpected server response %s" % data)
        return 0

    except socket.error:
        logger.error("API: clear_token: socket error")
        return 1


def disconnect(): # pragma: no cover
    global sock
    sock.close()

def request_token_by_msi(): # pragma: no cover
    global sock
    token = ''
    try:
        # Send request message
        req_msg = "MSI_req"
        sock.sendall(req_msg)

        # Receive the number of bytes in the token
        data = sock.recv(8)
        # Split the first response from the server
        two_str = data.rsplit(' ')
        token_len = int(two_str[0])
        token = two_str[1]

        # Now get the remaining bytes of the token
        done = False
        total_bytes_received = len(two_str[1])
        while total_bytes_received < token_len:
            data = sock.recv(8)
            bytes_received = len(data)
            token = token + data
            total_bytes_received += bytes_received

    except socket.error as (value, message):
        logger.error("API: msi: socket error %s" % message)
        logger.error("API: msi: expected token len %d" % token_len)
        logger.error("API: msi: actual token len %d" % total_bytes_received)
        token = ''
    except socket.timeout:
        logger.error("API: msi: socket timeout")
        logger.error("API: msi: expected token len %d" % token_len)
        logger.error("API: msi: actual token len %d" % total_bytes_received)
        token = ''
    except Exception as (value, message):
        logger.error("API: msi: other socket error %s" % message)
        logger.error("API: msi: expected token len %d" % token_len)
        logger.error("API: msi: actual token len %d" % total_bytes_received)
        token = ''

    finally:
        return token


def get_token_by_msi():
    for attempt in range(3):
        rc = connect()
        if rc == 0:
            token = request_token_by_msi()

            if token == '':
                logger.error("API:msi: Failed to get token on attempt %d" % attempt)
                disconnect()
                if attempt < 3:
                    time.sleep(2)
                else:
                    return token
            else:
                disconnect()
                break
        else:
            if attempt < 3:
                time.sleep(2)
    else:
        return ''
    return token

def request_token_by_aad(cloud, tenantId, appId, appKey): #pragma: no cover
    global sock, debug_fh
    token = ''
    try:
        # Send request message
        req_msg = "AAD_req %s %s %s %s" % (cloud, tenantId, appId, appKey)
        sock.sendall(req_msg)

        # Receive the number of bytes in the token
        data = sock.recv(8)
        # Split the first response from the server
        two_str = data.rsplit(' ')
        token_len = int(two_str[0])
        token = two_str[1]
        token_len = token_len - len(two_str[1])

        # Now get the remaining bytes of the token
        done = False
        total_bytes_received = 0
        while total_bytes_received < token_len:
            data = sock.recv(8)
            bytes_received = len(data)
            token = token + data
            total_bytes_received += bytes_received

    except socket.error as err:
        logger.error("API: aad: socket error %d" % err.errno)
        token = ''
    except socket.timeout:
        logger.error("API: aad: socket timeout")
        token = ''
    except Exception as err:
        logger.error("API: aad: other socket error")
        token = ''

    finally:
        return token


class Token_api():
    def __init__(self):
        if connect() != 0:
            subprocess.call(["sudo", "systemctl", "stop", "auth-token" ])
            subprocess.call(["sudo", "systemctl", "start", "auth-token"])
            logger.error("Restarting the Token_svr")
            time.sleep(3)
            rc = connect()
            if rc != 0:
                logger.error("Unable to start the Token_svr")
                logger.error("Failed connection to Token Manager rc=%d" % rc)
                sys.exit()

    def request_token_by_aad(self, cloud, tenantId, appId, appKey):
        return request_token_by_aad(cloud, tenantId, appId, appKey)

    def get_token_by_msi(self):
        return get_token_by_msi()

    def disconnect(self): # pragma: no cover
        return disconnect()

    def is_server_up(self):
        return connect()


