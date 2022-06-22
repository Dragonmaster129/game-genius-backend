from mongoConnection import mongoClient


def checkPlayersInGame(ID):
    db = mongoClient.client("cashflowDB")
    players = db["player"].find({"gameID": ID})
    playerList = []
    for i in players:
        playerList.append(i["email"])
    return playerList


print(checkPlayersInGame(0))
