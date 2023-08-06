from .kafkaMetricsSchema.com.topkrabbensteam.zm.custom_metric.enums import PrometheusMetricType
from .abstractMetricProducer  import AbstractMetricProducer
from .kafkaMetricsSchema.com.topkrabbensteam.zm.metrics.prometheus_metric import LabelMap

class ErrorCounterMetric(AbstractMetricProducer):      
    def formMetric(self,errorCategory, labelDict, buckets = None):
        if type(errorCategory) is not str:
            raise Exception("Error category must be a string!")
            
        super().formMetric(1,labelDict,buckets)
        metricLabel = LabelMap()
        metricLabel.label = "category"
        metricLabel.lable_value = errorCategory
        self.prometheusMetric.metric_labels.append(metricLabel)

    def _finalizeMetricParameters(self):
        self.prometheusMetric.metric_name = "error_count"
        self.prometheusMetric.metric_type = PrometheusMetricType.Counter
        

        