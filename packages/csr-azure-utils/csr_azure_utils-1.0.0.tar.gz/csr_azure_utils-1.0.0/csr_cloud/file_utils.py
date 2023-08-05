#!/usr/bin/env python

'''
Cisco Copyright 2018
Author: Vamsi Kalapala <vakalapa@cisco.com>

FILENAME: AZURESTORAGE.PY


'''
from azure.storage.file import FileService
import json
import logging


'''
https://azure-storage.readthedocs.io/en/latest/ref/azure.storage.file.fileservice.html

'''


class StorageFileUtils():
    def __init__(self, account_name, account_key, cloudname, feature=None):
        self.feature = feature if feature is not None else __name__
        self.log = logging.getLogger(self.feature)
        if cloudname == 'azuregov':
            endpoint = 'core.usgovcloudapi.net'
        elif cloudname == 'azurechina':
            endpoint = 'core.chinacloudapi.cn'
        else:
            endpoint = 'core.windows.net'
        self.azure_file_service = FileService(
            account_name=account_name, account_key=account_key,  endpoint_suffix=endpoint)


    def get_file_contents(self, file_share, folder, file_name):
        is_file = self.azure_file_service.exists(
            file_share, directory_name=folder, file_name=file_name)
        if is_file:
            filedata = self.azure_file_service.get_file_to_text(
                file_share, folder, file_name)
            self.log.info(filedata.content)
            # filedata_json =  json.loads(filedata.content)
            return filedata.content
        else:
            return None

    def file_exists(self, file_share, folder, file_name):
        return self.azure_file_service.exists(
            file_share, directory_name=folder, file_name=file_name)

    def create_directory(self, file_share, folder):
        try:
            self.azure_file_service.create_directory(file_share, folder)
            return True
        except Exception as e:
            self.log.exception("Failed to create directory in storage: %s" % str(e))
            return False

    def create_share(self, file_share):
        try:
            self.azure_file_service.create_share(file_share)
            return True
        except Exception as e:
            self.log.exception("Failed to create file share: %s" % str(e))
            return False

    def get_list_directories_and_files(self, file_share, folder=None):
        try:
            result_generator = self.azure_file_service.list_directories_and_files(
                file_share, folder)
            contents_dict = []
            for item in result_generator:
                item_dict = {
                    'name': item.name,
                    'type': type(item).__name__
                }
                contents_dict.append(item_dict)
            return contents_dict
        except Exception as e:
            self.log.exception("Downloading files failed Error: %s" % str(e))
            return False

    def write_file_contents(
            self,
            file_share,
            folder,
            file_name,
            file_contents):
        if not self.create_share(file_share):
            self.log.error("[File_Utils] Could not complete writing all the files. Illegal Transit VNET name used.")
            return False
        if not self.create_directory(file_share, folder):
            self.log.error("[File_Utils] Could not complete writing all the files. Incorrect Directory name.")
            return False

        for k, v in file_contents.items():
            file_contents[k] = str(v)
        try:
            self.azure_file_service.create_file_from_text(
                file_share, folder, file_name, json.dumps(file_contents))
        except Exception as e:
            self.log.exception("Error occurred while writing the files to storage account: %s" % str(e))
            return False
        return True

    def copy_local_file_to_remote(self, file_share, folder, file_name, local_file_path):
        try:
            self.azure_file_service.create_file_from_path(share_name=file_share,
                                                          directory_name=folder, file_name=file_name,
                                                          local_file_path=local_file_path)
        except IOError:
            raise IOError("Invalid file path %s" % local_file_path)

    def get_file_contents_json(self, file_share, folder, file_name):
        try:
            output = self.get_file_contents(file_share, folder, file_name)
            if output is not None:
                return json.loads(output)
            else:
                return None
        except Exception as e:
            self.log.exception("Error getting file contents from storage: %s" % str(e))
            return None

    def get_file_to_path(self, share_name, directory_name, file_name, file_path):
        '''
        Download a file to a local file path
        '''
        try:
            self.azure_file_service.get_file_to_path(
                share_name,  # share name
                directory_name,  # directory path
                file_name,  # source file name
                file_path)
            return file_path
        except Exception as e:
            self.log.exception("Exception downloading file %s" % str(e))
            return None

