from mongoConnection import mongoClient, resetPlayer


def getPlayerData(email):
    db = mongoClient.client("cashflowDB")
    try:
        playerData = db["player"].find({"email": email})[0]
        playerData.pop("_id")
        playerData.pop("pwd")
        return playerData
    except KeyError:
        resetPlayer.initializePlayerData(email)
        playerData = db["player"].find({"email": email})[0]
        playerData.pop("_id")
        playerData.pop("pwd")
        return playerData
