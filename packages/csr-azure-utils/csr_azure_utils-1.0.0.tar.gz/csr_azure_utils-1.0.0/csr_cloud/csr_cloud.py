import logging
from logging.handlers import RotatingFileHandler
import os
import errno
from azure_utils import AzureUtils
from os.path import expanduser



class csr_cloud():
    def __init__(self, feature, input1=None, input2=None, cloudname='azure'):
        self.cloudname = cloudname
        self.feature = feature
        self.log = None
        if self.feature == "tvnet":
            self.setup_logging()
            self.tvnet = AzureUtils(input1, input2, self.cloudname, self.feature)
        elif self.feature == "HA":
            self.setup_logging(expanduser('~/cloud/' + self.feature), 'csr_ha.log')
            from .ha_azure import csr_ha
            self.ha = csr_ha()
            # TODO: Need to remove the Debug logging level after testing, added this to give more details in case when a test fails.
            self.log.setLevel(logging.DEBUG)
        elif self.feature == "autoscaler":
            self.setup_logging()
            as_exception = None
            try:
                from .as_azure import as_cloud
            except Exception as e:
                as_exception = e
                pass
            if as_exception is not None:
                self.log.warning("failed to import as_azure module. Exception : {}".format(as_exception))
            else:
                self.as_cloud = as_cloud()

    def mkdir_p(self, path):
        try:
            os.makedirs(path, exist_ok=True)  # Python>3.2
        except TypeError:
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise

    def setup_logging(self, directory=None, logfile_name = None):
        try:
            if directory is None:
                directory = expanduser('~/' + self.feature + '/' + 'logs')

            path = directory + '/'
            self.mkdir_p(path)
            #logfile_name = self.feature + '_' + \
            #    str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H_%M_%S')) + '.log'
            if logfile_name is None:
                logfile_name = self.feature + '.log'
            hdlr = RotatingFileHandler(os.path.join(directory, logfile_name), mode='a', maxBytes=5 * 1024 * 1024,
                                             backupCount=2, encoding=None, delay=0)

            formatter = logging.Formatter('%(module)15s:%(funcName)25s:%(lineno)4s %(asctime)s %(levelname)s %(message)s')
            hdlr.setFormatter(formatter)
            self.log = logging.getLogger(self.feature)
            if not len(self.log.handlers):
                self.log.addHandler(hdlr)
            self.log.setLevel(logging.INFO)
        except Exception as e:
            print("csr_cloud: setup_logging: exception {}. ".format(e))
            pass
