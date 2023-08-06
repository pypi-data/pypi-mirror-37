from ..helpers.DictionarySerializerMethod import  DictionarySerializerMethod
import json

class AvroSchema(DictionarySerializerMethod):
    def __init__(self,schemaName,schemaType):
        self.type = schemaType
        self.name = schemaName   
        self.fields = []

    def isFieldExist(self,fieldName):
        for field in self.fields:
            if field["name"] == fieldName:
                return True
        return False
        
    def addField(self, fieldName, fieldType, doc=''):
        if(not self.isFieldExist(fieldName)):
            self.fields.append({"name":fieldName,"type":fieldType, "doc":doc,"default":None})
        
    def toJson(self):
        return json.dumps(self.__dict__)

    def toDict(self):
        return self.__dict__

    def assignObject(self,dict):
        self.__dict__ = dict
        return self
