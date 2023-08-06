from abc import ABC
from abc import abstractmethod

class AbstractDatabaseConfig(ABC):
    
    @abstractmethod
    def getUser(self):
        pass

    @abstractmethod
    def getPassword(self):
        pass

    @abstractmethod
    def getDatabaseName(self):
        pass

    @abstractmethod
    def getPort(self):
        pass

    @abstractmethod
    def getHost(self):
        pass

    @abstractmethod
    def getConnectionUrl(self):
        pass