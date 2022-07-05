from mongoConnection import mongoClient


def getInitData(profession):
    db = mongoClient.client("cashflowDB")
    initialData = db["initialData"]
    returnData = initialData.find({"profession": profession})[0]
    returnData.pop("_id")
    return returnData
