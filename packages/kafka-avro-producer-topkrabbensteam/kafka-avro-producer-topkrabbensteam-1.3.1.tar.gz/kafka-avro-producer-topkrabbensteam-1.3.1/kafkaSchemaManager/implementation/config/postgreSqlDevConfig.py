
from ...abstract.AbstractDatabaseConfig import AbstractDatabaseConfig
import os

class PostgreSqlDevConfig(AbstractDatabaseConfig):
    
    def getUser(self):
        return os.environ.get('POSTGRESQL_USER')

    def getPassword(self):
        return os.environ.get('POSTGRESQL_PASSWORD')

    def getDatabaseName(self):
        return os.environ.get('POSTGRESQL_DATABASE')

    def getPort(self):
        return os.environ.get('POSTGRESQL_PORT') or 5432

    def getHost(self):
        return os.environ.get('POSTGRESQL_URI')

    def getConnectionUrl(self):
        url = 'postgresql://{}:{}@{}:{}/{}'
        return url.format(self.getUser(), self.getPassword(), self.getHost(), self.getPort(), self.getDatabaseName())