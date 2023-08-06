import json
import os.path
import decimal
import datetime
import six
from avrogen.dict_wrapper import DictWrapper
from avrogen import avrojson
from avro import schema as avro_schema
if six.PY3:    from avro.schema import SchemaFromJSONData as make_avsc_object
    
else:
    from avro.schema import make_avsc_object
    
_STRING_SCHEMA_JSON = "{\"type\": \"record\", \"namespace\": \"com.topkrabbensteam.zm.metrics\", \"name\": \"MetricsList\", \"fields\": [{\"name\": \"metrics\", \"type\": {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"Metric\", \"fields\": [{\"name\": \"data_type\", \"type\": \"string\", \"doc\": \"\\u0420\\u045e\\u0420\\u0451\\u0420\\u0457 \\u0420\\u0491\\u0420\\u00b0\\u0420\\u0405\\u0420\\u0405\\u0421\\u2039\\u0421\\u2026 \\u0420\\u0458\\u0420\\u00b5\\u0421\\u201a\\u0421\\u0402\\u0420\\u0451\\u0420\\u0454\\u0420\\u0451: RED (RED) - Requests, Errors, Duration. \\u0420\\u045a\\u0420\\u00b5\\u0421\\u201a\\u0421\\u0402\\u0420\\u0451\\u0420\\u0454\\u0420\\u0451 \\u0421\\u0402\\u0420\\u00b0\\u0420\\u00b1\\u0420\\u0455\\u0421\\u201a\\u0421\\u2039 \\u0420\\u0454\\u0420\\u0455\\u0420\\u0458\\u0420\\u0457\\u0420\\u0455\\u0420\\u0405\\u0420\\u00b5\\u0420\\u0405\\u0421\\u201a\\u0420\\u00b0. \\u0420\\u0459\\u0420\\u0455\\u0420\\u00bb\\u0420\\u0451\\u0421\\u2021\\u0420\\u00b5\\u0421\\u0403\\u0421\\u201a\\u0420\\u0406\\u0420\\u0455 \\u0420\\u00b7\\u0420\\u00b0\\u0420\\u0457\\u0421\\u0402\\u0420\\u0455\\u0421\\u0403\\u0420\\u0455\\u0420\\u0406, \\u0420\\u0454\\u0420\\u0455\\u0420\\u00bb\\u0420\\u0451\\u0421\\u2021\\u0420\\u00b5\\u0421\\u0403\\u0421\\u201a\\u0420\\u0406\\u0420\\u0455 \\u0420\\u0455\\u0421\\u20ac\\u0420\\u0451\\u0420\\u00b1\\u0420\\u0455\\u0420\\u0454, \\u0420\\u0406\\u0421\\u0402\\u0420\\u00b5\\u0420\\u0458\\u0421\\u040f \\u0420\\u0455\\u0420\\u00b1\\u0421\\u0402\\u0420\\u00b0\\u0420\\u00b1\\u0420\\u0455\\u0421\\u201a\\u0420\\u0454\\u0420\\u0451 2 - USE (USE) - \\u0420\\u045a\\u0420\\u00b5\\u0421\\u201a\\u0421\\u0402\\u0420\\u0451\\u0420\\u0454\\u0420\\u00b0 \\u0421\\u0403\\u0420\\u0406\\u0421\\u040f\\u0420\\u00b7\\u0420\\u00b0\\u0420\\u0405\\u0420\\u0405\\u0420\\u00b0\\u0421\\u040f \\u0421\\u0403 \\u0421\\u0402\\u0420\\u00b5\\u0420\\u00b7\\u0421\\u0453\\u0420\\u00bb\\u0421\\u040a\\u0421\\u201a\\u0420\\u00b0\\u0421\\u201a\\u0420\\u0455\\u0420\\u0458 \\u0421\\u0402\\u0420\\u00b0\\u0420\\u00b1\\u0420\\u0455\\u0421\\u201a\\u0421\\u2039, \\u0420\\u00b7\\u0420\\u00b0\\u0420\\u0457\\u0421\\u0402\\u0420\\u0455\\u0421\\u0403\\u0421\\u2039,  \\u0420\\u0455\\u0421\\u20ac\\u0420\\u0451\\u0420\\u00b1\\u0420\\u0454\\u0420\\u0451 \\u0420\\u0451 \\u0421\\u201a.\\u0420\\u0491. 3 - Custom (Custom) - \\u0420\\u045a\\u0420\\u00b5\\u0421\\u201a\\u0421\\u0402\\u0420\\u0451\\u0420\\u0454\\u0420\\u00b0 \\u0420\\u0406 \\u0421\\u0403\\u0420\\u0406\\u0420\\u0455\\u0420\\u00b1\\u0420\\u0455\\u0420\\u0491\\u0420\\u0405\\u0420\\u0455\\u0420\\u0458  \\u0421\\u201e\\u0420\\u0455\\u0421\\u0402\\u0420\\u0458\\u0420\\u00b0\\u0421\\u201a\\u0420\\u00b5, \\u0420\\u0455\\u0420\\u00b1\\u0421\\u0402\\u0420\\u00b0\\u0420\\u00b1\\u0420\\u0455\\u0421\\u201a\\u0420\\u0454\\u0420\\u00b0 \\u0420\\u00b7\\u0420\\u00b0\\u0420\\u0406\\u0420\\u0451\\u0421\\u0403\\u0420\\u0451\\u0421\\u201a \\u0420\\u0455\\u0421\\u201a \\u0420\\u0491\\u0420\\u00b0\\u0420\\u0405\\u0420\\u0405\\u0421\\u2039\\u0421\\u2026 \\u0420\\u0406 \\u0420\\u0457\\u0420\\u0455\\u0420\\u00bb\\u0420\\u00b5 data\"}, {\"name\": \"data\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"log_data\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"metric_header\", \"type\": [\"null\", {\"type\": \"record\", \"namespace\": \"com.topkrabbensteam.zm.metrics.metric_header\", \"name\": \"MetricHeader\", \"fields\": [{\"name\": \"source\", \"type\": \"string\"}, {\"name\": \"source_type\", \"type\": \"string\", \"doc\": \"\\u0420\\u045e\\u0420\\u0451\\u0420\\u0457 \\u0420\\u0451\\u0421\\u0403\\u0421\\u201a\\u0420\\u0455\\u0421\\u2021\\u0420\\u0405\\u0420\\u0451\\u0420\\u0454\\u0420\\u00b0: 1 - Frontend (Frontend). \\u0420\\u0459\\u0420\\u0455\\u0420\\u0458\\u0420\\u0457\\u0420\\u0455\\u0420\\u0405\\u0420\\u00b5\\u0420\\u0405\\u0421\\u201a \\u0420\\u0451\\u0421\\u0403\\u0421\\u201a\\u0420\\u0455\\u0421\\u2021\\u0420\\u0405\\u0420\\u0451\\u0420\\u0454\\u0420\\u00b0 \\u0420\\u0405\\u0420\\u00b0\\u0421\\u2026\\u0420\\u0455\\u0420\\u0491\\u0420\\u0451\\u0421\\u201a\\u0421\\u0403\\u0421\\u040f \\u0420\\u0405\\u0420\\u00b0 \\u0421\\u0453\\u0421\\u0402\\u0420\\u0455\\u0420\\u0406\\u0420\\u0405\\u0420\\u00b5 UI 2 - Backend (Backend). \\u0420\\u0459\\u0420\\u0455\\u0420\\u0458\\u0420\\u0457\\u0420\\u0455\\u0420\\u0405\\u0420\\u00b5\\u0420\\u0405\\u0421\\u201a \\u0420\\u0451\\u0421\\u0403\\u0421\\u201a\\u0420\\u0455\\u0421\\u2021\\u0420\\u0405\\u0420\\u0451\\u0420\\u0454\\u0420\\u00b0 \\u0420\\u0405\\u0420\\u00b0\\u0421\\u2026\\u0420\\u0455\\u0420\\u0491\\u0420\\u0451\\u0421\\u201a\\u0421\\u0403\\u0421\\u040f \\u0420\\u0405\\u0420\\u00b0 \\u0421\\u0453\\u0421\\u0402\\u0420\\u0455\\u0420\\u0406\\u0420\\u0405\\u0420\\u00b5 \\u0421\\u0403\\u0420\\u00b5\\u0421\\u0402\\u0420\\u0406\\u0420\\u00b5\\u0421\\u0402\\u0420\\u00b0\"}, {\"name\": \"requester_uri\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"pushed_at\", \"type\": \"long\"}, {\"name\": \"priority\", \"type\": \"string\", \"doc\": \"\\u0420\\u045f\\u0421\\u0402\\u0420\\u0451 \\u0420\\u0457\\u0421\\u0402\\u0420\\u0451\\u0420\\u0455\\u0421\\u0402\\u0420\\u0451\\u0421\\u201a\\u0420\\u00b5\\u0421\\u201a \\u0420\\u0458\\u0420\\u00b5\\u0421\\u201a\\u0420\\u0451\\u0420\\u0454\\u0420\\u0451: 1 - Low. \\u0420\\u045c\\u0420\\u0451\\u0420\\u00b7\\u0420\\u0454\\u0420\\u0451\\u0420\\u2116 \\u0420\\u0457\\u0421\\u0402\\u0420\\u0451\\u0420\\u0455\\u0421\\u0402\\u0420\\u0451\\u0421\\u201a\\u0420\\u00b5\\u0421\\u201a 2 - Middle. \\u0420\\u040e\\u0421\\u0402\\u0420\\u00b5\\u0420\\u0491\\u0420\\u0405\\u0420\\u0451\\u0420\\u2116 \\u0420\\u0457\\u0421\\u0402\\u0420\\u0451\\u0420\\u0455\\u0421\\u0402\\u0420\\u0451\\u0421\\u201a\\u0420\\u00b5\\u0421\\u201a 3 - High. \\u0420\\u2019\\u0421\\u2039\\u0421\\u0403\\u0420\\u0455\\u0420\\u0454\\u0420\\u0451\\u0420\\u2116 \\u0420\\u0457\\u0421\\u0402\\u0420\\u0451\\u0420\\u0455\\u0421\\u0402\\u0420\\u0451\\u0421\\u201a\\u0420\\u00b5\\u0421\\u201a 4 - Critical. \\u0420\\u0459\\u0421\\u0402\\u0420\\u0451\\u0421\\u201a\\u0420\\u0451\\u0421\\u2021\\u0420\\u0405\\u0420\\u00b0\\u0421\\u040f \\u0420\\u0455\\u0421\\u20ac\\u0420\\u0451\\u0420\\u00b1\\u0420\\u0454\\u0420\\u00b0\"}, {\"name\": \"level\", \"type\": \"string\", \"doc\": \"\\u0420\\u0408\\u0421\\u0402\\u0420\\u0455\\u0420\\u0406\\u0420\\u00b5\\u0420\\u0405\\u0421\\u040a \\u0420\\u00bb\\u0420\\u0455\\u0420\\u0456\\u0420\\u0456\\u0420\\u0451\\u0421\\u0402\\u0420\\u0455\\u0420\\u0406\\u0420\\u00b0\\u0420\\u0405\\u0420\\u0451\\u0421\\u040f, \\u0420\\u0454\\u0420\\u0455\\u0421\\u201a\\u0420\\u0455\\u0421\\u0402\\u0421\\u2039\\u0420\\u2116 \\u0420\\u0406 \\u0420\\u0491\\u0420\\u00b0\\u0420\\u0405\\u0420\\u0405\\u0421\\u2039\\u0420\\u2116 \\u0420\\u0458\\u0420\\u0455\\u0420\\u0458\\u0420\\u00b5\\u0420\\u0405\\u0421\\u201a \\u0420\\u0406\\u0420\\u0454\\u0420\\u00bb\\u0421\\u040b\\u0421\\u2021\\u0420\\u00b5\\u0420\\u0405 \\u0420\\u0406 \\u0420\\u0451\\u0421\\u0403\\u0421\\u201a\\u0420\\u0455\\u0421\\u2021\\u0420\\u0405\\u0420\\u0451\\u0420\\u0454\\u0420\\u00b5 \\u0420\\u0458\\u0420\\u00b5\\u0421\\u201a\\u0421\\u0402\\u0420\\u0451\\u0420\\u0454. \\u0420\\u045a\\u0420\\u0455\\u0420\\u00b6\\u0420\\u00b5\\u0421\\u201a \\u0420\\u0457\\u0421\\u0402\\u0420\\u0451\\u0420\\u0405\\u0420\\u0451\\u0420\\u0458\\u0420\\u00b0\\u0421\\u201a\\u0421\\u040a \\u0420\\u00b7\\u0420\\u0405\\u0420\\u00b0\\u0421\\u2021\\u0420\\u00b5\\u0420\\u0405\\u0420\\u0451\\u0421\\u040f: INFO, WARN, DEBUG, ERROR\"}]}], \"default\": null}, {\"name\": \"prometheus_metric_data\", \"type\": [\"null\", {\"type\": \"record\", \"name\": \"PrometheusMetricData\", \"namespace\": \"com.topkrabbensteam.zm.metrics.prometheus_metric\", \"doc\": \"this is custom metric that can be used by Prometheus Metrics Exporter Tool\", \"fields\": [{\"name\": \"metric_type\", \"type\": {\"type\": \"enum\", \"name\": \"PrometheusMetricType\", \"namespace\": \"com.topkrabbensteam.zm.custom_metric.enums\", \"symbols\": [\"Counter\", \"Gauge\", \"Histogram\", \"Summary\"]}, \"doc\": \"\\u0420\\u045e\\u0420\\u0451\\u0420\\u0457\\u0421\\u2039 \\u0420\\u0458\\u0420\\u00b5\\u0421\\u201a\\u0421\\u0402\\u0420\\u0451\\u0420\\u0454 \\u0421\\u0403\\u0420\\u0451\\u0421\\u0403\\u0421\\u201a\\u0420\\u00b5\\u0420\\u0458\\u0421\\u2039 Prometheus\"}, {\"name\": \"metric_value\", \"type\": \"float\", \"doc\": \"\\u0420\\u2014\\u0420\\u0405\\u0420\\u00b0\\u0421\\u2021\\u0420\\u00b5\\u0420\\u0405\\u0420\\u0451\\u0420\\u00b5 metric_value \\u0420\\u0491\\u0420\\u00bb\\u0421\\u040f Counter: \\u0421\\u0453\\u0420\\u0406\\u0420\\u00b5\\u0420\\u00bb\\u0420\\u0451\\u0421\\u2021\\u0420\\u0451\\u0420\\u0406\\u0420\\u00b0\\u0420\\u00b5\\u0421\\u201a \\u0420\\u0405\\u0420\\u00b0 \\u0420\\u00b7\\u0420\\u0405\\u0420\\u00b0\\u0421\\u2021\\u0420\\u00b5\\u0420\\u0405\\u0420\\u0451\\u0420\\u00b5, \\u0420\\u0491\\u0420\\u00bb\\u0421\\u040f Gauge \\u0421\\u0453\\u0421\\u0403\\u0421\\u201a\\u0420\\u00b0\\u0420\\u0405\\u0420\\u00b0\\u0420\\u0406\\u0420\\u00bb\\u0420\\u0451\\u0420\\u0406\\u0420\\u00b0\\u0420\\u00b5\\u0421\\u201a \\u0420\\u00b7\\u0420\\u0405\\u0420\\u00b0\\u0421\\u2021\\u0420\\u00b5\\u0420\\u0405\\u0420\\u0451\\u0420\\u00b5, \\u0420\\u0491\\u0420\\u00bb\\u0421\\u040f Summary \\u0420\\u0451 Histogram \\u0420\\u0406\\u0420\\u0405\\u0420\\u0455\\u0421\\u0403\\u0420\\u0451\\u0421\\u201a \\u0420\\u0406 \\u0420\\u0405\\u0420\\u00b0\\u0420\\u00b1\\u0420\\u00bb\\u0421\\u040b\\u0420\\u0491\\u0420\\u00b5\\u0420\\u0405\\u0420\\u0451\\u0421\\u040f\"}, {\"name\": \"metric_name\", \"type\": \"string\"}, {\"name\": \"metric_labels\", \"type\": {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"LabelMap\", \"fields\": [{\"name\": \"label\", \"type\": \"string\"}, {\"name\": \"lable_value\", \"type\": \"string\"}]}}, \"default\": []}, {\"name\": \"buckets\", \"type\": {\"type\": \"array\", \"items\": \"float\"}, \"doc\": \"\\u0420\\u0408\\u0421\\u0403\\u0421\\u201a\\u0420\\u00b0\\u0420\\u0405\\u0420\\u00b0\\u0420\\u0406\\u0420\\u00bb\\u0420\\u0451\\u0420\\u0406\\u0420\\u00b0\\u0420\\u00b5\\u0421\\u201a \\u0420\\u0491\\u0420\\u0451\\u0420\\u00b0\\u0420\\u0457\\u0420\\u00b0\\u0420\\u00b7\\u0420\\u0455\\u0420\\u0405\\u0421\\u2039 \\u0420\\u0491\\u0420\\u00bb\\u0421\\u040f \\u0421\\u201a\\u0420\\u0451\\u0420\\u0457\\u0420\\u00b0 Histogram\", \"default\": []}]}], \"default\": null}]}}, \"default\": []}]}"



def __read_file(file_name):
    with open(file_name, "r") as f:
        return f.read()

def __get_names_and_schema():
    names = avro_schema.Names()
    schema = make_avsc_object(json.loads(_STRING_SCHEMA_JSON), names)
    return names, schema

__NAMES, SCHEMA = __get_names_and_schema()
__SCHEMAS = {}
def get_schema_type(fullname):
    return __SCHEMAS.get(fullname)
__SCHEMAS = dict((n.fullname.lstrip("."), n) for n in six.itervalues(__NAMES.names))


class SchemaClasses(object):
    
    
    pass
    class com(object):
        class topkrabbensteam(object):
            class zm(object):
                class custom_metric(object):
                    class enums(object):
                        
                        class PrometheusMetricTypeClass(object):
                            
                            """
                            
                            """
                            
                            Counter = "Counter"
                            Gauge = "Gauge"
                            Histogram = "Histogram"
                            Summary = "Summary"
                            
                        pass
                class metrics(object):
                    
                    class MetricClass(DictWrapper):
                        
                        """
                        
                        """
                        
                        
                        RECORD_SCHEMA = get_schema_type("com.topkrabbensteam.zm.metrics.Metric")
                        
                        
                        def __init__(self, inner_dict=None):
                            super(SchemaClasses.com.topkrabbensteam.zm.metrics.MetricClass, self).__init__(inner_dict)
                            if inner_dict is None:
                                self.data_type = str()
                                self.data = SchemaClasses.com.topkrabbensteam.zm.metrics.MetricClass.RECORD_SCHEMA.fields[1].default
                                self.log_data = SchemaClasses.com.topkrabbensteam.zm.metrics.MetricClass.RECORD_SCHEMA.fields[2].default
                                self.metric_header = SchemaClasses.com.topkrabbensteam.zm.metrics.metric_header.MetricHeaderClass(_json_converter.from_json_object(SchemaClasses.com.topkrabbensteam.zm.metrics.MetricClass.RECORD_SCHEMA.fields[3].default, writers_schema=SchemaClasses.com.topkrabbensteam.zm.metrics.MetricClass.RECORD_SCHEMA.fields[3].type))
                                self.prometheus_metric_data = SchemaClasses.com.topkrabbensteam.zm.metrics.prometheus_metric.PrometheusMetricDataClass(_json_converter.from_json_object(SchemaClasses.com.topkrabbensteam.zm.metrics.MetricClass.RECORD_SCHEMA.fields[4].default, writers_schema=SchemaClasses.com.topkrabbensteam.zm.metrics.MetricClass.RECORD_SCHEMA.fields[4].type))
                        
                        
                        @property
                        def data_type(self):
                            """
                            :rtype: str
                            """
                            return self._inner_dict.get('data_type')
                        
                        @data_type.setter
                        def data_type(self, value):
                            #"""
                            #:param str value:
                            #"""
                            self._inner_dict['data_type'] = value
                        
                        
                        @property
                        def data(self):
                            """
                            :rtype: str
                            """
                            return self._inner_dict.get('data')
                        
                        @data.setter
                        def data(self, value):
                            #"""
                            #:param str value:
                            #"""
                            self._inner_dict['data'] = value
                        
                        
                        @property
                        def log_data(self):
                            """
                            :rtype: str
                            """
                            return self._inner_dict.get('log_data')
                        
                        @log_data.setter
                        def log_data(self, value):
                            #"""
                            #:param str value:
                            #"""
                            self._inner_dict['log_data'] = value
                        
                        
                        @property
                        def metric_header(self):
                            """
                            :rtype: SchemaClasses.com.topkrabbensteam.zm.metrics.metric_header.MetricHeaderClass
                            """
                            return self._inner_dict.get('metric_header')
                        
                        @metric_header.setter
                        def metric_header(self, value):
                            #"""
                            #:param SchemaClasses.com.topkrabbensteam.zm.metrics.metric_header.MetricHeaderClass value:
                            #"""
                            self._inner_dict['metric_header'] = value
                        
                        
                        @property
                        def prometheus_metric_data(self):
                            """
                            :rtype: SchemaClasses.com.topkrabbensteam.zm.metrics.prometheus_metric.PrometheusMetricDataClass
                            """
                            return self._inner_dict.get('prometheus_metric_data')
                        
                        @prometheus_metric_data.setter
                        def prometheus_metric_data(self, value):
                            #"""
                            #:param SchemaClasses.com.topkrabbensteam.zm.metrics.prometheus_metric.PrometheusMetricDataClass value:
                            #"""
                            self._inner_dict['prometheus_metric_data'] = value
                        
                        
                    class MetricsListClass(DictWrapper):
                        
                        """
                        
                        """
                        
                        
                        RECORD_SCHEMA = get_schema_type("com.topkrabbensteam.zm.metrics.MetricsList")
                        
                        
                        def __init__(self, inner_dict=None):
                            super(SchemaClasses.com.topkrabbensteam.zm.metrics.MetricsListClass, self).__init__(inner_dict)
                            if inner_dict is None:
                                self.metrics = list()
                        
                        
                        @property
                        def metrics(self):
                            """
                            :rtype: list[SchemaClasses.com.topkrabbensteam.zm.metrics.MetricClass]
                            """
                            return self._inner_dict.get('metrics')
                        
                        @metrics.setter
                        def metrics(self, value):
                            #"""
                            #:param list[SchemaClasses.com.topkrabbensteam.zm.metrics.MetricClass] value:
                            #"""
                            self._inner_dict['metrics'] = value
                        
                        
                    pass
                    class metric_header(object):
                        
                        class MetricHeaderClass(DictWrapper):
                            
                            """
                            
                            """
                            
                            
                            RECORD_SCHEMA = get_schema_type("com.topkrabbensteam.zm.metrics.metric_header.MetricHeader")
                            
                            
                            def __init__(self, inner_dict=None):
                                super(SchemaClasses.com.topkrabbensteam.zm.metrics.metric_header.MetricHeaderClass, self).__init__(inner_dict)
                                if inner_dict is None:
                                    self.source = str()
                                    self.source_type = str()
                                    self.requester_uri = SchemaClasses.com.topkrabbensteam.zm.metrics.metric_header.MetricHeaderClass.RECORD_SCHEMA.fields[2].default
                                    self.pushed_at = int()
                                    self.priority = str()
                                    self.level = str()
                            
                            
                            @property
                            def source(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('source')
                            
                            @source.setter
                            def source(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['source'] = value
                            
                            
                            @property
                            def source_type(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('source_type')
                            
                            @source_type.setter
                            def source_type(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['source_type'] = value
                            
                            
                            @property
                            def requester_uri(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('requester_uri')
                            
                            @requester_uri.setter
                            def requester_uri(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['requester_uri'] = value
                            
                            
                            @property
                            def pushed_at(self):
                                """
                                :rtype: int
                                """
                                return self._inner_dict.get('pushed_at')
                            
                            @pushed_at.setter
                            def pushed_at(self, value):
                                #"""
                                #:param int value:
                                #"""
                                self._inner_dict['pushed_at'] = value
                            
                            
                            @property
                            def priority(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('priority')
                            
                            @priority.setter
                            def priority(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['priority'] = value
                            
                            
                            @property
                            def level(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('level')
                            
                            @level.setter
                            def level(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['level'] = value
                            
                            
                        pass
                    class prometheus_metric(object):
                        
                        class LabelMapClass(DictWrapper):
                            
                            """
                            
                            """
                            
                            
                            RECORD_SCHEMA = get_schema_type("com.topkrabbensteam.zm.metrics.prometheus_metric.LabelMap")
                            
                            
                            def __init__(self, inner_dict=None):
                                super(SchemaClasses.com.topkrabbensteam.zm.metrics.prometheus_metric.LabelMapClass, self).__init__(inner_dict)
                                if inner_dict is None:
                                    self.label = str()
                                    self.lable_value = str()
                            
                            
                            @property
                            def label(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('label')
                            
                            @label.setter
                            def label(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['label'] = value
                            
                            
                            @property
                            def lable_value(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('lable_value')
                            
                            @lable_value.setter
                            def lable_value(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['lable_value'] = value
                            
                            
                        class PrometheusMetricDataClass(DictWrapper):
                            
                            """
                            this is custom metric that can be used by Prometheus Metrics Exporter Tool
                            """
                            
                            
                            RECORD_SCHEMA = get_schema_type("com.topkrabbensteam.zm.metrics.prometheus_metric.PrometheusMetricData")
                            
                            
                            def __init__(self, inner_dict=None):
                                super(SchemaClasses.com.topkrabbensteam.zm.metrics.prometheus_metric.PrometheusMetricDataClass, self).__init__(inner_dict)
                                if inner_dict is None:
                                    self.metric_type = SchemaClasses.com.topkrabbensteam.zm.custom_metric.enums.PrometheusMetricTypeClass.Counter
                                    self.metric_value = float()
                                    self.metric_name = str()
                                    self.metric_labels = list()
                                    self.buckets = list()
                            
                            
                            @property
                            def metric_type(self):
                                """
                                :rtype: SchemaClasses.com.topkrabbensteam.zm.custom_metric.enums.PrometheusMetricTypeClass
                                """
                                return self._inner_dict.get('metric_type')
                            
                            @metric_type.setter
                            def metric_type(self, value):
                                #"""
                                #:param SchemaClasses.com.topkrabbensteam.zm.custom_metric.enums.PrometheusMetricTypeClass value:
                                #"""
                                self._inner_dict['metric_type'] = value
                            
                            
                            @property
                            def metric_value(self):
                                """
                                :rtype: float
                                """
                                return self._inner_dict.get('metric_value')
                            
                            @metric_value.setter
                            def metric_value(self, value):
                                #"""
                                #:param float value:
                                #"""
                                self._inner_dict['metric_value'] = value
                            
                            
                            @property
                            def metric_name(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('metric_name')
                            
                            @metric_name.setter
                            def metric_name(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['metric_name'] = value
                            
                            
                            @property
                            def metric_labels(self):
                                """
                                :rtype: list[SchemaClasses.com.topkrabbensteam.zm.metrics.prometheus_metric.LabelMapClass]
                                """
                                return self._inner_dict.get('metric_labels')
                            
                            @metric_labels.setter
                            def metric_labels(self, value):
                                #"""
                                #:param list[SchemaClasses.com.topkrabbensteam.zm.metrics.prometheus_metric.LabelMapClass] value:
                                #"""
                                self._inner_dict['metric_labels'] = value
                            
                            
                            @property
                            def buckets(self):
                                """
                                :rtype: list[float]
                                """
                                return self._inner_dict.get('buckets')
                            
                            @buckets.setter
                            def buckets(self, value):
                                #"""
                                #:param list[float] value:
                                #"""
                                self._inner_dict['buckets'] = value
                            
                            
                        pass
                        
__SCHEMA_TYPES = {
'com.topkrabbensteam.zm.custom_metric.enums.PrometheusMetricType': SchemaClasses.com.topkrabbensteam.zm.custom_metric.enums.PrometheusMetricTypeClass,
    'com.topkrabbensteam.zm.metrics.Metric': SchemaClasses.com.topkrabbensteam.zm.metrics.MetricClass,
    'com.topkrabbensteam.zm.metrics.MetricsList': SchemaClasses.com.topkrabbensteam.zm.metrics.MetricsListClass,
    'com.topkrabbensteam.zm.metrics.metric_header.MetricHeader': SchemaClasses.com.topkrabbensteam.zm.metrics.metric_header.MetricHeaderClass,
    'com.topkrabbensteam.zm.metrics.prometheus_metric.LabelMap': SchemaClasses.com.topkrabbensteam.zm.metrics.prometheus_metric.LabelMapClass,
    'com.topkrabbensteam.zm.metrics.prometheus_metric.PrometheusMetricData': SchemaClasses.com.topkrabbensteam.zm.metrics.prometheus_metric.PrometheusMetricDataClass,
    
}
_json_converter = avrojson.AvroJsonConverter(use_logical_types=False, schema_types=__SCHEMA_TYPES)

