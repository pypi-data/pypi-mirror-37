import os
import paramiko
import string

class GeneralUtils():
    '''

    This Class very generic util functions.

    '''
    
    def __init__(self):
        pass

    def create_pem_file(self, filename='privateKey', bits=1024):
        key = paramiko.RSAKey.generate(bits)
        key.write_private_key_file(os.path.join(os.getcwd(), '%s.pem' % filename))
        return key.get_fingerprint()

    def create_password(self, pwdLength=13):
        chars = string.ascii_letters + string.digits
        password = ''
        for i in range(int(pwdLength)):
            password += chars[ord(os.urandom(1)) % len(chars)]
        return password
