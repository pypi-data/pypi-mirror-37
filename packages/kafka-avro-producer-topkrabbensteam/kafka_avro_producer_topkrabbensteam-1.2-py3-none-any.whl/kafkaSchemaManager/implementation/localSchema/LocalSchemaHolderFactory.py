
class LocalSchemaHolderFactory:
    def createLocalSchemaHolder(self,schemaHasBeenModified,schemaName,schema):
        return LocalSchemaHolder(schemaHasBeenModified,schemaName,schema)

    def getLocalSchemaHolder(self,schemaLoader):        
        return schemaLoader.loadLocalSchema()
