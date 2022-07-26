from mongoConnection import getPlayerData, mongoClient
import json
import asyncio


class Player:
    def __init__(self, socket, playerData):
        self.socket = socket
        self.playerData = playerData
        self.beginningCard = {}

    def sendMsg(self, message):
        try:
            message.pop("_id")
        except KeyError:
            pass
        asyncio.create_task(self.socket.send_text(json.dumps(message)))

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

    def addBeginningCard(self, card):
        self.beginningCard = card
        for i in card:
            if i != "description" and i != "_id" and i != "ID" and i != "title":
                if i == "cash":
                    self.playerData["playerData"]["cash"] += card[i]
                    continue
                self.playerData["playerData"]["assets"][i] = card[i]
        self.sendMsg({"description": card["description"], "options": ["OK"]})


if __name__ == "__main__":
    player = Player(1234, getPlayerData.getPlayerData("test11@test.com"))
    player.saveData()
