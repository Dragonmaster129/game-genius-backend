def recessionTradeImproves(data, amount=30): # amount can be negative ### recession is negative
    for i in data["assets"]["realestate"]:
        i["value"] += i["size"] * amount
