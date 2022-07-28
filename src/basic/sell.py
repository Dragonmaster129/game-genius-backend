from src import resetKeyValues


def sell(itemData, data, playerAction, price, amount=1):
    if playerAction:
        exitingData = data[itemData[0]][itemData[1]].pop(itemData[2]-1)
        if itemData[1] == "realestate":
            data["cash"] += (price * exitingData["size"]) - exitingData["mortgage"]
        if itemData[1] == "land":
            exitingData["size"] -= amount
            try:
                data["cash"] += price - exitingData["mortgage"]
                exitingData.pop("mortgage")
                exitingData.pop("value")
            except KeyError:
                data["cash"] += price
            if exitingData["size"] > 0:
                data[itemData[0]][itemData[1]].append(exitingData)
        if itemData[1] == "stock":
            if amount == 0:
                amount = exitingData["amount"]
            if exitingData["option"] == "REGULAR":
                data["cash"] += (price * amount)
                exitingData["amount"] -= amount
                if exitingData["amount"] > 0:
                    data[itemData[0]][itemData[1]].append(exitingData)
            if exitingData["option"] == "PUT":
                data["cash"] += (exitingData["strikePrice"] - price) * exitingData["amount"]
            if exitingData["option"] == "CALL":
                data["cash"] += (price - exitingData["strikePrice"]) * exitingData["amount"]
            if exitingData["option"] == "SHORT":
                data["cash"] += (exitingData["strikePrice"] - price) * exitingData["amount"]

    data[itemData[0]][itemData[1]] = resetKeyValues.resetKeyValues(data[itemData[0]][itemData[1]])

    return data
