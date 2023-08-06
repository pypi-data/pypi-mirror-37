from abc import ABC
from abc import abstractmethod

class AbstractObjectSerializer(ABC):
        @abstractmethod
        def serializeObject(self,deserializedData):
            pass
        @abstractmethod
        def deserializeObject(self,serializedData):
            pass
