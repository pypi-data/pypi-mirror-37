from abc import ABC
from abc import abstractmethod
from .AbstractKafkaConfig import AbstractKafkaConfig
from kafka import KafkaClient,SimpleProducer
from datamountaineer.schemaregistry.client import SchemaRegistryClient
from datamountaineer.schemaregistry.serializers import MessageSerializer, Util

class AbstractKafkaAvroProducer(ABC):
    def __init__(self,topic,kafkaConfig:AbstractKafkaConfig):
        self.topic=topic        
        self.kafkaConfig = kafkaConfig
        kafka = KafkaClient(kafkaConfig.getKafkaBrokerIp())
        self.producer = SimpleProducer(kafka)
        self.client = SchemaRegistryClient(url=kafkaConfig.getSchemaRegistryUrl())
        self.serializer = MessageSerializer(self.client,False)
        if (topic is not None):
            self.schemaName = kafkaConfig.getSchemaByTopicName(self.topic)
            self.schema_id,self.avro_schema,self.schema_version = self.client.get_latest_schema(self.schemaName)
    
    @abstractmethod
    def changeTopic(self,topic):
        pass

    @abstractmethod
    def produceMessage(self,message):
        pass
