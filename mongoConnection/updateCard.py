from mongoConnection import mongoClient


def updateCard(cardData, collection, ID):
    db = mongoClient.client("cashflowDB")[collection]
    for i in cardData.keys():
        db.update_one({"ID": ID}, {"$set": {i: cardData[i]}})
