from distutils.core import setup
from setuptools.command.install import install
from subprocess import check_call
import os, platform


project_name = 'csr_azure_utils'
project_ver = '1.0.0'

'''
=======================================================================================
Note
=======================================================================================
This file is crucial to installation of csr_azure_utils. 
Before committing any changes to this file, please test installation of csr_azure_utils
beforehand on your local machine/MacBook and in Guestshell running in CSR.
'''

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        try:
            print "We are running in the postInstallCommand"
            cwd = os.path.dirname(os.path.realpath(__file__))
            if "centos" in platform.dist()[0].lower() and  "guestshell" in os.popen("whoami").read().strip():
                check_call("sudo cp auth-token.service /etc/systemd/user/",
                           shell=True)
                check_call("sudo systemctl enable /etc/systemd/user/auth-token.service",
                           shell=True)
            else:
                print "Skipping auth-service setup, csr_azure_utils couldn't find either guestshell as \
                active user or platform not centos"
            install.run(self)
        except Exception as e:
            print "Unable to setup the token service via systemd"

setup(
    name=project_name,
    packages=["csr_cloud"],
    version=project_ver,
    description='Utilities for csr1000v on Azure',
    author='Christopher Reder',
    author_email='creder@cisco.com',
    # use the URL to the github repo
    url='https://github4-chn.cisco.com/csr1000v-azure/' + project_name,
    download_url='https://github4-chn.cisco.com/csr1000v-azure/' + project_name + '/archive/' + \
         project_ver + '.tar.gz',
    keywords=['cisco', 'azure', 'guestshell', 'csr1000v'],
    classifiers=[],
    license="MIT",
    install_requires=[
        'urllib3[secure]',
        'python-crontab',
        'pathlib',
        'requests',
        'azure-storage',
        'configparser',
        'requests',
        'pyopenssl',
        'msrest',
        'msrestazure',
        'azure-storage',
        'azure-mgmt-applicationinsights',
        'applicationinsights',
        'azure-mgmt-monitor',
        'paramiko'
    ],
    cmdclass={
        'install': PostInstallCommand,
    }
)

