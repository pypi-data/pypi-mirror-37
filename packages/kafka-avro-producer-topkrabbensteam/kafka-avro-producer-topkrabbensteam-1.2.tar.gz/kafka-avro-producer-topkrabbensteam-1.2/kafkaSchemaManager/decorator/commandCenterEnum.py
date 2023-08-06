from enum import Enum

class CommandCenterEnum(Enum):
    LocalStorageCommandCenter = 0,
    PostgreeSqlCommandCenter = 1,
    LocalKafkaStorageCommandCenter = 2
