#!/bin/env python
import logging
from collections import namedtuple
import os
import json
import base64
import re
import string
from azure.storage.file import FileService
from azure.storage.cloudstorageaccount import CloudStorageAccount
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from metric_utils import MetricUtils
from haikunator import Haikunator
from azure.servicebus.servicebusservice import ServiceBusService
from servicebus_utils import ServiceBusUtils
import configparser
from shutil import copyfile
# Documentation:
# https://media.readthedocs.org/pdf/azure-sdk-for-python/latest/azure-sdk-for-python.pdf

logger = logging.getLogger('autoscaler.' + __name__)
logger.setLevel(logging.DEBUG)


class as_cloud():
    def __init__(self):
        self.logger = logger
        self.azure_dir = os.path.expanduser('~') + '/.azure'
        self.credentials_file_path = self.azure_dir + '/credentials'
        self.storage_acct_name = os.getenv("AZURE_STORAGE_NAME", "")
        self.storage_acct_key = os.getenv("AZURE_STORAGE_KEY", "")
        self.storage_prefix = self.get_storage_prefix()
        self.fileshare = self.storage_prefix.split('/')[0]
        self.directory = self.storage_prefix.split('/')[1]
        self.setup_autoscaler_env()
        self.region = os.getenv('DEFAULT_REGION', "eastus")
        self.app_id = os.getenv("AZURE_CLIENT_ID", "")
        self.app_key = os.getenv("AZURE_CLIENT_SECRET", "")
        self.subscription_id = os.getenv("SUBSCRIPTION_ID", "")
        self.tenant = os.getenv("TENANT_ID", "")
        self.credentials = ServicePrincipalCredentials(
            client_id=self.app_id,
            secret=self.app_key,
            tenant=self.tenant
        )
        self.Results = namedtuple('Results', 'min, max, avg, cnt, inst')
        self.privatekey_prefix = "AutoScaler/privatekeys"
        self.azure_file_service = FileService(
            account_name=self.storage_acct_name, account_key=self.storage_acct_key)
        self.network_client = NetworkManagementClient(
            self.credentials, self.subscription_id)
        self.compute_client = ComputeManagementClient(self.credentials, self.subscription_id)
        self.customer_resource_group = os.getenv("CUSTOMER_RESOURCE_GROUP", "")
        self.eventhub_rule_name = os.getenv("EVENTHUB_PUBLISHER_AUTH_RULE_NAME", "")
        self.eventhub_rule_key = os.getenv("EVENTHUB_PUBLISHER_AUTH_RULE_KEY",
                                           "")

        self.servicebus_utils = None
        self.metric_utils = None

    def setup_autoscaler_env(self):
        try:
            if not os.path.isfile(self.credentials_file_path):
                if not os.path.exists(self.azure_dir):
                    os.mkdir(self.azure_dir)
                    self.logger.info("{} created".format(self.azure_dir))
                self.get_file(self.storage_acct_name, 'AutoScaler', 'credentials', self.fileshare)
                copyfile('/tmp/credentials', self.credentials_file_path)
            self.load_env()
            return True
        except Exception as e:
            self.logger.exception(e)
            return False

    def load_env(self):
        try:
            config = configparser.ConfigParser()
            config.optionxform = str
            filename = self.credentials_file_path
            if not os.path.isfile(filename):
                raise Exception("credentials file do not exist. {}".format(filename))
            config.read(filename)
            for key in config['default']:
                value = config.get('default', key)
                value = value.strip("'").strip('"')
                os.environ[key] = str(value)
        except Exception as e:
            self.logger.exception(e)

    def get_transit_network_filename(self):
        return "transit_vnet_config.txt"

    def get_storage_prefix(self):
        if 'AZURE_STORAGE_PREFIX' in os.environ:
            vpnconfig_prefix = os.environ['AZURE_STORAGE_PREFIX']
        else:
            vpnconfig_prefix = "tvnetname/config"
        return vpnconfig_prefix

    def get_rg_name_from_instance_id(self, instance_id):
        '''

        :param instance_id (str): Long Instance ID of Azure VM.
        :return: rg (str): RG name of VM
        '''
        rg = None
        try:
            if instance_id is None or len(instance_id) <= 4:
                logger.warning("bad instance id : {}".format(instance_id))
            rg = instance_id.split('/')[4]
        except Exception as e:
            logger.exception(e)
        return rg

    def get_vm_name_from_instance_id(self, instance_id):
        '''

        :param instance_id (str): Long Instance ID of Azure VM
        :return: vm_name (str)
        '''
        vm_name = None
        try:
            if instance_id is None:
                logger.warning("bad instance id : {}".format(instance_id))
            vm_name = instance_id.split('/')[-1]
        except Exception as e:
            logger.exception(e)
        return vm_name

    def get_short_instance_id(self, instance_id):
        '''

        :param instance_id: This is an Azure's long Instance ID.
               sample: /subscriptions/69ff3a41-a66a-4d31-8c7d-9a1ef44595c3/resourceGroups/RGTVNETAUTOSCALER/
               providers/Microsoft.Compute/virtualMachines/csrtvnet-1
        :return: uuid (str) : Short instance ID
               sample: 4e97b40a-0770-4096-80b7-edada2853d9c
        '''
        try:
            rg = self.get_rg_name_from_instance_id(instance_id)
            vm_name = self.get_vm_name_from_instance_id(instance_id)
            vm = self.compute_client.virtual_machines.get(rg, vm_name)
            uuid = str(vm.vm_id)
            return uuid
        except Exception as e:
            logger.error(e)
        return None

    def get_rg_vmname_combo_id(self, instance_id):
        '''
        :param instance_id - this is an Azure's long instance id.
            sample: /subscriptions/69ff3a41-a66a-4d31-8c7d-9a1ef44595c3/resourceGroups/RGTVNETAUTOSCALER/
               providers/Microsoft.Compute/virtualMachines/csrtvnet-1
        :return: returns combination of rg and vmname <RG>-<vmname>
        '''
        try:
            rg = self.get_rg_name_from_instance_id(instance_id)
            vm_name = self.get_vm_name_from_instance_id(instance_id)
            id = "{}-{}".format(str(rg).lower(), str(vm_name).lower())
            return id
        except Exception as e:
            logger.error(e)
        return None

    def get_as_private_key_files_info(self, instance_id):
        '''
        This method returns transit network solutions' private key files location information
        :param instance_id (str): Azure's long instance id
        :return: key_tuple (tuple object) - ( private key directory path, file name)
        '''
        try:
            id = self.get_rg_vmname_combo_id(instance_id)
            return (self.privatekey_prefix, id + '.pem')
        except Exception as e:
            logger.error(e)
        return None

    def get_tnet_private_key_files_info(self, instance_id):
        '''
        This method returns Autoscaler solutions' private key files location information
        :param instance_id (str):
        :return: key_tuple (tuple object) - ( private key directory path, file name)
        '''
        try:
            rg = self.get_rg_name_from_instance_id(instance_id)
            vm_name = self.get_vm_name_from_instance_id(instance_id)
            vm = self.compute_client.virtual_machines.get(rg, vm_name)
            uuid = str(vm.vm_id)
            return ('config/privatekeys', uuid + '.pem')
        except Exception as e:
            logger.error(e)
        return None

    def get_file_contents(self, file_share, directory, file_name):
        is_file = self.azure_file_service.exists(
            file_share, directory_name=directory, file_name=file_name)
        if is_file:
            filedata = self.azure_file_service.get_file_to_text(
                file_share, directory, file_name)
            return filedata.content
        else:
            return None

    def get_file(self, storage_name, directory, filename, fileshare=None):
        if fileshare is None:
            fileshare = self.fileshare
        account = CloudStorageAccount(storage_name, self.storage_acct_key)
        file_service = account.create_file_service()
        destination_file = '/tmp/' + filename
        try:
            if directory[-1] == '/':
                # Prevent from Azure API failure
                directory = directory[:-1]
            file_service.get_file_to_path(
                fileshare,  # share name
                directory,  # directory path
                filename,  # source file name
                destination_file)  # destination path with name
            return True
        except Exception as e:
            logger.warning("{} file not found in dir {} of storage name {}".format(filename,
                                                                                   directory,
                                                                                   storage_name))
            pass
        return None

    def put_file(self, status, storage_name, directory, filename, fileshare=None):
        if fileshare is None:
            fileshare = self.fileshare
        account = CloudStorageAccount(storage_name, self.storage_acct_key)
        file_service = account.create_file_service()
        source_file = '/tmp/' + filename
        try:
            directory = directory.rstrip("/")
            file_service.create_directory(fileshare, directory)
            file_service.create_file_from_path(
                fileshare,  # share name
                directory,  # directory path
                filename,  # destination file name
                source_file)  # source path with name
        except Exception as e:
            logger.exception("received error putting file. fileshare {}, directory {}, filename {}, error {}".format(
                fileshare, directory, filename, e))
            pass

    '''
        Returns the transit network config. If not exist, create one.
    '''

    def get_transit_network_config(self, storage_name, config_filename):
        vpnconfig_prefix = self.get_storage_prefix()
        self.logger.info("storage_name: %s" % storage_name)
        self.logger.info("vpnconfig_prefix: %s" % vpnconfig_prefix)
        self.logger.info("config_filename: %s" % config_filename)
        # try to retrieve the Transit network config file - transit_vpc_config.txt
        for i in range(5):
            try:
                config = json.loads(self.get_file_contents(self.fileshare, self.directory, config_filename))
            except Exception as e:
                self.logger.warning("Exception while getting vpc config: %s" % e)
                config = None
                continue
        if config is None:
            logger.info("Config file : {} not found".format(config_filename))
            config = self.create_transit_network_config(storage_name, config_filename)
        return config

    def create_transit_network_config(self, storage_name, config_filename):
        self.logger.info("storage_name: %s" % storage_name)
        self.logger.info("vpnconfig_prefix: %s" % self.storage_prefix)
        self.logger.info("config_filename: %s" % config_filename)
        fileshare, directory = self.fileshare, self.directory

        # build transit network config file
        dmvpn_json = json.loads(self.get_file_contents(fileshare, directory, "dmvpn.json"))
        hub1_json = json.loads(self.get_file_contents(fileshare, directory, "hub1.json"))
        hub2_json = json.loads(self.get_file_contents(fileshare, directory, "hub2.json"))
        logger.info("received dmvpn, hub1, hub2.json")

        transit_network_config_dict = {}
        transit_network_config_dict = self.fill_up_tnet_config(transit_network_config_dict,
                                                               dmvpn_json, hub1_json, hub2_json)
        logger.info("transit_network_config_dict {}".format(transit_network_config_dict))
        with open('/tmp/' + config_filename, 'w') as fp:
            json.dump(transit_network_config_dict, fp, sort_keys=True, indent=4)
        logger.info("transit_network_config_dict {}".format(transit_network_config_dict))
        self.put_file(None, storage_name, directory, config_filename)
        return json.loads(transit_network_config_dict)

    def fill_up_tnet_config(self, transit_network_config_dict, dmvpn_json, hub1_json, hub2_json):
        transit_network_config_dict['EIP1'] = hub1_json['pip']
        transit_network_config_dict['EIP2'] = hub2_json['pip']
        if dmvpn_json['RoutingProtocol'] == 'BGP':
            transit_network_config_dict['BGP_ASN'] = dmvpn_json['RoutingProtocolASN']
        else:
            transit_network_config_dict['BGP_ASN'] = ''

        transit_network_config_dict['APP_ID'] = self.app_id
        transit_network_config_dict['APP_KEY'] = self.app_key
        return transit_network_config_dict

    def put_transit_network_Config(self, status, storage_name, config_file, config):

        self.logger.info(
            "Uploading new config file: %s/%s/%s/%s",
            storage_name,
            self.fileshare,
            self.directory,
            config_file)

        tmp_file_loc = "/tmp/" + config_file
        self.logger.debug("writing transit network config to tmp location: {}".format(tmp_file_loc))
        with open(tmp_file_loc, "w") as text_file:
            text_file.write(json.dumps(config))
        self.put_file(None, storage_name, self.directory, config_file)

    def get_private_ip_from_instance_id(self, instance_id):
        try:
            logger.info("Getting Private IP for Instance ID : {}".format(instance_id))

            rg = self.get_rg_name_from_instance_id(instance_id)
            vmname = self.get_vm_name_from_instance_id(instance_id)
            vm = self.compute_client.virtual_machines.get(rg, vmname)
            for ni_reference in vm.network_profile.network_interfaces:
                ni_reference = ni_reference.id.split('/')
                ni_name = ni_reference[8]
                net_interface = self.network_client.network_interfaces.get(rg, ni_name)
                if net_interface.ip_configurations[0].private_ip_address:
                    return net_interface.ip_configurations[0].private_ip_address
        except Exception as e:
            self.logger.warning("Exception while looking up ip address: %s" % e)
            return None

    '''
    # Given the VM unique ID, this method returns rg name of instance
    '''

    def get_instance_rg_name(self, instance_id):
        try:
            logger.info("Getting RG name for instance with ID : {}".format(instance_id))
            for vm in self.compute_client.virtual_machines.list_all():
                vm_id = vm.vm_id
                if str(vm_id) == str(instance_id):
                    vm_id_ref = vm.id
                    rg_from_vm = self.get_rg_name_from_instance_id(vm_id_ref)
                    return rg_from_vm
        except Exception as e:
            self.logger.warning("Exception while looking up RG name: %s" % e)
            return None

    '''
    # Given the VM unique ID, this method returns VM name
    '''
    def get_instance_name(self, instance_id):
        try:
            logger.info("Getting Instance name for instance with ID : {}".format(instance_id))
            for vm in self.compute_client.virtual_machines.list_all():
                vm_id = vm.vm_id
                if str(vm_id) == str(instance_id):
                    vm_id_ref = vm.id
                    instance_name = self.get_vm_name_from_instance_id(vm_id_ref)
                    return instance_name
        except Exception as e:
            self.logger.warning("Exception while looking up RG name: %s" % e)
            return None

    def get_instanceId_from_ip(self, public_ip_address):
        try:
            logger.info("Getting Instance ID for Public ip : {}".format(public_ip_address))
            for public_ip in self.network_client.public_ip_addresses.list_all():
                if public_ip.ip_address == public_ip_address:
                    # Get id of public IP
                    pip_id = public_ip.id.split('/')
                    rg_from_pip = pip_id[4].lower()
                    pip_name = pip_id[-1]

            for vm in self.compute_client.virtual_machines.list_all():
                rg_from_vm = self.get_rg_name_from_instance_id(vm.id).lower()
                if rg_from_pip == rg_from_vm:
                    for ni_reference in vm.network_profile.network_interfaces:
                        ni_reference = ni_reference.id.split('/')
                        ni_name = ni_reference[8]
                        net_interface = self.network_client.network_interfaces.get(rg_from_pip, ni_name)
                        public_ip_reference = net_interface.ip_configurations[0].public_ip_address
                        if public_ip_reference:
                            public_ip_reference = public_ip_reference.id.split('/')
                            ip_name = public_ip_reference[8]
                            if ip_name == pip_name:
                                return str(vm.id)
        except Exception as e:
            self.logger.warning("Exception while looking up ip address: %s" % e)
            return None

    def get_private_key(self, storage_name, prikey):
        return True

    def put_private_key(self, status, storage_name, instance_id, prikey):
        id = self.get_rg_vmname_combo_id(instance_id)
        instance_private_key_filename = id + '.pem'
        tmp_file_loc = "/tmp/" + instance_private_key_filename
        self.logger.debug("writing prikey to {}".format(tmp_file_loc))
        with open(tmp_file_loc, "w") as text_file:
            text_file.write(prikey)

        self.logger.debug(
            "Uploading private key: %s/%s/%s/%s",
            storage_name,
            self.privatekey_prefix,
            instance_id,
            instance_private_key_filename)

        self.put_file(None, storage_name, self.privatekey_prefix, instance_private_key_filename)

    def get_instance_config_filename(self, instance_id):
        instance_name = self.get_rg_vmname_combo_id(instance_id)
        return "%s.cfg" % instance_name

    def copy_file(self, status, storage_name, directory, from_file, to_file,
                  fileshare=None):
        try:
            if fileshare is None:
                fileshare = self.fileshare
            is_file = self.azure_file_service.exists(
                fileshare, directory_name=directory, file_name=from_file)
            if is_file:
                url = self.azure_file_service.make_file_url(fileshare, directory, from_file)
                # create directory if not exist
                self.azure_file_service.create_directory(fileshare, directory)
                self.azure_file_service.copy_file(fileshare, directory, to_file, url)
            else:
                self.logger.error("no file named {} exist. storage_name {}".format(from_file, storage_name))
                return False
            return True
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False

    def copy_file_from_to_dir(self, storage_name, from_dir, from_file,
                              to_dir, to_file, fileshare=None):
        try:
            if fileshare is None:
                fileshare = self.fileshare
            from_file_exist = self.azure_file_service.exists(
                fileshare, directory_name=from_dir, file_name=from_file)
            if from_file_exist:
                url = self.azure_file_service.make_file_url(fileshare, from_dir, from_file)
            else:
                logger.exception("no file named {} exist. storage_name {}".format(from_file, storage_name))
                return False
            # create directory if not exist
            self.azure_file_service.create_directory(fileshare, to_dir)
            self.azure_file_service.copy_file(fileshare, str(to_dir), str(to_file), url)
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False
        logger.info("Success copying file from dir {} file {} to dir {} file {}".format(from_dir, from_file, to_dir, to_file))
        return True

    def copy_private_key(self, status, storage_name, from_file, to_file):
        return self.copy_file_from_to_dir(storage_name, self.privatekey_prefix, from_file, self.privatekey_prefix, to_file)


    def copy_original_privateKey(self, status, storage_name, from_file, to_file):
        return self.copy_file_from_to_dir(storage_name, 'config/privatekeys', from_file, self.privatekey_prefix, to_file)

    def save_original_privateKey(self, status, storage_name, from_file, to_file):
        # this API depends on from_file variable which expected to be of form - "vm-uuid.pem"
        return self.copy_file_from_to_dir(storage_name, self.privatekey_prefix, from_file, 'config/privatekeys', to_file)

    def associate_role_to_instance(self, instance_id, role):
        return True

    def set_instance_tags(self, cfg, instance_id, name):
        try:
            rg = self.get_rg_name_from_instance_id(instance_id)
            vmname = self.get_vm_name_from_instance_id(instance_id)
            vm = self.compute_client.virtual_machines.get(rg, vmname)
            as_group_name = cfg.get_as_group_name()
            as_storage_name = cfg.get_storage_name()
            vm.tags = {
                "Name": name,
                "AutoScaleGroup": as_group_name,
                "storage_name": as_storage_name
            }
            self.compute_client.virtual_machines.create_or_update(rg, vmname, vm)
        except Exception as e:
            self.logger.warning(
                "Failed to set label on instance %s to %s (%s)" %
                (instance_id, name, e))

    def is_instance_ready(self, instance_id):
        # TODO: Change this to achieve concrete readiness. Ping test? / SSH test?
        return self.is_instance_running(instance_id)

    def is_instance_running(self, instance_id):
        rg = self.get_rg_name_from_instance_id(instance_id)
        vmname = self.get_vm_name_from_instance_id(instance_id)
        try:
            vm = self.compute_client.virtual_machines.get(rg, vmname, expand='instanceView')
            status = vm.instance_view.statuses[1].display_status
            logger.info("instance id: {}, status: {}".format(instance_id, status))
            status = status.split()[-1]
            if status.lower() == 'running':
                return True
        except Exception as e:
            logger.error(e)
        return False

    def get_running_state(self, instance_id):
        rg = self.get_rg_name_from_instance_id(instance_id)
        vmname = self.get_vm_name_from_instance_id(instance_id)
        try:
            vm = self.compute_client.virtual_machines.get(rg, vmname, expand='instanceView')
            status = vm.instance_view.statuses[1].display_status.lower()
            logger.info("instace id: {}, status: {}".format(instance_id, status))
            if "stop" in status:
                logger.info("return value: stopped")
                return "stopped"
            if "terminat" in status or "delet" in status:
                logger.info("return value: terminated")
                return "terminated"
            status = status.split()[-1]
            logger.info("return value: {}".format(status))
            return status
        except Exception as e:
            logger.error(e)
            logger.info("return value: terminated")
            return "terminated"

    def get_reachability_status(self, instance_id):
        # TODO: change this to more robust reachability check
        if self.is_instance_running(instance_id):
            return "Passed"
        else:
            return "Failed"

    def does_file_exist(self, storage_name, filename, directory=None, fileshare=None):
        try:
            if fileshare is None:
                fileshare = self.fileshare
            if directory is None:
                directory = 'AutoScaler'
            return self.azure_file_service.exists(fileshare, directory, filename)
        except Exception as e:
            self.logger.info("Exception: %s" % e)
            return False

    def get_metric(
            self,
            name,
            instance_id,
            period,
            metric_period,
            metric_type,
            namespace):
        try:
            if self.metric_utils is None:
                self.metric_utils = MetricUtils('autoscaler')
            vm_name = self.get_vm_name_from_instance_id(instance_id)
            rg = self.get_rg_name_from_instance_id(instance_id)
            instance_id = self.get_rg_vmname_combo_id(instance_id)
            dimensions = {
                "InstanceId": instance_id
            }

            if metric_type.lower() == 'avg':
                metric_type = 'avg'
            elif metric_type.lower() == 'sum':
                metric_type = 'sum'
            else:
                metric_type = 'max'

            if namespace == "csr1000v":
                mylist = self.metric_utils.get_custom_metric(name, 'customMetrics',
                                                             period, metric_period,
                                                             metric_type, dimensions)
            else:
                resource_id = (
                    "subscriptions/{}/"
                    "resourceGroups/{}/"
                    "providers/Microsoft.Compute/virtualMachines/{}"
                ).format(self.subscription_id, rg, vm_name)

                mylist = self.metric_utils.get_azure_metric(name, period, metric_period, metric_type, resource_id)

            if metric_type == 'sum':
                for i in range(len(mylist)):
                    mylist[i] = (mylist[i][0], mylist[i][1], mylist[i][2]/metric_period)

            if len(mylist):
                results = sorted(mylist, key=lambda x: x[0])
                name, min_time, min_value = min(
                    results, key=lambda item: item[2])
                name, max_time, max_value = max(
                    results, key=lambda item: item[2])
                avg_value = (sum(x[2] for x in results) / len(mylist))
                self.logger.debug("%s (%s) => %s/%s/%s" % (instance_id, name, min_value, max_value, avg_value))

                result = self.Results(
                    min=min_value,
                    max=max_value,
                    avg=avg_value,
                    cnt=len(mylist),
                    inst=instance_id)
                return result
            else:
                self.logger.warning("retrieved empty metric list for metric name: {}, instance id: {}, namespace: {}".format(
                                    name, instance_id, namespace
                ))
        except Exception as e:
            self.logger.exception(e)

    def put_metric(self, name, description, group_name):
        try:
            if self.metric_utils is None:
                self.metric_utils = MetricUtils('autoscaler')
            dimensions = {
                "Namespace": "csr1000v",
                "AutoScaleGroup": group_name,
                "Action": description
            }
            self.metric_utils.put_metric(name, value=1, dimensions=dimensions)
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
            :param topicarn: input format - "eventhub_namespace_name/eventhub_name"
            :param msg:
            :param subject:
            :param msgtype:
            :param message_attributes:
            :return:
        '''
        try:
            if self.servicebus_utils is None:
                self.servicebus_utils = ServiceBusUtils('autoscaler')
            self.servicebus_utils.send_notification(topic_details=topic_details,
                                                    message_attributes=message_attributes)
            return True
        except Exception as e:
            self.logger.exception(e)
            return False

    def send_user_notification(self, cloud_config,
                               msg="",
                               subject="",
                               msgtype='string',
                               message_attributes={}):
        try:
            if 'EH Details' in cloud_config:
                eh_details = cloud_config['EH Details']
            else:
                raise Exception("No EH Details found in cloud config")
            logger.info("Sending user notification to event hub : {}".format(eh_details))
            namespace, eh_name = eh_details.split("/")
            sbs = ServiceBusService(namespace, shared_access_key_name=self.eventhub_rule_name,
                                    shared_access_key_value=self.eventhub_rule_key)
            sbs.send_event(eh_name, message_attributes)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def put_rule(self, arn, minutes):
        '''
        response = self.events_client.list_rule_names_by_target(
            TargetArn=arn,
        )
        for rule_name in response['RuleNames']:
            name = rule_name
            break
        if minutes > 1:
            frequency = "rate(%d minutes)" % int(minutes)
        else:
            frequency = "rate(%d minute)" % int(minutes)

            self.logger.info("frequency: %s" % frequency)
        try:
            rule_response = self.events_client.put_rule(
                Name=name,
                ScheduleExpression=frequency,
                State='ENABLED',
            )
            self.logger.info("%s" % rule_response)
        except Exception as e:
            self.logger.warning("Exception putting rule: %s" % e)
        '''
        return

    def get_rule_minutes(self, arn):
        '''
        response = self.events_client.list_rule_names_by_target(
            TargetArn=arn,
        )
        for rule_name in response['RuleNames']:
            name = rule_name
            break

        try:
            rule_response = self.events_client.describe_rule(
                Name=name
            )
            self.logger.info("%s" % rule_response)
        except Exception as e:
            self.logger.warning("Exception getting rule: %s" % e)
            return 999

        expression = rule_response['ScheduleExpression']
        numbers = re.findall(r'\d+', expression)
        print numbers
        return int(numbers[0])
        '''
        return

    def get_cloud_cfg_subset(self, instance_id, default_cfg=None):
        cloud_config = default_cfg if default_cfg else {}
        subnet_list = []
        sec_group_list = []
        # in Azure, Transit VNet deploys CSR in Availability sets. as_set will hold availability set info
        as_list = []
        private_ip = ""
        public_ip = ""
        try:

            rg = self.get_rg_name_from_instance_id(instance_id)
            vmname = self.get_vm_name_from_instance_id(instance_id)

            i = self.compute_client.virtual_machines.get(rg, vmname, expand='instanceView')
            if i is None:
                self.logger.warning("No instance found with instance id %s" % (instance_id))
            if i.availability_set and i.availability_set.id:
                avset_name = i.availability_set.id.split('/')[-1]
                as_list.append(avset_name)
            else:
                logger.warning("av set not found for instance id : {}".format(instance_id))
            for idx, nic in enumerate(i.network_profile.network_interfaces):
                nic_name = nic.id.split('/')[-1]
                nic = self.network_client.network_interfaces.get(rg, nic_name)
                if nic.ip_configurations and len(nic.ip_configurations) > 0:
                    # Assumption: NIC can be associated with only one subnet.
                    if nic.ip_configurations[0].subnet and nic.ip_configurations[0].subnet.id:
                        subnet_list.append(nic.ip_configurations[0].subnet.id)
                    else:
                        logger.warning("No subnets associated with nic: {}".format(nic_name))
                else:
                    logger.warning("Could not find ip configuration for nic {}".format(nic_name))
                if idx == 0:
                    private_ip = nic.ip_configurations[0].private_ip_address
                    public_ip_name = nic.ip_configurations[0].public_ip_address.id.split('/')[-1]
                    pip_ref = self.network_client.public_ip_addresses.get(rg, public_ip_name)
                    public_ip = pip_ref.ip_address

            async_poller = self.network_client.network_interfaces.list_effective_network_security_groups(rg, nic_name)
            sg_list = async_poller.result()
            # sample sg id = "/subscriptions/69ff3a41-a66a-4d31-8c7d-9a1ef44595c3/resourceGroups/rgtvnetAutoscaler/providers/Microsoft.Network/networkSecurityGroups/csrtvnet-SSH-SecurityGroup"
            for sg_id in sg_list.value:
                sec_group_list.append(sg_id.id)

            cloud_config["instance_type"] = i.hardware_profile.vm_size
            # Agnostifying the term - "ami-id" to image-Id.
            # Please keep in mind that in AWS image-id == "ami-id" and
            # in Azure image-id == "sku-id"
            if i.storage_profile.__dict__['image_reference']:
                cloud_config["image-id"] = i.storage_profile.image_reference.sku
                cloud_config["image-version"] = i.storage_profile.image_reference.version
            cloud_config["as_list"] = as_list
            cloud_config["subnet_id"] = subnet_list
            cloud_config["security_groups"] = sec_group_list
            # Azure does not have instance profile. There profile will be set to - azure_instance_profile as stub
            cloud_config["iam_instance_profile"] = "azure_instance_profile"

            cloud_config["public_ip_address"] = public_ip
            cloud_config["private_ip_address"] = private_ip
            cloud_config["resource_group"] = rg
            self.logger.debug(
                "Instance %s config =\n %s\n" %
                (instance_id, cloud_config))
            return cloud_config
        except Exception as e:
            self.logger.warning("Failed to get config for %s (%s)" % (instance_id, e))
            return cloud_config

    def get_cloud_config(self, instance_id):
        return self.get_cloud_cfg_subset(instance_id)

    def get_ip_allocation_id(self, instance_id):
        '''
        config = self.get_cloud_config(instance_id)
        ip_address = config["public_ip_address"]

        response = self.ec2_client.describe_addresses(
            PublicIps=[
                ip_address
            ],
        )
        return response["Addresses"][0]['AllocationId']
        '''
        return

    def reserve_ip(self, name=None):
        try:
            elastic_ip_name = self.customer_resource_group + '-' + name + 'pip'
            public_ip_parameters = {
                'location': self.region,
                'public_ip_allocation_method': 'static',
                'dns_settings': {
                    'domain_name_label': (elastic_ip_name + '-dns').lower()
                },
                'idle_timeout_in_minutes': 30
            }
            async_publicip_creation = self.network_client.public_ip_addresses.create_or_update(
                self.customer_resource_group,
                elastic_ip_name,
                public_ip_parameters
            )
            public_ip_info = async_publicip_creation.result()
            elastic_ip = public_ip_info.__dict__['ip_address']
            allocation_id = public_ip_info.__dict__['id']
        except Exception as e:
            self.logger.info("Elastic IP was not created, Error: %s ", e)
            elastic_ip = None
            allocation_id = None
        return elastic_ip, allocation_id

    def associate_ip(self, instance_id, allocationId):
        '''
        response = self.ec2_client.associate_address(
            InstanceId=instance_id,
            AllocationId=allocationId)
        '''
        ip_name = allocationId.split('/')[-1]
        vm_name = self.get_vm_name_from_instance_id(instance_id)
        self.logger.info(
            "Ip %s has already been associated with virtual machine during Nic creation %s" % (ip_name, vm_name))
        return

    def release_ip(self, instance_id):
        url = instance_id.split('/')
        instance_name = url.pop()
        elastic_ip_name = self.customer_resource_group + '-' + instance_name + 'pip'
        try:
            delete_ip = self.network_client.public_ip_addresses.delete(self.customer_resource_group, elastic_ip_name)
            delete_ip.wait()
            self.logger.info("Deleted public IP %s" % elastic_ip_name)
        except Exception as e:
            self.logger.exception("Exception in releasing IP %s : %s" % (elastic_ip_name, e))
            pass

    def create_network_interface(self, interface_name, subnet_id, security_group_id=None, pip_id=None):
        nic_params = {
            'location': self.region,
            'enable_ip_forwarding': True,
            'ip_configurations': [
                {
                    'name': 'IP_CONFIG_NAME',
                    'subnet': {
                        'id': subnet_id
                    }
                },
            ]
        }

        if security_group_id:
            nic_params['network_security_group'] = {
                'id': security_group_id
            }
        if pip_id:
            nic_params['ip_configurations'][0]['public_ip_address'] = {'id': pip_id}

        try:
            self.network_client.network_interfaces.create_or_update(self.customer_resource_group, interface_name,
                                                                    nic_params)
            result = self.network_client.network_interfaces.get(self.customer_resource_group, interface_name)
            return result.id
        except Exception as e:
            self.logger.exception("Exception during creation of network interface is %s" % e)
            return None

    def create_vm_parameters(self, vmname, location, uname, password, nic_id_1, nic_id_2, strg_acc_name, sku, vm_size,
                             custom_data, boot_diag, boot_diag_sa, image_uri, av_set_id=None):
        """Create the VM parameters structure.
        """
        haikunator = Haikunator()
        vm_reference = {
            'publisher': 'cisco',
            'offer': 'cisco-csr-1000v',
            'sku': sku,
            'version': None
        }
        os_disk_name = vmname + haikunator.haikunate()
        vm_params = {}
        vm_params['location'] = location
        vm_params['os_profile'] = {
            'computer_name': vmname,
            'admin_username': uname,
            'admin_password': password,
            'custom_data': base64.b64encode(custom_data)
        }
        vm_params['hardware_profile'] = {
            'vm_size': vm_size
        }

        # vm_params['plan'] = {
        #     'name': vm_reference['sku'],
        #     'publisher': vm_reference['publisher'],
        #     'product': vm_reference['offer']
        # }
        vm_params['network_profile'] = {
            'network_interfaces': [{
                'id': nic_id_1,
                'primary': True
            }, {
                'id': nic_id_2,
                'primary': False
            }]
        }
        vm_params['diagnostics_profile'] = {
            'boot_diagnostics': {
                'enabled': boot_diag,
                'storage_uri': boot_diag_sa
            }
        }
        if av_set_id is not None:
            vm_params['availability_set'] = {
                'id': av_set_id
            }

        if image_uri is not None:
            vm_params['storage_profile'] = {
                'os_disk': {
                    'name': os_disk_name,
                    'os_type': 'Linux',
                    'caching': 'None',
                    'create_option': 'fromImage',
                    'vhd': {
                        'uri': 'https://{}.blob.core.windows.net/vhds/{}.vhd'.format(
                            strg_acc_name, os_disk_name)
                    },
                    'image': {
                        'uri': image_uri
                    }
                }
            }
        else:
            vm_params['storage_profile'] = {
                # This will be used when we have a marketplace image
                'image_reference': {
                    'publisher': vm_reference['publisher'],
                    'offer': vm_reference['offer'],
                    'sku': vm_reference['sku'],
                    'version': 'latest'
                }
            }
        self.logger.info("vm create params: %s" % vm_params)
        return vm_params

    def get_storage_uri(self, storage_name):
        https = "https://"
        blob_string = ".blob.core.windows.net"
        uri = []
        uri.append(https)
        uri.append(storage_name)
        uri.append(blob_string)
        storage_uri = ''.join(uri)
        self.logger.info("Storage Account URI is %s" % storage_uri)
        return storage_uri

    def createRandomPassword(self, pwdLength=15, specialChars="False"):
        logger.info("Creating random password")
        if specialChars is None:
            specialChars = "True"
        # Generate new random password
        chars = string.ascii_letters + string.digits
        if specialChars == "True":
            chars += '#$%^&+='
            p = re.compile(
                '^(?=.{1,})(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[#$%^&+=]).*$')
        else:
            p = re.compile('^(?=.{1,})(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).*$')
        numTries = 0
        pwdFound = False
        while not pwdFound:
            password = ''
            numTries += 1
            for i in range(int(pwdLength)):
                password += chars[ord(os.urandom(1)) % len(chars)]
            m = p.match(password)
            if m is not None:
                pwdFound = True
        logger.info("Password created after %s tries", numTries)
        logger.debug("%s", password)
        return password

    def create_autoscaler_userdata(self, cfg, fingerprint, tag):
        tech_package = cfg.get_license_level_type()
        username = "automate"
        password = self.createRandomPassword()
        as_configs = []
        as_configs.append("\nsection: IOS Configuration\n")
        as_configs.append("username %s priv 15 pass %s\n" % (username, password))
        as_configs.append("ip ssh pubkey-chain\n")
        as_configs.append("username %s %s" % (username, "\n"))
        as_configs.append("key-hash ssh-rsa %s\n" %
                          (fingerprint))
        as_configs.append("\n")

        as_configs.append('Section: License\n')
        as_configs.append('TechPackage:' + tech_package + '\n')

        as_configs.append('Section: autoscaler\n')
        as_configs.append(tag + '\n')

        as_configs.append("Section: IOS Configuration\n")
        as_configs.append('')
        autoscaler = ''.join(as_configs)
        return autoscaler

    def create_userdata(self, cfg, status, inst_num, fingerprint, tag):
        cloud_config = cfg.get_default_instance_config()
        guestshell = cloud_config['guestshell_config']
        sectiontvnet = cloud_config['section_tvnet']
        role = 'role hub-' + str(inst_num) + '\n'
        tvnet_customdata = cloud_config['tvnetsa_customdata']
        as_customdata = self.create_autoscaler_userdata(cfg, fingerprint, tag)
        userdata = []
        userdata.append(as_customdata)
        userdata.append(guestshell)
        userdata.append(sectiontvnet)
        userdata.append(role)
        userdata.append(tvnet_customdata)
        customdata = ''.join(userdata)
        return customdata

    def spin_up_csr(self, cfg, status, image_id, name, allocationId, fingerprint, tag):
        attempts = 0
        while(attempts < 3):
            try:
                logger.info("Attempt # {}".format(attempts))
                inst_num = int(name.rsplit('-', 1)[1])
                if self.customer_resource_group is None:
                    raise Exception("RG name is None.")
                self.logger.info("Instance Number: %d" % inst_num)
                cloud_config = cfg.get_default_instance_config()
                self.logger.info("Cloud Config: %s" % cloud_config)
                userdata = self.create_userdata(cfg, status, inst_num, fingerprint, tag)
                boot_diag = cloud_config['boot_diagnostics']
                if boot_diag:
                    boot_diag_sa = self.get_storage_uri(cloud_config['boot_diagnostics_sa_name'])
                else:
                    boot_diag_sa = ""
                av_set_enabled = cloud_config['availability_set']
                if av_set_enabled == "Yes":
                    av_set_id = cloud_config['availability_set_id']
                else:
                    av_set_id = ""
                subnet_obj_list = cloud_config["subnet_id"]
                num_sub = len(subnet_obj_list)
                gi0_subnet = inst_num % num_sub
                # This is with assumption there are only two subnets
                gi1_subnet = (inst_num + 1) % num_sub
                nic_list = {}
                base_nic_name = name + '-nic'
                for index, subnet in enumerate(subnet_obj_list):
                    if index == 0:
                        nic_id = self.create_network_interface(base_nic_name + '-' + str(index), subnet_obj_list[gi0_subnet],
                                                               cloud_config['security_group_id'], allocationId)
                    else:
                        nic_id = self.create_network_interface(base_nic_name + '-' + str(index), subnet_obj_list[gi1_subnet])
                    nic_list[index] = nic_id
                vm_params = self.create_vm_parameters(name, self.region, cloud_config['username'], cloud_config['password'],
                                                      nic_list[0],
                                                      nic_list[1], cloud_config['vhd_storage_account'], image_id,
                                                      cloud_config['vm_size'], userdata, boot_diag, boot_diag_sa,
                                                      cloud_config['image_uri'], av_set_id)

                async_vm_creation = self.compute_client.virtual_machines.create_or_update(
                    self.customer_resource_group, name, vm_params
                )
                async_vm_creation.wait()
                self.logger.info("VM %s created successfully." % name)
                vm = self.compute_client.virtual_machines.get(self.customer_resource_group, name)
                self.logger.info("return from vm creation: %s" % vm.__dict__['id'])
                return vm.__dict__['id']
            except Exception as e:
                self.logger.exception("Attempt # {}, EXCEPTION: {}".format(attempts, e))
                x = e.error.error.lower()
                if 'propertychangenotallowed' in x:
                    self.logger.info("Terminating instance {} in rg {}.".format(name, self.customer_resource_group))
                    async_vm_deletion = self.compute_client.virtual_machines.delete(
                        self.customer_resource_group,
                        name,
                    )
                    async_vm_deletion.wait()
                    self.logger.info("Terminated Instance {} in rg {}".format(name, self.customer_resource_group))
            attempts += 1
        return None, None

    def delete_interfaces(self, cloud_config, vm_name):
        subnet_obj_list = cloud_config["subnet_id"]
        base_nic_name = vm_name + '-nic'
        try:
            for index in range(len(subnet_obj_list)):
                nic_id = self.network_client.network_interfaces.delete(self.customer_resource_group,
                                                                       base_nic_name + '-' + str(index))
                nic_id.wait()
                self.logger.info("Network interface %s deleted successfully" % (base_nic_name + '-' + str(index)))
            return True
        except Exception as e:
            self.logger.exception("Exception during delete of Network Interface attached to VM %s %s" % (vm_name, e))
            return None

    def spin_down_csr(self, instance_list, config):
        cloud_config = config
        vm_name = self.get_vm_name_from_instance_id(instance_list.pop())
        try:
            response = self.compute_client.virtual_machines.delete(self.customer_resource_group, vm_name)
            response.wait()
            self.logger.info("Deleted VM %s successfully." % vm_name)
            ret = self.delete_interfaces(cloud_config, vm_name)
            return True
        except Exception as e:
            self.logger.exception("Error in Deleting VM: %s" % e)
            return False

    def reboot_instance(self, instance_id):
        '''
        try:
            response = self.ec2_client.reboot_instances(
                InstanceIds=[
                    instance_id
                ],
            )

            self.logger.info("Rebooted instance %s" % instance_id)
            self.logger.debug("%s" % response)

        except Exception as e:
            self.logger.error("Failed to reboot instance %s: %s" % (instance_id, e))
            return False
        '''
        return True

    def clean_storage(self, storage_name, fileshare=None):
        if not fileshare:
            fileshare = self.fileshare
        account = CloudStorageAccount(storage_name, self.storage_acct_key)
        file_service = account.create_file_service()
        try:
            generator = file_service.list_directories_and_files(fileshare, self.privatekey_prefix)
            for file_or_dir in generator:
                splits = file_or_dir.split('.')
                if len(splits) > 1 and splits[-1] == 'pem':
                    instance_id = splits[0]
                    if self.get_running_state(instance_id) == None:
                        file_service.delete_file(fileshare, self.privatekey_prefix, file_or_dir)
                        self.logger.info("Deleted %s file" % (file_or_dir))
                    else:
                        self.logger.info(
                            "Instance %s is not terminated.  No need to delete pem file" %
                            instance_id)
        except Exception as e:
            self.logger.exception("EXCEPTION: %s" % e)

    def update_function(self, function_name, storage_name, key_name):
        return True

    def is_csr_image_version_16_9_1(self, image_id):
        return False