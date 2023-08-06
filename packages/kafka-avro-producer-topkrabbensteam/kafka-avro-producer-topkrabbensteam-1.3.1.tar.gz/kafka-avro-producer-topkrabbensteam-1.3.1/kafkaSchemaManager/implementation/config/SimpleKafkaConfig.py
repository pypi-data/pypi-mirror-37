from ...abstract.AbstractKafkaConfig import AbstractKafkaConfig
import json
import io


class SimpleKafkaConfig(AbstractKafkaConfig):
    def __init__(self, schemaRegistry, kafkaIp):
        self.kafkaIp = kafkaIp
        self.schemaRegistry = schemaRegistry

    def getSchemaRegistryUrl(self):
        return self.schemaRegistry

    def getKafkaBrokerIp(self):
        return self.kafkaIp

    def getTopicBySchemaName(self, schemaName):
        return schemaName

    def getSchemaByTopicName(self, topicName):
        return topicName

