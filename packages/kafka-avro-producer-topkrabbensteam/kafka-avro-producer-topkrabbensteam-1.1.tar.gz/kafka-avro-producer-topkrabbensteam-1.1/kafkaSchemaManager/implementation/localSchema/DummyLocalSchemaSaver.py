from ...abstract.AbstractSchemaSaver import AbstractSchemaSaver
import json
import io

class DummyLocalSchemaSaver(AbstractSchemaSaver):
    def __init__(self,schemaName):
        super().__init__(schemaName)        

    def load(self):
        return None

    def save(self,object):
        pass