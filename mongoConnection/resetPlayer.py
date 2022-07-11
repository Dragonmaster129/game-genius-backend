from mongoConnection import mongoClient
from sampledata import initData


def initializePlayerData(email, initialData=None):
    if initialData is None:
        initialData = initData.getInitData("Doctor")
    db = mongoClient.client("cashflowDB")
    players = db["player"]
    players.update_one({"email": email}, {"$set": {"playerData": initialData}})


# initializePlayerData("test@test.com")
