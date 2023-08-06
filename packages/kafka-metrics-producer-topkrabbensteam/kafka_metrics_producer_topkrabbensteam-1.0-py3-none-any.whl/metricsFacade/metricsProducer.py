from .kafkaMetricsSchema.com.topkrabbensteam.zm.metrics import MetricsList
from kafkaSchemaManager.decorator.CommandCenterFactory import CommandCenterFactory
from kafkaSchemaManager.decorator.commandCenterEnum import CommandCenterEnum

class MetricsProducer:
    def __init__(self, topicName, kafkaConfig):
        self.topicName = topicName
        self.kafkaConfig = kafkaConfig
        self.commandCenter = CommandCenterFactory.createCommandCenter(CommandCenterEnum.LocalKafkaStorageCommandCenter,
                                                         self.topicName,
                                                         kafkaConfig,
                                                         None, 
                                                         None)
        self.metricsData = MetricsList()


    def AddMetric(self,metric):
        self.metricsData.metrics.append(metric.getMetric())

    def CleanMetrics(self):
        self.metricsData.metrics.clear()

    def ProduceMetrics(self):
        self.commandCenter.ProduceKafkaMessage(self.metricsData)
        self.CleanMetrics()

    def GetMetricList(self):
        return self.metricsData

