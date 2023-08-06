kafka-avro-producer-topkrabbensteam
=========================
##### Kafka-avro-producer-topkrabbensteam.

Dedicated to work with Kafka (produce messages) using Apache Avro schemas.
It helps to maintain schema when it changes and implement schema update mechanism based on local schema, which can be stored either locally (as JSON file) or in a PostgreSQL database. Other implementations are possible via abstract class extensions

##### Installation:
	pip install kafka-avro-producer-topkrabbensteam
 
##### Usage:
	from kafkaSchemaManager.decorator.CommandCenterFactory import CommandCenterFactory
	from kafkaSchemaManager.decorator.commandCenterEnum import CommandCenterEnum
#### Create command center
    commandCenter = CommandCenterFactory.createCommandCenter(CommandCenterEnum.PostgreeSqlCommandCenter,
                                                         "testTopic",
                                                         JsonKafkaConfig("config.json"),
                                                         PostgreSqlLocalConfig(), 
                                                         None)
    
=========================
##### This package is dedicated to the bright future.
=========================
 



    