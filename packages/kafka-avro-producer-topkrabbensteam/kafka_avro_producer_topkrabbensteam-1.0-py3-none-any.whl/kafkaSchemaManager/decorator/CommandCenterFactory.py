from .commandCenterEnum import CommandCenterEnum
from .commandCenter import CommandCenter


from ..implementation.localSchema import LocalSchemaHolder, LocalSchemaHolderFactory,JsonLocalSchemaLoader
from ..implementation.kafka.KafkaSchemaRegistryUpdater import KafkaSchemaRegistryUpdater
from ..implementation.kafka.KafkaAvroProducer import KafkaAvroProducer
from ..implementation.localSchema.JsonLocalSchemaLoader import JsonLocalSchemaLoader
from ..implementation.helpers.JsonFileSaver import JsonFileSaver
from ..implementation.helpers.JsonObjectSerializer import JsonObjectSerializer
#postgre imports
from ..implementation.localSchema.SqlPostgreLocalSchemaLoader import SqlPostgreLocalSchemaLoader
from ..implementation.localSchema.SqlPostgreLocalSchemaSaver import SqlPostgreLocalSchemaSaver
from ..implementation.postgreBootstrap.postgreSqlOperations import PostgreSqlOperations
from ..implementation.config.postgreSqlLocalConfig import PostgreSqlLocalConfig

#kafka loaders
from ..implementation.localSchema.LocalSchemaLoaderFromKafka import LocalSchemaLoaderFromKafka
from ..implementation.localSchema.DummyLocalSchemaSaver import DummyLocalSchemaSaver


class CommandCenterFactory:
       

    @staticmethod
    def createCommandCenter(commandCenterId, schemaName,kafkaConfig,databaseConfig, localSchemaStoragePath):
        commandCenter = CommandCenter()
        if(commandCenterId == CommandCenterEnum.LocalStorageCommandCenter):                        
            #loader
            localSchemaLoader = JsonLocalSchemaLoader(localSchemaStoragePath,schemaName)            
            kafkaSchemaOperations = KafkaSchemaRegistryUpdater(kafkaConfig,None)
            kafkaProducer  = KafkaAvroProducer(None,kafkaConfig)            
            #saver
            localSchemaSaver = JsonFileSaver(localSchemaStoragePath,schemaName)
            commandCenter.SetUp(kafkaConfig,None,kafkaSchemaOperations,kafkaProducer,localSchemaSaver,localSchemaLoader)
            commandCenter.ChangeKafkaProducerTopic(schemaName)        
            return commandCenter
       
        if(commandCenterId == CommandCenterEnum.PostgreeSqlCommandCenter):
            postgreOperations = PostgreSqlOperations(databaseConfig)
            postgreOperations.openDatabase()            
            localSchemaLoader = SqlPostgreLocalSchemaLoader(schemaName,postgreOperations)
            kafkaSchemaOperations = KafkaSchemaRegistryUpdater(kafkaConfig,None)
            kafkaProducer  = KafkaAvroProducer(None,kafkaConfig)      
            localSchemaSaver = SqlPostgreLocalSchemaSaver(schemaName,postgreOperations)
            commandCenter.SetUp(kafkaConfig,None,kafkaSchemaOperations,kafkaProducer,localSchemaSaver,localSchemaLoader)
            commandCenter.ChangeKafkaProducerTopic(schemaName)
            return commandCenter

        if(commandCenterId == CommandCenterEnum.LocalKafkaStorageCommandCenter):
            localSchemaLoader = LocalSchemaLoaderFromKafka(kafkaConfig,schemaName)
            kafkaSchemaOperations = KafkaSchemaRegistryUpdater(kafkaConfig,None)
            kafkaProducer  = KafkaAvroProducer(None,kafkaConfig)      
            localSchemaSaver = DummyLocalSchemaSaver(schemaName)
            commandCenter.SetUp(kafkaConfig,None,kafkaSchemaOperations,kafkaProducer,localSchemaSaver,localSchemaLoader)
            commandCenter.ChangeKafkaProducerTopic(schemaName)
            return commandCenter