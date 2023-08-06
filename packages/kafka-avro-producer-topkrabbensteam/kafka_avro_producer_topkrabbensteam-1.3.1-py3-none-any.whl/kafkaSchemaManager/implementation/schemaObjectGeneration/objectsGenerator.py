import json
from avrogen import write_schema_files

class ObjectsGenerator:

    def __init__(self, parentDirectory, schemaAsJson):
        self.parentDirectory = parentDirectory
        self.schemaAsJson = schemaAsJson

    def generateObjects(self):            
            write_schema_files(self.schemaAsJson, self.parentDirectory)

