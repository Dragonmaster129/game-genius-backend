def buy(card, data, playerAction, amount=1):
    if playerAction:
        type = card.pop("type")
        key = len(data["assets"][type])
        if type == "stock":
            card["amount"] = amount
            if card["option"] != "SHORT":
                data["cash"] -= card["costPerShare"] * amount
            if card["option"] == "PUT" or card["option"] == "CALL":
                card["turns"] = 3
        elif type != "business" or card["name"] == "CARD1":
            data["cash"] -= card["downpay"] * amount
        if type == "dividends":
            newcard = {"name": card["name"], "value": card["value"]*amount}
            card = newcard

        card["key"] = key + 1
        data["assets"][type].append(card)

    return data
