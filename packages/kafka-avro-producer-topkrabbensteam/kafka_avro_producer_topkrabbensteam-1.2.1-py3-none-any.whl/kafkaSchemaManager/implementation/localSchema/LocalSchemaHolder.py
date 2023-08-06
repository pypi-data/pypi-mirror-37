from ..helpers.DictionarySerializerMethod import DictionarySerializerMethod
from ...abstract.AbstractSchemaHolder import AbstractSchemaHolder

class LocalSchemaHolder(DictionarySerializerMethod,AbstractSchemaHolder):
    def __init__(self,schemaHasBeenModified,schemaName,schema):
        self.schemaHasBeenModified = schemaHasBeenModified
        self.schemaName = schemaName
        self.schema = schema

    def toDict(self):
        objectAsDictionary =  self.__dict__.copy()
        objectAsDictionary["schema"] = self.schema.toDict()
        return objectAsDictionary

    def getSchemaName(self):
        return self.schemaName  
    
    def getSchemaHasBeenModified(self):
        return self.schemaHasBeenModified
   
    def getSchema(self):
        return self.schema

    def markAsModified(self):
        self.schemaHasBeenModified = True

    def markAsUnmodified(self):
        self.schemaHasBeenModified = False
