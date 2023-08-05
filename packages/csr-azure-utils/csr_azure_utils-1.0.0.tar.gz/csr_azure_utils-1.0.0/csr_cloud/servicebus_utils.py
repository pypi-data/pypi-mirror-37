'''
Cisco Copyright 2018
Author: Vishlesh Patel <vishlpa4@cisco.com>

FILENAME: SERVICEBUS_UTILS.PY
'''

from azure.servicebus.servicebusservice import ServiceBusService
from azure.servicebus import Message
import os
import logging
from azure.mgmt.eventhub.models import EHNamespace, Sku, SkuName, AccessRights, Eventhub, CaptureDescription
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.servicebus import ServiceBusManagementClient
import configparser
import datetime
import json

class ServiceBusUtils():
    def __init__(self, feature=None):
        self.feature = feature if feature is not None else __name__
        self.logger = logging.getLogger(self.feature)
        self.region = os.getenv('DEFAULT_REGION', "eastus")
        self.client_id = os.getenv("AZURE_CLIENT_ID", "")
        self.client_secret = os.getenv("AZURE_CLIENT_SECRET", "")
        self.subscription_id = os.getenv("SUBSCRIPTION_ID", "")
        self.tenant = os.getenv("TENANT_ID", "")
        self.customer_resource_group = os.getenv("CUSTOMER_RESOURCE_GROUP","")
        self.servicebus_client = self.get_servicebus_client()
        self.namespace = os.getenv("SERVICE_BUS_NAMESPACE_NAME", '')
        self.namespace_rule_name = os.getenv("SERVICE_BUS_NAMESPACE_ADMIN_AUTH_RULE_NAME", "")
        self.namespace_rule_key = os.getenv("SERVICE_BUS_NAMESPACE_ADMIN_AUTH_RULE_KEY", "")

    def load_env(self):
        try:
            config = configparser.ConfigParser()
            config.optionxform = str
            home = os.path.expanduser("~")
            filename = home + '/.azure/credentials'
            if not os.path.isfile(filename):
                raise Exception("credentials file do not exist. {}".format(filename))
            config.read(filename)
            for key in config['default']:
                value = config.get('default', key)
                value = value.strip("'").strip('"')
                os.environ[key] = str(value)
        except Exception as e:
            self.logger.exception(e)

    def get_servicebus_client(self):
        try:
            self.credentials = ServicePrincipalCredentials(
                client_id=self.client_id,
                secret=self.client_secret,
                tenant=self.tenant
            )
            servicebus_client = ServiceBusManagementClient(self.credentials, self.subscription_id)
            return servicebus_client
        except Exception as e:
            self.logger.exception(e)
            return None

    def create_namespace(self, namespace_name, rg=""):
        '''

        :return: creates an event hub resource and returns namespace object
        '''
        try:
            # Create a Namespace
            rg = self.customer_resource_group if rg == "" else rg
            namespaceparameter=EHNamespace(location=self.region,sku=Sku(name=SkuName.standard))
            poller = self.servicebus_client.namespaces.create_or_update(rg, namespace_name, namespaceparameter)
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
                Admin - Can do both manange, publish and listen
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
            if role.lower() == 'admin':
                accessRights.append(AccessRights('Manage'))
            createnamespaceauthorule = self.servicebus_client.namespaces.create_or_update_authorization_rule(rg,
                                       namespace_name, authoRule_name,
                                       accessRights)
            # List keys for the authorization rule
            listkeysauthorizationrule = self.servicebus_client.namespaces.list_keys(rg, namespace_name,
                                                                                  authoRule_name)
            return listkeysauthorizationrule
        except Exception as e:
            self.logger.exception(e)
            return None

    def create_subscription(self, subscription_name, topic_name, namespace, rule_name=None, rule_key=None):
        try:
            rule_name = self.namespace_rule_name if rule_name is None else rule_name
            rule_key = self.namespace_rule_key if rule_key is None else rule_key
            bus_service = ServiceBusService(service_namespace=namespace,
                                        shared_access_key_name=rule_name,
                                        shared_access_key_value=rule_key)
            bus_service.create_subscription(topic_name, subscription_name)
            return True
        except Exception as e:
            self.logger.warning("failed to create subscription for service bus topic")
            self.logger.exception(e)
            return False

    def create_topic(self, topic_name, namespace, rule_name=None, rule_key=None):
        try:
            rule_name = self.namespace_rule_name if rule_name is None else rule_name
            rule_key = self.namespace_rule_key if rule_key is None else rule_key
            bus_service = ServiceBusService(service_namespace=namespace,
                                        shared_access_key_name=rule_name,
                                        shared_access_key_value=rule_key)
            bus_service.create_topic(topic_name)
            return True
        except Exception as e:
            self.logger.warning("failed to create service bus topic")
            self.logger.exception(e)

    def delete_namespace(self, rg, namespace):
        try:
            deletenamespace = self.servicebus_client.namespaces.delete(rg, namespace).result()
            return True
        except Exception as e:
            self.logger.exception(e)
            return False

    def send_notification(
            self,
            topic_details,
            msg="",
            subject="",
            msgtype='string',
            message_attributes={}):
        '''
            :param topicarn: input format - "service bus namespace_name/ servicebus topic name"
            :param msg:
            :param subject:
            :param msgtype:
            :param message_attributes:
            :return:
        '''
        try:
            namespace, topic_name = topic_details.split("/")
            sbs = ServiceBusService(namespace, shared_access_key_name=self.namespace_rule_name,
                                    shared_access_key_value=self.namespace_rule_key)
            message_attributes = json.dumps(message_attributes)
            servicebus_msg = Message(message_attributes.encode('utf-8'))
            sbs.send_topic_message(topic_name, servicebus_msg)
            return True
        except Exception as e:
            self.logger.exception("topic details: {}, exception {}".format(topic_details, e))

if __name__ == "__main__":
    foo = ServiceBusUtils()
    #foo.create_namespace("testnamespace1jul6", "testservicebusutils")
    rule_name = 'admin'
    role = 'admin'
    keys = foo.create_authorization_rule("testnamespace1jul6", rule_name, role, "testservicebusutils")
    foo.namespace_rule_name = rule_name
    foo.namespace_rule_key = keys.primary_key
    foo.create_topic('testtopic', 'testnamespace1jul6')
    foo.create_subscription('autosubscription', 'testtopic', "testnamespace1jul6")
    now = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    msg = str({ "event": "scale_out", "pip" : "10.x.x.x" , "time": now })
    foo.send_notification("testnamespace1jul6/testtopic", message_attributes=msg)
