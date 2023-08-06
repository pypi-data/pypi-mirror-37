from ...abstract import AbstractSchemaSaver
import json
import io
from ...abstract.AbstractDatabaseSchemaOperations import AbstractDatabaseSchemaOperations
from ...abstract.AbstractSchemaSaver import AbstractSchemaSaver
from ..postgreBootstrap.parserKafkaSchemaHolder import ParserKafkaSchemaHolder

class SqlPostgreLocalSchemaSaver(AbstractSchemaSaver):
    def __init__(self,schemaName, databaseOps:AbstractDatabaseSchemaOperations):
        super().__init__(schemaName)
        self.databaseOps = databaseOps

    def load(self):        
        return json.loads( self.databaseOps.getSchemaByName(self.schemaName).schemaJson )

    def save(self,object): 
        kafkaSchema = ParserKafkaSchemaHolder(object.getSchemaName(),object.toDict())
        self.databaseOps.updateSchema(kafkaSchema)
        