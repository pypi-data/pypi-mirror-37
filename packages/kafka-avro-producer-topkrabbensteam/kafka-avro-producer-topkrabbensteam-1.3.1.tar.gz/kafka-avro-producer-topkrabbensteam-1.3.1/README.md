kafka-avro-producer-topkrabbensteam
=========================
##### Kafka-avro-producer-topkrabbensteam.

Dedicated to work with Kafka (produce messages) using Apache Avro schemas.
It helps to maintain schema when it changes and implement schema update mechanism based on local schema, which can be stored either locally (as JSON file) or in a PostgreSQL database. Other implementations are possible via abstract class extensions

##### Installation:
	pip install kafka-avro-producer-topkrabbensteam
 
# Usage:

## Implement config classes based on AbstractKafkaConfig, AbstractDatabaseConfig
* AbstractDatabaseConfig - stands for database connection config
* AbstractKafkaConfig - stands for kafka connection config

## Select one of the following possibilities:

 * LocalStorageCommandCenter = 0, #stands for managing Avro Schema from local JSON file
 
 * PostgreeSqlCommandCenter = 1, #managing Avro Schema based on PostgreSQL database
 
 * LocalKafkaStorageCommandCenter = 2 #do not able to change schema, but can get it from Kafka and produce messages based on the present Kafaka schema
 
```python
from kafkaSchemaManager.decorator.CommandCenterFactory import CommandCenterFactory
from kafkaSchemaManager.decorator.commandCenterEnum import CommandCenterEnum

## Create command center
commandCenter = CommandCenterFactory.createCommandCenter(CommandCenterEnum.PostgreeSqlCommandCenter,
                                                         "testTopic",
                                                         JsonKafkaConfig("config.json"),
                                                         PostgreSqlLocalConfig(), 
                                                         None)

## Produce Avro message to Kafka
commandCenter.ProduceKafkaMessage({"Email":"seregae@e1.ru","ParserName": "must have", "myNewBrandField2": "Hello world"})

## Change Kafka schema runtime

#add a new field to a Kafka schema
commandCenter.AddNullStringSchemaField("jedi00087","my new command field")
#update it locally and on server
commandCenter.UpdateLocalSchemaAndThenUpdateServerKafkaSchema()
					
## Update local schema from JSON file
localSchemaJson = JsonLocalSchemaLoader("localMigrationTopic.json","testTopic").loadLocalSchema()
commandCenter.localSchemaHolder = localSchemaJson
commandCenter.UpdateLocalSchema()					
														 
## Check local schema (json base, database based etc.) and present Kafka schema

commandCenter.GetKafkaSchemaOperations().checkIfSchemaExists(schemaName)
commandCenter.IsKafkaSchemaIsOutdated()
														 
```
    
=========================
##### This package is dedicated to the bright future. 
=========================
 



    