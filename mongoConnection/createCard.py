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
#     market = {
#         "title": "Apartment Buyer",  # The bold words at the top of the card
#         "description": """Buyer offers $35,000 per unit for all units in apartment houses.
# Everyone may sell at this price.
# If you sell, pay off the related mortgage, and give up the net cash flow you currently receive on this property.""",  # exactly what is on the card telling you what to do
#         "type": "realestate",  # eg. realestate, stock, land, business, dividend, insurance, child marries, (CONTINUED.)
#         # pollution, natural disaster, CHARITY, mentor
#         "name": "APARTMENTCOMPLEX",  # eg. MYT4U, OK4U, 4-PLEX, STARTERHOUSE, APARTMENTCOMPLEX, ALL. What card affects
#         "highest": False, # when realestate, affects the highest value of property
#         "price": 35000, # eg. the stock price, what you are selling realestate for per unit, land. (CONTINUED.)
#         "forcedSale": False, # You have no choice but to sell.
#         "target": "All",  # eg. Player, player your right, everyone, right all, starts with you and moves to the right.
#     }
#     createCard(market, "market")
    cashflow = {
        "title": "8-plex for Sale",  # the bold words at the top of the card
        "description": """Great rental area. Low vacancy rate.
Use this for yourself or sell the opportunity.
48% ROI, may sell for $240,000 to $320,000
Cost: $200,000
Mortgage: $160,000
Down Pay: $40,000
Cash Flow: +$1,600""",  # the words on the card
        "type": "realestate",  # stock, realestate, land, business (D2Y)
        "name": "8-PLEX",  # MYT4U, OK4U, DUPLEX, STARTERHOUSE, LAND, CARD 1
        "card": {
            "type": "realestate",
            "name": "8-PLEX",
            "size": 8,
            "cost": 200000,
            "mortgage": 160000,
            "downpay": 40000,
            "value": 1600,
        },
    }
    createCard(cashflow, "cashflow")
    pass
