#!/usr/bin/env python

'''
Cisco Copyright 2018
Author: Abhinav Sanakkayala <asanakka@cisco.com>




'''
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
import logging

log = logging.getLogger('csr_tvnet')

class BlobUtils():
    def __init__(self, account_name, account_key):

        self.block_blob_service = BlockBlobService(
            account_name=account_name, account_key=account_key)

    def create_container_if_doesnt_exist(self, containername):
        if self.does_container_exist(containername) is False:
            self.block_blob_service.create_container(containername)

    def download_file_from_container(self, containername, filename, directory="/bootflash/"):
        try:
            self.block_blob_service.get_blob_to_path(
                containername, filename, directory + filename)
        except Exception as e:
            log.exception("Config File Download Failed.  Error: %s" % e)
            return False
        print("\nDownload Complete")
        return True

    def upload_file_to_container(self, containername, filename, directory="/bootflash/"):
        self.create_container_if_doesnt_exist(containername)
        try:
            self.block_blob_service.create_blob_from_path(
                containername,
                filename,
                directory + filename,
                content_settings=ContentSettings(
                    content_encoding='UTF-8', content_language='en')
            )
        except Exception as e:
            print("Uploading %s Failed.  Error: %s" % (filename, e))
            return False

        print("Upload Complete to container %s" % (containername))
        return True

    def does_container_exist(self, containername):
        containers = self.block_blob_service.list_containers()

        for c in containers:
            if containername is c.name:
                return True
        return False
