from mongoConnection import mongoClient


def deleteCard(collection, ID):
    db = mongoClient.client("cashflowDB")[collection]
    print(db.delete_one({"ID": ID}))
