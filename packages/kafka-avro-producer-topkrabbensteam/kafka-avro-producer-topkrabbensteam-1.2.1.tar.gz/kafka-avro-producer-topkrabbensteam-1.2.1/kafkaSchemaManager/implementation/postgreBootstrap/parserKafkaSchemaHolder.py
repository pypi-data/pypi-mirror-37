
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, String ,DateTime,Integer,PrimaryKeyConstraint 
from .base import Base
import datetime

class ParserKafkaSchemaHolder(Base):
    __tablename__ = 'parsingKafkaSchemas'
    id=Column(Integer, primary_key=True, autoincrement=True)
    schemaName = Column(String)
    schemaJson = Column(JSONB)
    dateUpdated = Column(DateTime)

    def __init__(self, schemaName, schemaJson):
        self.schemaName = schemaName
        self.schemaJson = schemaJson
        self.dateUpdated = datetime.datetime.now()
    
