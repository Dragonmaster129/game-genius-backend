def buy(card, data, playerAction):
    if playerAction:
        name = card.pop("type")
        key = len(data["assets"][name])
        card["key"] = key + 1
        data["cash"] -= card["downpay"]
        data["assets"][name].append(card)

    return data
