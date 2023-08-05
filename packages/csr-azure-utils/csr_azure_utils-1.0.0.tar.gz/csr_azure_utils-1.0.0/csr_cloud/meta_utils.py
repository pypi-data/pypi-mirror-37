import json
import logging
import urllib2
import os

metadata_dir = '/home/guestshell/azure/tools/MetadataMgr/'
metadata_file = metadata_dir + 'metadata.json'
metadata_url = 'http://169.254.169.254/metadata/instance?api-version=2017-12-01'
headers = {'Metadata': 'true'}

deviceType='localMachine'
try:
    import cli
    deviceType='csr1000v'
except Exception as e:
    print(e)


def mkdir_p(path):
    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except Exception as e:
            return False
    return True

class MetaDataUtils:

    def __init__(self, feature=None):
        self.metadata = None
        self.feature = feature if feature is not None else __name__
        self.log = logging.getLogger(self.feature)

        if deviceType == 'csr1000v':
            mkdir_p(metadata_dir)
            if os.path.exists(metadata_file):
                self.read_metadata_from_file()
                current_version = metadata_url.split('=')[1].replace('-', '')
                if current_version not in self.metadata["compute"]["version"]:
                    self.metadata = self.get_metadata()
                    self.write_metadata_to_file()
            else:
                self.metadata = self.get_metadata()
                self.write_metadata_to_file()



    def write_metadata_to_file(self):
        with open(metadata_file, 'w') as fh:
            fh.write(json.dumps(self.metadata, indent=2))

    def read_metadata_from_file(self):
        with open(metadata_file, 'r') as fh:
            self.metadata = json.load(fh)

    def dump_metadata(self):
        print(json.dumps(self.metadata, indent=2))

    def pretty_metadata(self):
        for i, interface in enumerate(self.metadata["network"]["interface"]):
            print("Port %d" % i)
            print("Mac is %s" % interface["macAddress"])
            for j, ip in enumerate(interface["ipv4"]["ipAddress"]):
                print("Public ip is %s" % ip["publicIpAddress"])
                print("Private ip is %s" % ip["privateIpAddress"])
            for s, subnet in enumerate(interface["ipv4"]["subnet"]):
                print("subnet is %s/%s" % (subnet["address"], subnet["prefix"]))


    def get_metadata(self):
        req = urllib2.Request(metadata_url, headers=headers)
        resp = urllib2.urlopen(req)
        resp_read = resp.read()
        data = json.loads(resp_read)
        return data

    def get_pip(self):
        for _, interface in enumerate(self.metadata["network"]["interface"]):
            for _, ip in enumerate(interface["ipv4"]["ipAddress"]):
                if ip['publicIpAddress'] is not u'':
                    self.log.info("[INFO] Public ip is %s" % ip["publicIpAddress"])
                    return ip['publicIpAddress']

    def get_private_ip(self):
        for _, interface in enumerate(self.metadata["network"]["interface"]):
            for _, ip in enumerate(interface["ipv4"]["ipAddress"]):
                if ip['privateIpAddress'] is not u'':
                    log.info("[INFO] Private ip is %s" % ip["privateIpAddress"])
                    return ip['privateIpAddress']

    def get_vmid(self):
        return self.metadata['compute']['vmId']

    def get_subscriptionId(self):
        subid = ''
        try:
            subid = self.metadata["compute"]["subscriptionId"]
        except KeyError:
            subid = ''
        finally:
            return subid


    def get_resourceGroup(self):
        rg = ''
        try:
            rg = self.metadata["compute"]["resourceGroupName"]
        except KeyError:
            rg = ''
        finally:
            return rg
    
    
    def get_compute_param(self, param):
        param_value = ''
        try:
            param_value = self.metadata["compute"][param]
        except KeyError:
            param_value = ''
        finally:
            return param_value


    def get_instance_id(self):
        '''
        :return: returns short instance id of instance.
        '''
        if deviceType == 'csr1000v':
            return self.metadata['compute']['vmId']
        else:
            return "1234-5678"

    def get_instance_name(self):
        '''
        :return: returns instance name from metadata
        '''
        if deviceType == 'csr1000v':
            return self.metadata['compute']['name']
        else:
            return "myMac"


    def get_rg_vmname_combo_id(self):
        '''

        :return: returns combination of rg and vmname <RG>-<vmname>
        '''

        if deviceType == 'csr1000v':
            vmname = self.metadata['compute']['name']
            rg = self.metadata['compute']['resourceGroupName']
            id = "{}-{}".format(str(rg).lower(), str(vmname).lower())
            return id
        else:
            return 'rgname-vmname'
