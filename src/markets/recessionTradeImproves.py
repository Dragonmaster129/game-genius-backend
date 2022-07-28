def recessionTradeImproves(data, amount=30): # amount can be negative ### recession is negative
    for i in data["assets"]["realestate"]:
        i["value"] += i["size"] * amount


def checkNegative(data):
    assets = []
    for i in data["assets"]["realestate"]:
        if i["value"] < 0:
            assets.append(True)
        else:
            assets.append(False)
    return assets
