from abc import ABC
from abc import abstractmethod

class AbstractLocalSchemaLoader(ABC): 
    
    def __init__(self,schemaName):
        self.schemaName = schemaName

    
    def setSchemaName(self,schemaName):
        self.schemaName = schemaName

    @abstractmethod
    def loadLocalSchema(self):
        pass
