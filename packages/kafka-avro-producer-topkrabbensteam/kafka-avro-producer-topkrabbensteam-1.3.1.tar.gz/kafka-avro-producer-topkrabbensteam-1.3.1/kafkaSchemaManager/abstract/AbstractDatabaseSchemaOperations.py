from abc import ABC
from abc import abstractmethod
from .AbstractDatabaseConfig import AbstractDatabaseConfig


class AbstractDatabaseSchemaOperations(ABC):

    def __init__(self,config:AbstractDatabaseConfig):
        self.config = config

    @abstractmethod
    def openDatabase(self):
        pass

    @abstractmethod
    def closeDatabase(self):
        pass

    @abstractmethod
    def saveDatabaseChanges(self):
        pass

    @abstractmethod
    def addSchema(self,schema):
        pass

    @abstractmethod
    def getSchemaByName(self, schemaName):
        pass

    @abstractmethod
    def updateSchema(self,schema):
        pass
   