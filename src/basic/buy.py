from src.basic import borrowLoan
import math


def buy(card, data, playerAction, amount=1):
    if playerAction:
        type = card.pop("type")
        try:
            card.pop("_id")
        except KeyError:
            pass
        if type == "d2y":
            type = "business"
        if type == "royalty" or type == "dividend":
            type = "dividends"
        if type == "realestate deal":
            type = "realestate"
        key = len(data["assets"][type])
        if type == "stock":
            card["amount"] = amount
            if card["option"] != "SHORT":
                if data["cash"] - card["costPerShare"] * amount < 0:
                    loan = (card["costPerShare"] * amount) - data["cash"]
                    loan = math.ceil(loan/1000) * 1000
                    borrowLoan.borrowLoan(data, loan)
                data["cash"] -= card["costPerShare"] * amount
            if card["option"] == "PUT" or card["option"] == "CALL":
                card["turns"] = 3
        elif type != "business" or card["name"] == "CARD1":
            if type == "realestate" or type == "land":
                if data["cash"] < card["downpay"]:
                    loan = math.ceil((card["downpay"] - data["cash"])/1000)*1000
                    borrowLoan.borrowLoan(data, loan)
                data["cash"] -= card["downpay"]
            else:
                if data["cash"] < card["downpay"] * amount:
                    loan = math.ceil(((card["downpay"] * amount) - data["cash"])/1000) * 1000
                    borrowLoan.borrowLoan(data, loan)
                data["cash"] -= card["downpay"] * amount
        if type == "dividends":
            newcard = {"name": card["name"], "value": card["value"]*amount}
            card = newcard

        card["key"] = key + 1
        data["assets"][type].append(card)

    return data
