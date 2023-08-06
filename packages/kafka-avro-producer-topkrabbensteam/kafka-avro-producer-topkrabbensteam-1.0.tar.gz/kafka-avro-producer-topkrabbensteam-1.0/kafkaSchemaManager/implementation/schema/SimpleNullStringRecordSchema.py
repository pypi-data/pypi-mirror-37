from .AvroSchema import AvroSchema

class SimpleNullStringRecordSchema(AvroSchema):
    def __init__(self, schemaName):        
        self.name = schemaName
        self.type = "record"
        super(SimpleNullStringRecordSchema, self).__init__(self.name, self.type)
        
    def addField(self, fieldName, doc=''):
        if(not self.isFieldExist(fieldName)):
            self.fields.append({"name":fieldName,"type":["null","string"], "doc":doc,"default":None})  
