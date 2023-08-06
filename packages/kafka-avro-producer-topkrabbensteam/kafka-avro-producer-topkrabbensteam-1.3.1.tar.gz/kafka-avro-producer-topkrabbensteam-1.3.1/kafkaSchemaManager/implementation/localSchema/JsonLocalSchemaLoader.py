from ...abstract.AbstractLocalSchemaLoader import AbstractLocalSchemaLoader
from .LocalSchemaHolder import LocalSchemaHolder
import json
import io

class JsonLocalSchemaLoader(AbstractLocalSchemaLoader):
    def __init__(self,path, schemaName):
        super().__init__(schemaName)
        self.path = path
        

    def loadLocalSchema(self):
        with open(self.path,'r') as file:            
            loadedSchema = json.loads(file.read())
            from ..schema.AvroSchema import AvroSchema
            from ..schema.ComplexAvroSchema import ComplexAvroSchema

            if loadedSchema["schema"] is None:
                raise Exception("Avro schema is not found, or does not exist!")

            schema = None
            if type(loadedSchema["schema"] ) == list:
                schema = ComplexAvroSchema(loadedSchema["schema"])
            else:
                schema = AvroSchema(None,None).assignObject(loadedSchema["schema"])

            localSchema = LocalSchemaHolder(loadedSchema["schemaHasBeenModified"],
                                            loadedSchema["schemaName"],
                                             schema)
            return localSchema
