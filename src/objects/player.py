from mongoConnection import getPlayerData, mongoClient


class Player:
    def __init__(self, socket, playerData):
        self.socket = socket
        self.playerData = playerData

    def sendMsg(self, message):
        # TODO figure out how to send the message
        pass

    def saveData(self, collection=None):
        if collection is None:
            collection = mongoClient.client("cashflowDB")["player"]
        playerData = self.playerData["playerData"]
        collection.update_one({"email": self.playerData["email"]},
                              {"$set": {"playerData": playerData,
                                        "gameID": self.playerData["gameID"]}})
        # print(self.playerData.keys())

    def reassignSocket(self):
        # TODO find out how to reassign socket
        pass


if __name__ == "__main__":
    player = Player(1234, getPlayerData.getPlayerData("test11@test.com"))
    player.saveData()
