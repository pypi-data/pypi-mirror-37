from ..decorator.commandCenterEnum import CommandCenterEnum
from ..decorator.commandCenter import CommandCenter
from ..decorator.CommandCenterFactory import CommandCenterFactory

class CommandCenterBuilder:

    @staticmethod
    def getBuilder():
        return CommandCenterBuilder()

    def __init__(self):
        self.databaseConfig = None
        self.localSchemaStoragePath = None
        self.topicName = None
        self.kafkaConfig = None
        self.commandCenterId = None

    def BuildCommandCenter(self):
        return CommandCenterFactory.createCommandCenter(self.commandCenterId,self.topicName,self.kafkaConfig,self.databaseConfig,self.localSchemaStoragePath)

    def setTopic(self,topicName):
        self.topicName = topicName
        return self

    def setDatabaseConfig(self,databaseConfig):
        self.databaseConfig = databaseConfig
        return self

    def setKafkaConfig(self, kafkaConfig):
        self.kafkaConfig = kafkaConfig
        return self

    def setLocalSchemaStoragePath(self,localSchemaStoragePath):
        self.localSchemaStoragePath = localSchemaStoragePath
        return self

    def setCommandCenterId(self,commandCenterId):
        self.commandCenterId =commandCenterId
        return self