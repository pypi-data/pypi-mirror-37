from abc import ABC
from abc import abstractmethod

class AbstractSchemaHolder(ABC):
    
    @abstractmethod
    def getSchemaName(self):
        pass
    
    @abstractmethod
    def getSchemaHasBeenModified(self):
        pass

    @abstractmethod
    def getSchema(self):
        pass

    @abstractmethod
    def markAsModified(self):
        pass

    @abstractmethod
    def markAsUnmodified(self):
        pass
