from mongoConnection import mongoClient
import uuid


def createCard(cardData, collection):
    db = mongoClient.client("cashflowDB")[collection]
    ID = uuid.uuid4().hex
    db.insert_one({"ID": ID})
    for i in cardData.keys():
        print(i)
        print(cardData[i])
        db.update_one({"ID": ID}, {"$set": {i: cardData[i]}})
    print(cardData)


if __name__ == "__main__":
    createCard({"description": "YOU CAN'T SAY NO!", "cash": 20, "cashflow": 200, "category": "other"}, "doodad")
