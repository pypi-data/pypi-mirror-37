from abc import ABC
from abc import abstractmethod

class AbstractSchemaSaver(ABC):
    def __init__(self,schemaName):
        self.schemaName = schemaName

    @abstractmethod
    def load(self):
        pass
    @abstractmethod
    def save(self,object):
        pass
