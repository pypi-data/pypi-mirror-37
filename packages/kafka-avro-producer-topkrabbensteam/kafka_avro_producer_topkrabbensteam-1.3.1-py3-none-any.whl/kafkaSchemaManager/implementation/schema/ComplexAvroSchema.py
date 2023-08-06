from ..helpers.DictionarySerializerMethod import  DictionarySerializerMethod
import json

class ComplexAvroSchema(DictionarySerializerMethod):
    def __init__(self,schemaList):
        self.schemaList = schemaList      
        
    def toJson(self):
        return json.dumps(self.__dict__["schemaList"])

    def toDict(self):
        return self.__dict__["schemaList"]
    
