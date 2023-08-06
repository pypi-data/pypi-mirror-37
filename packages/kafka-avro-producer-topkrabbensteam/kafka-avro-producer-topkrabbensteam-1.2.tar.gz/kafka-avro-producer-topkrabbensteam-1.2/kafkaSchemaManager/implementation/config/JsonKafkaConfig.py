from ...abstract.AbstractKafkaConfig import AbstractKafkaConfig
import json
import io

class JsonKafkaConfig(AbstractKafkaConfig):
    def __init__(self,configPath):
        with open(configPath, 'r') as f:
            self.config = json.load(f)
    def getSchemaRegistryUrl(self):
        return self.config["KAFKA"]["KAFKA_SCHEMA_REGISTRY_URL"]
        
    def getKafkaBrokerIp(self):
        return self.config["KAFKA"]["KAFKA_BROKER_IP"]
        
    def getTopicBySchemaName(self,schemaName):
        return schemaName
    
    def getSchemaByTopicName(self,topicName):
        return topicName      

    