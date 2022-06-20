from mongoConnection import mongoClient


def getInitData(profession):
    db = mongoClient.client("cashflowDB")
    initialData = db["initialData"]
    return initialData.find({"profession": profession})[0]
