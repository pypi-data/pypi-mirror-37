from abc import ABC
from abc import abstractmethod
class AbstractKafkaConfig(ABC):
    @abstractmethod
    def getSchemaRegistryUrl(self):
        pass
    @abstractmethod
    def getKafkaBrokerIp(self):
        pass
    @abstractmethod
    def getTopicBySchemaName(self,schemaName):
        pass
    @abstractmethod
    def getSchemaByTopicName(self,topicName):
        pass
