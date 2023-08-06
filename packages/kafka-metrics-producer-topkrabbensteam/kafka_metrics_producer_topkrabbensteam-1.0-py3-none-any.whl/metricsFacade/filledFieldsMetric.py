from .kafkaMetricsSchema.com.topkrabbensteam.zm.custom_metric.enums import PrometheusMetricType
from .kafkaMetricsSchema.com.topkrabbensteam.zm.metrics.metric_header import  MetricHeader
from .kafkaMetricsSchema.com.topkrabbensteam.zm.metrics.prometheus_metric import  PrometheusMetricData
from .kafkaMetricsSchema.com.topkrabbensteam.zm.metrics import MetricsList
from .kafkaMetricsSchema.com.topkrabbensteam.zm.metrics import Metric
from .kafkaMetricsSchema.com.topkrabbensteam.zm.metrics.prometheus_metric import LabelMap
from .metricType import MetricType
from .abstractMetricProducer  import AbstractMetricProducer
import time

class FilledFieldsMetric(AbstractMetricProducer):   

    def countRawDataFilledFields(self,object):
        total_filled_fields = 0
        for attr, value in object.items():
            if value is not None:
                if type(value) is list:
                    for i in range(0,len(value)):
                        total_filled_fields = total_filled_fields + self.countRawDataFilledFields(value[i])
                elif type(value) is not str and type(value) is not int and type(value) is not float and type(value) is not bool:
                    total_filled_fields = total_filled_fields + self.countRawDataFilledFields(value)
                else:
                    total_filled_fields = total_filled_fields + 1
        return total_filled_fields

    def _finalizeMetricParameters(self):
        self.prometheusMetric.metric_name = "filled_field_count"
        self.prometheusMetric.metric_type = PrometheusMetricType.Gauge
        self.prometheusMetric.metric_value = self.countRawDataFilledFields(self.prometheusMetric.metric_value)
        