from mongoConnection import mongoClient


def getPlayerData(email):
    db = mongoClient.client("cashflowDB")
    print(db["player"].find({"email": email})[0]["playerData"])
    return db["player"].find({"email": email})[0]["playerData"]
