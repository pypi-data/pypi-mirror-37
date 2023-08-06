

from .schema_classes import SchemaClasses, SCHEMA as my_schema, get_schema_type
from avro.io import DatumReader


class SpecificDatumReader(DatumReader):
    SCHEMA_TYPES = {
        "com.topkrabbensteam.zm.custom_metric.enums.PrometheusMetricType": SchemaClasses.com.topkrabbensteam.zm.custom_metric.enums.PrometheusMetricTypeClass,
        "com.topkrabbensteam.zm.metrics.Metric": SchemaClasses.com.topkrabbensteam.zm.metrics.MetricClass,
        "com.topkrabbensteam.zm.metrics.MetricsList": SchemaClasses.com.topkrabbensteam.zm.metrics.MetricsListClass,
        "com.topkrabbensteam.zm.metrics.metric_header.MetricHeader": SchemaClasses.com.topkrabbensteam.zm.metrics.metric_header.MetricHeaderClass,
        "com.topkrabbensteam.zm.metrics.prometheus_metric.LabelMap": SchemaClasses.com.topkrabbensteam.zm.metrics.prometheus_metric.LabelMapClass,
        "com.topkrabbensteam.zm.metrics.prometheus_metric.PrometheusMetricData": SchemaClasses.com.topkrabbensteam.zm.metrics.prometheus_metric.PrometheusMetricDataClass,
    }
    def __init__(self, readers_schema=None, **kwargs):
        writers_schema = kwargs.pop("writers_schema", readers_schema)
        writers_schema = kwargs.pop("writer_schema", writers_schema)
        super(SpecificDatumReader, self).__init__(writers_schema, readers_schema, **kwargs)
    def read_record(self, writers_schema, readers_schema, decoder):
        
        result = super(SpecificDatumReader, self).read_record(writers_schema, readers_schema, decoder)
        
        if readers_schema.fullname in SpecificDatumReader.SCHEMA_TYPES:
            result = SpecificDatumReader.SCHEMA_TYPES[readers_schema.fullname](result)
        
        return result