from datamountaineer.schemaregistry.client import SchemaRegistryClient
from datamountaineer.schemaregistry.serializers import MessageSerializer, Util
from ...abstract.AbstractKafkaAvroProducer import AbstractKafkaAvroProducer


class KafkaAvroProducer(AbstractKafkaAvroProducer):    
    def produceMessage(self,message):     
        if(self.schema_id is None):
            encoded = self.serializer.encode_record_with_schema(self.topic, self.avro_schema, message)    
        else:
            encoded = self.serializer.encode_record_with_schema_id(self.schema_id, self.avro_schema, message)    
        self.producer.send_messages(self.topic, encoded)
    
    def changeTopic(self,topic):
        if (topic is not None):
            self.topic = topic
            self.schemaName = self.kafkaConfig.getSchemaByTopicName(self.topic)
            self.schema_id,self.avro_schema,self.schema_version = self.client.get_latest_schema(self.schemaName)
