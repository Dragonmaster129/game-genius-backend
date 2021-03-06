from mongoConnection import mongoClient
from sampledata import initData
import random


def initializePlayerData(email, initialData=None):
    db = mongoClient.client("cashflowDB")
    if initialData is None:
        tmpList = db["initialData"].find({}, {"_id": 0, "profession": True})
        List = []
        iteration = 0
        while True:
            try:
                List.append(tmpList[iteration]["profession"])
                iteration += 1
            except IndexError:
                break
        initialData = initData.getInitData(random.choice(List))
    players = db["player"]
    players.update_one({"email": email}, {"$set": {"playerData": initialData}})


# initializePlayerData("test@test.com")
