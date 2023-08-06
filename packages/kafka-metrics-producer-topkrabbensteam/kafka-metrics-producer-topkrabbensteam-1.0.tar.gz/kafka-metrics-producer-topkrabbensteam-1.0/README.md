kafka-metrics-producer-topkrabbensteam
=========================
##### Kafka-metrics-producer-topkrabbensteam.

    Library that can be used to produce metrics to Kafka using Apache Avro schemas

##### Installation:
	pip install kafka-metrics-producer-topkrabbensteam
 
##### Usage:
	from metricsFacade.filledFieldsMetric import FilledFieldsMetric
    from metricsFacade.metricsProducer import MetricsProducer
    from metricsFacade.advertCrawlTimeSecondsMetric import AdvertCrawlTimeSecondsMetric
    from metricsFacade.errorCounterMetric import ErrorCounterMetric
    from metricsFacade.errorCategory import ErrorCategory
    from metricsFacade.moduleName import ModuleName
    from metricsFacade.labelsList import LabelsList

#Metrics
    topicName = "metrics_data"
    metricsProducer = MetricsProducer(topicName, JsonKafkaConfig("config.json"))


    filledFieldMetric = FilledFieldsMetric(ModuleName.Parser.name)
    advertCrawlTime = AdvertCrawlTimeSecondsMetric(ModuleName.Crawler.name)
    errorMetric = ErrorCounterMetric(ModuleName.Crawler.name)
    
    while True:
        time.sleep(1)
        metricValue = (random.random()*100)   
    
        flag = (metricValue > (random.random()*100))
        
        siteLabelValue = "cian.ru" if flag else "drom.ru"
        errorCategoryLabel = ErrorCategory.ServerError.name if flag else ErrorCategory.NotFound.name
    
        
        filledFieldMetric.formMetric({"field":"1","data":"2","count":None, "zzz":1,"mmm":2.0, "f":True},{LabelsList.sourceName:siteLabelValue})
        advertCrawlTime.formMetric(metricValue,{LabelsList.sourceName:siteLabelValue})
        errorMetric.formMetric(errorCategoryLabel,{LabelsList.sourceName:siteLabelValue})
            
        print ('Producing metric: %(type)s %(site)s %(value)f' 
               % {"site": siteLabelValue,"value":metricValue,"type":filledFieldMetric.getMetric().prometheus_metric_data.metric_type})
            
        metricsProducer.AddMetric(filledFieldMetric)    
        metricsProducer.AddMetric(advertCrawlTime)
        metricsProducer.AddMetric(errorMetric)
        
        metricsProducer.ProduceMetrics()    
    
=========================
##### This package is dedicated to the bright future.
=========================
 



    