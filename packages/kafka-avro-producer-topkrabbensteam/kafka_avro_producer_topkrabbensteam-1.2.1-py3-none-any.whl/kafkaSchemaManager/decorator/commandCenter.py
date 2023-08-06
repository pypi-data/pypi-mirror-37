from ..implementation.schema.SimpleNullStringRecordSchema import SimpleNullStringRecordSchema
from ..implementation.config.JsonKafkaConfig import JsonKafkaConfig
from ..implementation.localSchema import LocalSchemaHolder, LocalSchemaHolderFactory,JsonLocalSchemaLoader
from ..implementation.kafka.KafkaSchemaRegistryUpdater import KafkaSchemaRegistryUpdater
from ..implementation.kafka.KafkaAvroProducer import KafkaAvroProducer

from ..abstract.AbstractKafkaConfig import AbstractKafkaConfig
from ..abstract.AbstractSchemaHolder import AbstractSchemaHolder
from ..abstract.AbstractKafkaSchemaRegistryUpdater import AbstractKafkaSchemaRegistryUpdater
from ..abstract.AbstractKafkaAvroProducer import AbstractKafkaAvroProducer
from ..abstract.AbstractSchemaSaver import AbstractSchemaSaver
from ..abstract.AbstractLocalSchemaLoader import AbstractLocalSchemaLoader


class CommandCenter:

    def SetUp(self,kafkaConfig:AbstractKafkaConfig,
              localSchemaHolder:AbstractSchemaHolder,
              kafkaSchemaOperations:AbstractKafkaSchemaRegistryUpdater,
              kafkaProducer:AbstractKafkaAvroProducer, 
              localSchemaSaver:AbstractSchemaSaver,
              localSchemaLoader:AbstractLocalSchemaLoader):
        self.kafkaConfig = kafkaConfig
        self.localSchemaHolder = localSchemaHolder
        self.kafkaSchemaOperations = kafkaSchemaOperations
        self.kafkaProducer = kafkaProducer
        self.localSchemaSaver = localSchemaSaver
        self.localSchemaLoader = localSchemaLoader

    def AddNullStringSchemaField(self,fieldName,documentation):
        self.localSchemaHolder.getSchema().addField(fieldName,["null","string"],documentation)

    def AddSchemaField(self,fieldName,fieldType, documentation):
        self.localSchemaHolder.getSchema().addField(fieldName,fieldType,documentation)


    def UpdateLocalSchemaAndThenUpdateServerKafkaSchema(self):
        self.UpdateLocalSchema()
        self.UpdateKafkaSchema()
        #mark schema as being updated already
        self.UpdateLocalSchema(False)

    def UpdateLocalSchema(self, markAsModified = True):
        if(markAsModified == True):
            self.localSchemaHolder.markAsModified()
        else:
            self.localSchemaHolder.markAsUnmodified()

        self.localSchemaSaver.save(self.localSchemaHolder)

    def FetchLocalSchema(self):
        return self.localSchemaHolder.getSchema()

    def GetCurrentKafkaSchema(self):
        return self.kafkaSchemaOperations.getKafkaSchema(self.localSchemaHolder.getSchemaName())

    def IsKafkaSchemaIsOutdated(self):
        return self.kafkaSchemaOperations.haveToUpdateKafkaSchema()

    def UpdateKafkaSchema(self):
        self.kafkaSchemaOperations.updateKafkaSchema()

    def ChangeKafkaProducerTopic(self, topic):
        self.kafkaProducer.changeTopic(topic)   
        self.localSchemaLoader.setSchemaName(topic)
        self.localSchemaHolder = self.localSchemaLoader.loadLocalSchema()
        self.kafkaSchemaOperations.updateLocalSchemaHolder(self.localSchemaHolder)

    def ProduceKafkaMessage(self,dictionaryMessage):
        self.kafkaProducer.produceMessage(dictionaryMessage)

    def GetCurrentKafkaProducer(self):
        return self.kafkaProducer

    def GetKafkaSchemaOperations(self):
        return self.kafkaSchemaOperations

    def GetLocalSchemaHolder(self):
        return self.localSchemaHolder

    
