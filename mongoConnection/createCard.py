from mongoConnection import mongoClient
import uuid


def createCard(cardData, collection):
    db = mongoClient.client("cashflowDB")[collection]
    ID = uuid.uuid4().hex
    try:
        if db.find({"ID": ID})[0]:
            createCard(cardData, collection)
    except IndexError:
        db.insert_one({"ID": ID})
        for i in cardData.keys():
            db.update_one({"ID": ID}, {"$set": {i: cardData[i]}})


# list of collections in DB
# beginning
# capitalgain
# cashflow
# doodad
# game
# initialData
# market
# player



if __name__ == "__main__":
    # createCard({"description": "Description 50", "cash": 20, "cashflow": 200, "category": "other"}, "doodad")
    # createCard({"description": "Words that make the capital", "deleteThis": 1}, "cashflow")
#     capitalGain = {
#         "title": "Stock -- OK4U Drug Co.",
#         "description": """Only you, or a Puts or Calls owner, may buy or short this stock.
# Everyone may sell.
# Short sellers must buy now.
# Symbol OK4U
# Today's price: $5
# No dividend (Yield or ROI = 0%)
# Prior trading range: $10 to $40""",
#         "type": "stock",
#         "name": "OK4U",
#         "card": {
#             "type": "stock",
#             "name": "OK4U",
#             "option": "REGULAR",
#             "costPerShare": 5,
#         }
#     }
#     createCard(capitalGain, "capitalgain")
    market = {
        "title": "House Buyer",
        "description": """Buyer offers $75,000 for a "starter house" (2 bedroom/1 bath). Has own financing.
Everyone may sell at this price.
If you sell, pay off the related mortgage, and give up the net cash flow you currently receive on this property""",
        "type": "realestate",  # eg. realestate, stock, land, business, dividend, insurance, child marries, (CONTINUED.)
        # pollution, natural disaster, CHARITY, mentor
        "name": "STARTERHOUSE",  # eg. MYT4U, OK4U, 4-PLEX, STARTERHOUSE, APARTMENTCOMPLEX, ALL. What card affects
        "highest": False,  # when realestate, affects the highest value of property
        "price": 75000,  # eg. the stock price, what you are selling realestate for per unit, land. (CONTINUED.)
        # when child marries pay amount.
        "forcedSale": False,  # You have no choice but to sell.
        "target": "Player",  # eg. Player, player your right, everyone, right all, starts with you and moves to the right.
    }
    createCard(market, "market")
    pass
