'''
Cisco Copyright 2018
Author: Vishlesh Patel <vishlpa4@cisco.com>

FILENAME: METRIC_UTILS.PY
'''

import logging
import os
from applicationinsights import TelemetryClient
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
from azure.mgmt.monitor import MonitorManagementClient
import urlparse
import requests
import configparser

AI_URLBASE = "https://api.applicationinsights.io/{version}/apps/{appId}/{operation}/"
API_VERSION = 'v1'

class MetricUtils:

    def __init__(self, feature=None):
        self.feature = feature if feature is not None else __name__
        self.logger = logging.getLogger(self.feature)
        self.apiKey = os.getenv("API_KEY", '')
        self.appId = os.getenv("APP_ID", '')
        self.instrumentation_key = os.getenv("INSTRUMENTATION_KEY","")
        self.tc = TelemetryClient(self.instrumentation_key)
        self.region = os.getenv('DEFAULT_REGION', "")
        self.app_id = os.getenv("AZURE_CLIENT_ID", "")
        self.app_key = os.getenv("AZURE_CLIENT_SECRET", "")
        self.subscription_id = os.getenv("SUBSCRIPTION_ID", "")
        self.tenant = os.getenv("TENANT_ID", "")
        self.credentials = ServicePrincipalCredentials(
            client_id=self.app_id,
            secret=self.app_key,
            tenant=self.tenant
        )
        self.customer_resource_group = os.getenv("CUSTOMER_RESOURCE_GROUP", "")
        self.appInsights_client = ApplicationInsightsManagementClient(credentials=self.credentials,subscription_id=self.subscription_id)

        self.monitor_management_client = MonitorManagementClient(self.credentials, self.subscription_id)

    def create_app_insights_resource(self, resource_name):
        insights_properties = {}
        insights_properties['location'] = self.region
        insights_properties['kind'] = 'other'
        insights_properties['application_type'] = 'other'
        insights_properties['flow_type'] = 'Bluefield'
        insights_properties['request_source'] = 'rest'
        try:
            response = self.appInsights_client.components.create_or_update(self.customer_resource_group,resource_name,insights_properties)
            self.logger.info("App Insight resource created successfully: %s" % response)
            return response.instrumentation_key, response.app_id
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return None

    def create_api_key(self,resource_name):
        try:
            api_params = {}
            api_params['name'] = resource_name + '-api-key'
            url = '/subscriptions/' + self.subscription_id + '/resourcegroups/' + self.customer_resource_group + '/providers/Microsoft.insights/components/' + resource_name + '/api'
            api_params['linked_read_properties'] = [url]
            api_key = self.appInsights_client.api_keys.create(self.customer_resource_group, resource_name, api_params)
            self.logger.info("API key created successfully: %s" % api_key)
            return api_key
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return None

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
                if value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                os.environ[key] = str(value)
        except Exception as e:
            self.logger.exception(e)

    def put_metric(self, metricName, value, dimensions=None):
        try:
            self.tc.track_metric(metricName, value, properties=dimensions)
        except Exception as e:
            self.logger.exception(e)

    def put_event(self, eventName, value=None, dimenstions=None):
        measurements = None
        if value is not None:
            measurements = {
                'value' : value
            }
        try:
            self.tc.track_event(eventName, measurements, dimenstions)
        except Exception as e:
            self.logger.exception(e)

    def get_az_time(self, time_period):
        '''

        :param time_period: time period in seconds
        :return:
        '''
        t = None
        time_period = int(time_period)
        if time_period < 60:
            t = "PT" + str(time_period) + "S"
        elif time_period < 3600:
            time_period = int(time_period / 60)
            t = "PT" + str(time_period) + "M"
        elif time_period < 21600:
            time_period = int(time_period / 3600)
            t = "PT" + str(time_period) + "H"
        else:
            time_period = int(time_period / 21600)
            t = "P" + str(time_period) + "D"
        return t

    # def get_azure_metric(self, vm_name, metric, minutes):
    def get_azure_metric(self,
                   metricName,
                   period=60,
                   metric_period=60,
                   aggregation_type='avg',
                   resource_id=None):

        try:
            timespan = self.get_az_time(period)
            interval = self.get_az_time(metric_period)

            metrics_data = self.monitor_management_client.metrics.list(
                resource_id,
                timespan=timespan,
                interval=interval,
                aggregation='Total',
                metricnames=metricName
            )
        except Exception as e:
            self.logger.exception("Exception while retrieving metric %s: %s" % (metricName, e))
            return
        # build up list to return
        mylist = []

        for item in metrics_data.value:
            for timeserie in item.timeseries:
                for data in timeserie.data:
                    if aggregation_type.lower() == 'avg':
                        data.total = data.total / metric_period
                    metric_tuple = (metricName, data.time_stamp, data.total)
                    mylist.append(metric_tuple)

        return mylist

    def get_custom_metric(self,
                   metricName,
                   metricType='customMetrics',
                   period=60,
                   metric_period=60,
                   aggregation_type='avg',
                   dimensions=None):
        '''
        :param name: name of the metric to retrieve
        :param metricType - Type of metric
        :param timespan - timespan period - PT1D (Past 1 day), or PT1H (Past 1 Hour) or PT1M (Past 1 Minute)
        :param interval - interval period - PT1D (Past 1 day), or PT1H (Past 1 Hour) or PT1M (Past 1 Minute)
        :param dimesions: dimensions dict if you want to retrieve metric for only that dimensions
            for e.g.,
            if you want to retrieve metrics only for CSR whose instanceID == 1
            dimensions dict --> { 'instanceID' : '1' }
        :return: returns metrics collected in dict format
        '''
        try:
            metricPath = metricType + '/' + metricName
            aggregation_type = aggregation_type.lower()
            dimensionsKey = None
            dimensionsVal = None
            if len(dimensions) > 0:
                keys = dimensions.keys()
                dimensionsKey = keys[0]
                dimensionsVal = dimensions[keys[0]]
            new_url = AI_URLBASE.format(
                version=API_VERSION, appId=self.appId, operation='metrics')
            url = urlparse.urljoin(new_url, metricPath)
            timespan = self.get_az_time(period)
            interval = self.get_az_time(metric_period)

            query = 'timespan={}&interval={}&aggregation={}'.format(
                timespan, interval, aggregation_type)
            if dimensionsKey is not None and dimensionsVal is not None:
                query += "&filter=customDimensions/{}%20eq%20'{}'".format(dimensionsKey, dimensionsVal)
            url += '?' + query
            self.logger.debug("url being used to retrieve metrics {}".format(url))
            metrics = requests.get(url, headers={"X-Api-Key": self.apiKey})
            if metrics.status_code == 200:
                self.logger.debug("Get Metric request status code - 200")
            else:
                self.logger.warning("bad return status code {} when trying to retrieve {}, dimension {}, \
                aggregation type {}".format(metrics.status_code, metricPath, dimensionsVal, aggregation_type))

            mylist = []
            metrics = metrics.json()
            for segment in metrics['value']['segments']:
                metricPath = 'customMetrics/{}'.format(metricName)
                response_value = segment[metricPath][aggregation_type]
                timestamp = segment["start"]
                mylist.append((metricName, timestamp, response_value))

            return mylist

        except Exception as e:
            self.logger.exception(e)
            return None

    def get_event_metrics(self,
                          name,
                          eventType='customEvents',
                          period='PT24H',
                          query=None):
        '''

        :param name: Name of event
        :param eventType: Event type. e.g. customEvents, traces, requests
        :param period: Timespan
        :param query: Search Query
        :return:
        '''
        try:
            new_url = AI_URLBASE.format(
                version=API_VERSION, appId=self.appId, operation='metrics')
            url = urlparse.urljoin(new_url, eventType)
            q = '?timespan={}'.format(period)
            q += "&$filter=customEvent/name eq '{}'".format(name)
            if query is not None:
                q += '&' + query

            url += '?' + q
            self.logger.debug("url being used to retrieve events {}".format(url))
            self.logger.debug(self.apiKey)
            events = requests.get(url, headers={"X-Api-Key": self.apiKey}).text
            if events.status_code == 200:
                self.logger.debug("Get event request status code - 200")
            else:
                self.logger.warning("bad return status code {}".format(events.status_code))
            return events.json()
        except Exception as e:
            self.logger.exception(e)

    def flush_metric_queue(self):
        try:
            self.tc.flush()
        except Exception as e:
            self.logger.exception(e)
