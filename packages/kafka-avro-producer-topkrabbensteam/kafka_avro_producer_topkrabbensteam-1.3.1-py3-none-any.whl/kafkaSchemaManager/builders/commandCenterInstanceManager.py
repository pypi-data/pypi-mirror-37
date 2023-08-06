class CommandCenterHolder:
    def __init__(self, topicName, commandCenter):
        self.commandCenter = commandCenter
        self.topicName = topicName

class CommandCenterInstanceManager:
    commandCenterList=[]
    def __init__(self,commandCenterBuilder):
        self.commandCenterBuilder = commandCenterBuilder

    def fetchOrCreateCommandCenterByTopicName(self,topicName):
        for commandCenterHolder in self.commandCenterList:
            if commandCenterHolder.topicName == topicName:
                return commandCenterHolder.commandCenter
        newCommandCenterInstance = self.commandCenterBuilder.setTopic(topicName).BuildCommandCenter()
        self.commandCenterList.append(CommandCenterHolder(topicName,newCommandCenterInstance))
        return newCommandCenterInstance

