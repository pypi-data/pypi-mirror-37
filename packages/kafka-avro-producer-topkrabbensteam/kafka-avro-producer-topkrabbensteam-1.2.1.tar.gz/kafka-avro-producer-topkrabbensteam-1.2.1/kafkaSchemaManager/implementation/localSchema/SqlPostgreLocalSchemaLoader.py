
from ...abstract.AbstractLocalSchemaLoader import AbstractLocalSchemaLoader
from .LocalSchemaHolder import LocalSchemaHolder
import json
import io
from ...abstract.AbstractDatabaseSchemaOperations import AbstractDatabaseSchemaOperations

class SqlPostgreLocalSchemaLoader(AbstractLocalSchemaLoader):
    def __init__(self, schemaName, databaseOps:AbstractDatabaseSchemaOperations):
        super().__init__(schemaName)
        self.databaseOps = databaseOps
        

    def loadLocalSchema(self):
            schema = self.databaseOps.getSchemaByName(self.schemaName)
            loadedSchema = schema.schemaJson 
            from ..schema.AvroSchema import AvroSchema
            localSchema = LocalSchemaHolder(loadedSchema["schemaHasBeenModified"],
                                            loadedSchema["schemaName"],
                                            AvroSchema(None,None).assignObject(loadedSchema["schema"]) )
            return localSchema