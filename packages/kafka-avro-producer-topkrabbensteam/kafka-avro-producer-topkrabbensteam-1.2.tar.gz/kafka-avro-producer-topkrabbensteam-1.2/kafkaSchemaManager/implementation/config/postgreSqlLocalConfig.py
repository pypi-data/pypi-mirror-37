
from ...abstract.AbstractDatabaseConfig import AbstractDatabaseConfig

class PostgreSqlLocalConfig(AbstractDatabaseConfig):
    
    def getUser(self):
        return "serega"

    def getPassword(self):
        return "123"

    def getDatabaseName(self):
        return "parserSchemas"

    def getPort(self):
        return 5432

    def getHost(self):
        return "localhost"

    def getConnectionUrl(self):
        url = 'postgresql://{}:{}@{}:{}/{}'
        return url.format(self.getUser(), self.getPassword(), self.getHost(), self.getPort(), self.getDatabaseName())