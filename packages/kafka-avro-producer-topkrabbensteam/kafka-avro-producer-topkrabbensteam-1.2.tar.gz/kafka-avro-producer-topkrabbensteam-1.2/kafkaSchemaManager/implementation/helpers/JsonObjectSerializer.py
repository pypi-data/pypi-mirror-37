from ...abstract.AbstractObjectSerializer import AbstractObjectSerializer
import json

class JsonObjectSerializer(AbstractObjectSerializer):
    def serializeObject(self,deserializedData):
            return json.dumps(deserializedData)
       
    def deserializeObject(self,serializedData):
            return json.loads(serializedData)
