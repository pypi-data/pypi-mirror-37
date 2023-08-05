#!/bin/env python
'''
Cisco Copyright 2018
Author: Vishlesh Patel <vishlpa4@cisco.com>

FILENAME: EVENTHUB_UTILS.PY
'''

from azure.servicebus.servicebusservice import ServiceBusService
import os
import logging
from msrestazure.azure_exceptions import CloudError
import azure.mgmt.eventhub.models
from azure.mgmt.eventhub.models import EHNamespace, Sku, SkuName, AccessRights, Eventhub, CaptureDescription
from azure.mgmt.eventhub.models import ErrorResponseException, ErrorResponse, AuthorizationRule, AccessKeys, EncodingCaptureDescription, Destination
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.eventhub import EventHubManagementClient
import configparser

class EventHubUtils():
    def __init__(self, feature=None):
        self.feature = feature if feature is not None else __name__
        self.logger = logging.getLogger(self.feature)
        self.region = os.getenv('DEFAULT_REGION', "eastus")
        self.app_id = os.getenv("AZURE_CLIENT_ID", "")
        self.app_key = os.getenv("AZURE_CLIENT_SECRET", "")
        self.subscription_id = os.getenv("SUBSCRIPTION_ID", "")
        self.tenant = os.getenv("TENANT_ID", "")
        self.customer_resource_group = os.getenv("CUSTOMER_RESOURCE_GROUP","")
        self.eventhub_client = self.get_event_hub_client()
        self.eventhub_rule_name = os.getenv("EVENTHUB_PUBLISHER_AUTH_RULE_NAME", "publisherRule")
        self.eventhub_rule_key = os.getenv("EVENTHUB_PUBLISHER_AUTH_RULE_KEY", "zReduFf8ImU33lfaofcfb3DGjkzd+sHgIvuhlLKgi2o=")

    def load_env(self):
        try:
            config = configparser.ConfigParser()
            config.optionxform = str
            home = os.path.expanduser("~")
            filename = home + '/.azure/credentials'
            config.read(filename)
            for key in config['default']:
                value = config.get('default', key)
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                os.environ[key] = str(value)
        except Exception as e:
            self.logger.exception(e)

    def get_event_hub_client(self):
        try:
            self.credentials = ServicePrincipalCredentials(
                client_id=self.app_id,
                secret=self.app_key,
                tenant=self.tenant
            )
            eventhub_client = EventHubManagementClient(self.credentials, self.subscription_id)
            return eventhub_client
        except Exception as e:
            self.logger.exception(e)

    def create_namespace(self, namespace_name, rg=""):
        '''

        :return: creates an event hub resource and returns namespace object
        '''
        try:
            # Create a Namespace
            rg = self.customer_resource_group if rg == "" else rg
            namespaceparameter=EHNamespace(location=self.region,sku=Sku(name=SkuName.standard))
            poller = self.eventhub_client.namespaces.create_or_update(rg, namespace_name, namespaceparameter)
            creatednamespace = poller.result()
            self.logger.info("created a namespace - {} successfully.".format(namespace_name))
            return True
        except Exception as e:
            self.logger.exception(e)
            return False

    def create_authorization_rule(self,  namespace_name, rule_name, role="Publisher", rg=""):
        '''

        :param rg:
        :param namespace_name:
        :param rule_name: name or rule
        :param role: datatype - string.
                Publisher - can only send/publish event
                Listener - can only listen to events
                Admin - Can do both publish and listen
        :return:
                returns all keys for the rule.
                Accessible by using returned object.primary_key,
                                    returned object.secondary_key
                                    returned object.secondary_connection_string
                                    returned object.primary_connection_string
        '''
        try:
            # Create a new authorization rule
            authoRule_name = rule_name
            rg = self.customer_resource_group if rg == "" else rg
            role = str(role)
            accessRights = []
            if role.lower() == 'publisher' or role.lower() == 'admin':
                accessRights.append(AccessRights('Send'))
            if role.lower() == 'listener' or role.lower() == 'admin':
                accessRights.append(AccessRights('Listen'))
            createnamespaceauthorule = self.eventhub_client.namespaces.create_or_update_authorization_rule(rg,
                                       namespace_name, authoRule_name,
                                       accessRights)
            # List keys for the authorization rule
            listkeysauthorizationrule = self.eventhub_client.namespaces.list_keys(rg, namespace_name,
                                                                                  authoRule_name)
            return listkeysauthorizationrule
        except Exception as e:
            self.logger.exception(e)
            return None

    def create_event_hub_with_capture_feature(self, eventhub_name, rg, namespace, sa_resourece_id):
        try:
            # Create a Eventhub
            eventhubparameter = Eventhub(
                message_retention_in_days=4,
                partition_count=4,
                capture_description=CaptureDescription(
                    enabled=True,
                    encoding=EncodingCaptureDescription.avro,
                    interval_in_seconds=120,
                    size_limit_in_bytes=10485763,
                    destination=Destination(
                        name="EventHubArchive.AzureBlockBlob",
                        storage_account_resource_id=sa_resourece_id,
                        blob_container="container",
                        archive_name_format="{Namespace}/{EventHub}/{PartitionId}/{Year}-{Month}-{Day}-{Hour}-{Minute}-{Second}")
                )
            )
            createdeventhubresponse = self.eventhub_client.event_hubs.create_or_update(rg,
                                                                                       namespace, eventhub_name,
                                                                                       eventhubparameter)
            return True
        except Exception as e:
            self.logger.exception(e)
            return False

    def create_event_hub(self, eventhub_name, rg, namespace):
        try:
            # Create a Eventhub
            eventhubparameter = Eventhub(
                message_retention_in_days=4,
                partition_count=4
                )
            createdeventhubresponse = self.eventhub_client.event_hubs.create_or_update(rg,
                                                                                       namespace, eventhub_name,
                                                                                       eventhubparameter)
            return True
        except Exception as e:
            self.logger.exception(e)
            return False

    def delete_event_hub(self, eventhub_name, rg, namespace):
        try:
            geteventhubresponse = self.eventhub_client.event_hubs.delete(rg, namespace,
                                                                         eventhub_name)
            return True
        except Exception as e:
            self.logger.exception(e)
            return False

    def delete_namespace(self, rg, namespace):
        try:
            deletenamespace = self.eventhub_client.namespaces.delete(rg, namespace).result()
            return True
        except Exception as e:
            self.logger.exception(e)
            return False

    def send_notification(
            self,
            topicarn,
            msg="",
            subject="",
            msgtype='string',
            message_attributes={}):
        '''
            :param topicarn: input format - "eventhub_namespace_name/eventhub_name"
            :param msg:
            :param subject:
            :param msgtype:
            :param message_attributes:
            :return:
        '''
        try:
            namespace, eh_name = topicarn.split("/")
            sbs = ServiceBusService(namespace, shared_access_key_name=self.eventhub_rule_name,
                                    shared_access_key_value=self.eventhub_rule_key)
            sbs.send_event(eh_name, message_attributes)
            return True
        except Exception as e:
            self.logger.exception("topicarn: {}, exception: {}".format(topicarn, e))
            return False

if __name__ == "__main__":
    foo = EventHubUtils()
    foo.create_namespace("testnamespace1jun17", "rgeventhubjun17")
    keys = foo.create_authorization_rule("testnamespace1jun17", "listenerRole", "listener", "rgeventhubjun17")
    print(keys.primary_connection_string)
    sa_id = "/subscriptions/b7fd700c-0b05-44ba-823a-6e954c480149/resourcegroups/rgeventhubjun17/providers/Microsoft.Storage/storageAccounts/testeventhubjul17"
    foo.create_event_hub_with_capture_feature("eventhub1", "rgeventhubjun17", "testnamespace1jun17", sa_id)
    msg = str({ "event": "scale_out", "pip" : "10.x.x.x" })
    foo.send_notification("testnamespace1jun17/eventhub1", message_attributes=msg)
    #foo.create_event_hub("eventhub2", "rgeventhubjun17", "testnamespace1jun17")
