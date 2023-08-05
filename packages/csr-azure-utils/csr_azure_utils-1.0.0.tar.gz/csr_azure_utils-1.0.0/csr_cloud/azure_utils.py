
from file_utils import StorageFileUtils
from meta_utils import MetaDataUtils
from general_utils import GeneralUtils

class AzureUtils(StorageFileUtils, MetaDataUtils, GeneralUtils):
    def __init__(self, account_name, account_key, cloudname, feature):
        StorageFileUtils.__init__(self, account_name, account_key, cloudname, feature)
        MetaDataUtils.__init__(self, feature)
        GeneralUtils.__init__(self)

