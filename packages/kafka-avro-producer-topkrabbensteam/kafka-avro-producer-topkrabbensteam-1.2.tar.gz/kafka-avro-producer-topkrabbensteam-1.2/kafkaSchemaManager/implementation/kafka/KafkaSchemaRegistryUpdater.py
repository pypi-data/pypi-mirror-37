from ...abstract import AbstractKafkaSchemaRegistryUpdater,AbstractKafkaConfig
from ..localSchema.LocalSchemaHolder import LocalSchemaHolder
import avro.schema
from datamountaineer.schemaregistry.client import SchemaRegistryClient
from datamountaineer.schemaregistry.serializers import MessageSerializer, Util
from kafka import KafkaClient

class KafkaSchemaRegistryUpdater(AbstractKafkaSchemaRegistryUpdater):
    def __init__(self,kafkaConfig:AbstractKafkaConfig, localSchemaHolder:LocalSchemaHolder):
        super().__init__(kafkaConfig,localSchemaHolder)
        self.client= SchemaRegistryClient(url=kafkaConfig.getSchemaRegistryUrl())

    def checkIfSchemaExists(self,schemaName):
        schema_id,avro_schema,schema_version = self.client.get_latest_schema(schemaName)
        if schema_id is None:
            return False
        return True       
        
    def getKafkaSchema(self,schemaName):
        schema_id,avro_schema,schema_version = self.client.get_latest_schema(schemaName)
        return avro_schema

    def getKafkaSchemaVersion(self,schemaName):
        schema_id,avro_schema,schema_version = self.client.get_latest_schema(schemaName)
        return schema_version

    def haveToUpdateKafkaSchema(self):
        updateFlag = self.localSchemaHolder.schemaHasBeenModified
        schemaName = self.localSchemaHolder.schemaName
        kafkaVersion = self.getKafkaSchemaVersion(schemaName)

        if(kafkaVersion is None):
            return True

        if updateFlag == True:
            return True
        return False


    def updateKafkaSchema(self):
        if self.haveToUpdateKafkaSchema():
            self.client.register(self.localSchemaHolder.schemaName, 
                                 avro.schema.Parse(self.localSchemaHolder.schema.toJson()))
            

