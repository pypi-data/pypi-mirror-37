from ...abstract.AbstractLocalSchemaLoader import AbstractLocalSchemaLoader
from ...abstract.AbstractKafkaConfig import AbstractKafkaConfig
from .LocalSchemaHolder import LocalSchemaHolder
from datamountaineer.schemaregistry.client import SchemaRegistryClient
import json
import io

class LocalSchemaLoaderFromKafka(AbstractLocalSchemaLoader):
    def __init__(self,kafkaConfig:AbstractKafkaConfig, schemaName):
        super().__init__(schemaName)
        self.kafkaConfig = kafkaConfig
        self.client= SchemaRegistryClient(url=kafkaConfig.getSchemaRegistryUrl())       

    def loadLocalSchema(self):
        schema_id,avro_schema,schema_version = self.client.get_latest_schema(self.schemaName)
        if avro_schema is None:
            raise Exception("Avro schema is not found, or does not exist!")

        from ..schema.AvroSchema import AvroSchema
        localSchema = LocalSchemaHolder(False,
                                        self.schemaName,
                                        AvroSchema(None,None).assignObject(avro_schema.to_json()) )
        return localSchema
