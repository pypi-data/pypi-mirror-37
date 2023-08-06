from .kafkaMetricsSchema.com.topkrabbensteam.zm.custom_metric.enums import PrometheusMetricType
from .abstractMetricProducer  import AbstractMetricProducer

class AdvertCrawlTimeSecondsMetric(AbstractMetricProducer):      

    def _finalizeMetricParameters(self):
        self.prometheusMetric.metric_name = "advert_crawl_time_seconds"
        self.prometheusMetric.metric_type = PrometheusMetricType.Histogram
        self.prometheusMetric.buckets = [0,2,3,5,8,10,15,30,50,80,90,float('Inf')]

        