from abc import ABC
from abc import abstractmethod
from .AbstractKafkaConfig import AbstractKafkaConfig
from ..implementation.localSchema.LocalSchemaHolder import LocalSchemaHolder

class AbstractKafkaSchemaRegistryUpdater(ABC):
    def __init__(self,kafkaConfig:AbstractKafkaConfig, localSchemaHolder:LocalSchemaHolder):
        self.kafkaConfig = kafkaConfig      
        self.localSchemaHolder=localSchemaHolder
            
    def updateLocalSchemaHolder(self, localSchemaHolder):
        self.localSchemaHolder = localSchemaHolder
    @abstractmethod
    def checkIfSchemaExists(self,schemaName):
        pass
    @abstractmethod
    def getKafkaSchemaVersion(self,schemaName):
        pass
    @abstractmethod
    def haveToUpdateKafkaSchema(self):
        pass
    @abstractmethod
    def updateKafkaSchema(self):
        pass
    @abstractmethod
    def getKafkaSchema(self,schemaName):
        pass