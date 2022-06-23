from mongoConnection import mongoClient, resetPlayer


def getPlayerData(email):
    db = mongoClient.client("cashflowDB")
    try:
        playerData = db["player"].find({"email": email})[0]["playerData"]
        playerData.pop("_id")
        return playerData
    except KeyError:
        resetPlayer.initializePlayerData(email)
        playerData = db["player"].find({"email": email})[0]["playerData"]
        playerData.pop("_id")
        return playerData
