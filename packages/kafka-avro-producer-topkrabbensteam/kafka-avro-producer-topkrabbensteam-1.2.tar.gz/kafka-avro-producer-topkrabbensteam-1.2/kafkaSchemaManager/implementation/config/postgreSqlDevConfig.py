
from ...abstract.AbstractDatabaseConfig import AbstractDatabaseConfig
import os

class PostgreSqlDevConfig(AbstractDatabaseConfig):
    
    def getUser(self):
        return os.environ.get('POSTGRESQL_USER') or "authdb"

    def getPassword(self):
        return os.environ.get('POSTGRESQL_PASSWORD') or "Ietha7opiu6xaifuegeesheeNaelah"

    def getDatabaseName(self):
        return os.environ.get('POSTGRESQL_DATABASE') or "parser_schemas"

    def getPort(self):
        return os.environ.get('POSTGRESQL_PORT') or 5432

    def getHost(self):
        return os.environ.get('POSTGRESQL_URI') or "172.17.217.103"

    def getConnectionUrl(self):
        url = 'postgresql://{}:{}@{}:{}/{}'
        return url.format(self.getUser(), self.getPassword(), self.getHost(), self.getPort(), self.getDatabaseName())