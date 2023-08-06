from ..localSchema import LocalSchemaHolder, LocalSchemaHolderFactory,JsonLocalSchemaLoader
from ..kafka.KafkaSchemaRegistryUpdater import KafkaSchemaRegistryUpdater
from ..kafka.KafkaAvroProducer import KafkaAvroProducer
from ..localSchema.JsonLocalSchemaLoader import JsonLocalSchemaLoader
from ..localSchema.LocalSchemaHolder import LocalSchemaHolder
from ..schema.SimpleNullStringRecordSchema import SimpleNullStringRecordSchema
from ..helpers.JsonFileSaver import JsonFileSaver
from ..helpers.JsonObjectSerializer import JsonObjectSerializer

from ..postgreBootstrap.parserKafkaSchemaHolder import ParserKafkaSchemaHolder
from ..postgreBootstrap.postgreSqlOperations import PostgreSqlOperations
from ..config.postgreSqlLocalConfig import PostgreSqlLocalConfig
from ..config.JsonKafkaConfig import JsonKafkaConfig

def CreateSchema(schemaName,  schemaFileName):
    localSchemaSaver = JsonFileSaver(schemaFileName,schemaName)
    localSchema = SimpleNullStringRecordSchema(schemaName)
    localSchema.addField("Email","Адрес электронной почты")
    localSchema.addField("ParserName","Название парсера")
    localSchema.addField("ParsedDate","Дата парсинга объявления")
    localSchema.addField("Address","Адрес")
    localSchema.addField("Video","Видеоматериалы")
    localSchema.addField("ShowcaseGlazing","Витринное остекление")
    localSchema.addField("PotentialObjectUsage","Потенциально возможное использование помещения (магазин, псн и т.п.)")
    localSchema.addField("Entrance","Расположение входа объекта предложения (отдельный и т.п.)")
    localSchema.addField("CeilingHeight","Высота потолков")
    localSchema.addField("ConstructionYear","Год постройки")
    localSchema.addField("DateCreate","Дата создания")
    localSchema.addField("AgencyFoundationDate","Дата создания агенства")
    localSchema.addField("CadastralNumber","Кадастровый номер")
    localSchema.addField("ObjectState","Состояние объекта (строящееся, проект, и т.п.)")
    localSchema.addField("BuildingClass","Класс здания (B, B+…)")
    localSchema.addField("AgencyAdvertsCount","Количество объявлений агентства")
    localSchema.addField("CommunalPaymentsIncluded","Включены или нет коммунальные платежи в стоимость")
    localSchema.addField("LocalPositionLine","Локальное месторасположение объекта предложения (линия)")
    localSchema.addField("Furniture","Наличие мебели")
    localSchema.addField("PartialRent","Возможно ли частичная аренда площади помещения")
    localSchema.addField("AgencyName","Название агентсва")
    localSchema.addField("BusinessCentreName","Название бизнес-центра")
    localSchema.addField("BuildingName","Название здания")
    localSchema.addField("AdvertName","Название объявления (общая информация)")
    localSchema.addField("Taxes","В каком виде происходит включение налога (с НДС, без НДС и т.п.)")
    localSchema.addField("ObjectType","Тип объекта (офис, здание, склад …)")
    localSchema.addField("Description","Комментарий к объявлению")
    localSchema.addField("ObjectArea","Площадь объекта")
    localSchema.addField("BuildingArea","Площадь здания")
    localSchema.addField("MinimumRentArea","Минимальное значение площади для аренды")
    localSchema.addField("ObjectOccupation","Занято или нет помещение")
    localSchema.addField("ObjectFinish","Состояние помещения (типовой ремонт, …)")
    localSchema.addField("RentPeriod","Срок аренды")
    localSchema.addField("Url","Ссылка на страницу")
    localSchema.addField("RentPriceForYear","Ставка аренды за метр в год")
    localSchema.addField("RentPriceForMonth","Ставка аренды за метр в месяц")
    localSchema.addField("ContactPhone","Контакнтый телефон или телефоны")
    localSchema.addField("AccountType","Владелец имущества (представитель). Агенство, Собственник")
    localSchema.addField("RentType","Тип аренды (прямая, субаренда…)")
    localSchema.addField("BuildingType","Тип здания")
    localSchema.addField("RealtyType","Тип недвижимости (коммерческая и т.п.)")
    localSchema.addField("RoomType","Тип помещения (магазин, офис…)")
    localSchema.addField("ContractType","Тип сделки (Аренда, Продажа…)")
    localSchema.addField("LandArea","площадь земельного участка")
    localSchema.addField("Photos","Набор ссылок на фотографии объекта, разделенные запятой")
    localSchema.addField("Price","Стоимость предложения")
    localSchema.addField("Floor","Этаж объекта предложения")
    localSchemaHolder = LocalSchemaHolder(True,schemaName,localSchema)
    localSchemaSaver.save(localSchemaHolder)
    return localSchemaHolder

