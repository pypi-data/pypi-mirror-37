from ...abstract.AbstractSchemaSaver import AbstractSchemaSaver
import json
import io

class JsonFileSaver(AbstractSchemaSaver):
    def __init__(self,path,schemaName):
        super().__init__(schemaName)
        self.path = path

    def load(self):
        with open(self.path,'r') as file:            
            return json.loads(file.read())

    def save(self,object):
        with open(self.path,'w') as file:
            json.dump(object.toDict(),file)