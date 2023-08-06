from abc import ABC
from abc import abstractmethod
from .kafkaMetricsSchema.com.topkrabbensteam.zm.custom_metric.enums import PrometheusMetricType
from .kafkaMetricsSchema.com.topkrabbensteam.zm.metrics.metric_header import  MetricHeader
from .kafkaMetricsSchema.com.topkrabbensteam.zm.metrics.prometheus_metric import  PrometheusMetricData
from .kafkaMetricsSchema.com.topkrabbensteam.zm.metrics import MetricsList
from .kafkaMetricsSchema.com.topkrabbensteam.zm.metrics import Metric
from .kafkaMetricsSchema.com.topkrabbensteam.zm.metrics.prometheus_metric import LabelMap

from .metricType import MetricType
import time

class AbstractMetricProducer(ABC):
    
    def __init__(self, moduleName):
        if type(moduleName) is not str:
            raise Exception("Module name must be a string!")
        if "." in moduleName:
            moduleName = moduleName.replace(".", "_")

        self.initMetricMetadata(moduleName)

    def initMetricMetadata(self, moduleName):
        self.current_milli_time = lambda: int(round(time.time() * 1000))        
        self.metric = Metric()
        self.metric.data_type = MetricType.RED.name
        self.metricHeader = MetricHeader()        
        self.metricHeader.pushed_at = self.current_milli_time()
        self.metricHeader.source = moduleName
        self.metricHeader.source_type = "Backend"
        self.metricHeader.priority = "Middle"
        self.metricHeader.level = "INFO"
        self.metric.metric_header = self.metricHeader
        self.prometheusMetric = PrometheusMetricData()        

    def changeMetricPriority(self,priority):
        self.metricHeader.priority = priority

    def changeMetricLevel(self,level):
        self.metricHeader.level = level

    def changeMetricSourceType(self,source_type):
        self.metricHeader.source_type = source_type

    def changeMetricType(self,metric_type):
        self.metricHeader.source_type = metric_type
    
    def _preInitMetric(self):
        self.metricHeader.pushed_at = self.current_milli_time()    

    
    def _setMetricData(self,metricValue, labelDict, buckets = None):                        
        if buckets is not None:           
           self.prometheusMetric.buckets = buckets
        else:
           self.prometheusMetric.buckets = []

        self.prometheusMetric.metric_value = metricValue        

        #clear labels
        self.prometheusMetric.metric_labels.clear()

        metricLabel = LabelMap()
        metricLabel.label = "module_name"
        metricLabel.lable_value = self.metricHeader.source
        self.prometheusMetric.metric_labels.append(metricLabel)

        #add labels from labelDict
        for metricLabelKey in labelDict:
            #add labels
            metricLabel = LabelMap()
            metricLabel.label = metricLabelKey.replace(".", "_")
            metricLabel.lable_value = labelDict[metricLabelKey].replace(".", "_")
            self.prometheusMetric.metric_labels.append(metricLabel)

        self.metric.prometheus_metric_data = self.prometheusMetric
        

    @abstractmethod
    def _finalizeMetricParameters(self):
        pass

    def getMetric(self):
        return self.metric  

    def formMetric(self,metricValue, labelDict, buckets = None):

        if(self.metricHeader.source is None):
            raise Exception("Module must be provided!")
        
        if(labelDict is None):
            raise Exception("Labels are not specified!")  
        
        for key in labelDict:
            if type(labelDict[key]) is not str:
                raise Exception("All label values must be strings!")

        self._preInitMetric()
        self._setMetricData(metricValue,labelDict,buckets)
        self._finalizeMetricParameters()

        if(self.prometheusMetric.metric_type is None):
            raise Exception("Prometheus metric type are not specified!")

        if(self.prometheusMetric.metric_name is None):
            raise Exception("Metric name must be provided in a derived class")

        if (self.prometheusMetric.metric_type == PrometheusMetricType.Histogram):
            if(self.prometheusMetric.buckets is None or not self.prometheusMetric.buckets):
                raise Exception("Buckets are not specified!")   

        

    