
from ..config.postgreSqlLocalConfig import PostgreSqlLocalConfig

from ...abstract.AbstractDatabaseConfig import AbstractDatabaseConfig
from .parserKafkaSchemaHolder import ParserKafkaSchemaHolder
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .base import Base
import datetime
from ...abstract.AbstractDatabaseSchemaOperations import AbstractDatabaseSchemaOperations


import sqlalchemy

class PostgreSqlOperations(AbstractDatabaseSchemaOperations):

    def __init__(self, config:AbstractDatabaseConfig):
        super().__init__(config)
        self.engine = create_engine(self.config.getConnectionUrl())
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)


    def saveDatabaseChanges(self):
        self.session.commit()

    
    def openDatabase(self):
        self.session = self.Session()

    def closeDatabase(self):
        self.session.close()      

    def addSchema(self,schema):    
        if(self.getSchemaByName(schema.schemaName) is None):
            self.session.add(schema)
            self.session.commit()
            return True
        return False

    def getSchemaByName(self, schemaName):
        return self.session.query(ParserKafkaSchemaHolder) \
        .filter(ParserKafkaSchemaHolder.schemaName == schemaName) \
        .first()

    def updateSchema(self,schema):
        if not self.addSchema(schema):
           schemaDb = self.getSchemaByName(schema.schemaName)
           schemaDb.schemaName = schema.schemaName
           schemaDb.schemaJson = schema.schemaJson
           schemaDb.dateUpdated = datetime.datetime.now()
           self.session.commit()



        