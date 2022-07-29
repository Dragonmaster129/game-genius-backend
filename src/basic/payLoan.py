def payLoan(data, amount):
    if amount <= data["cash"]:
        data["expenses"]["loan"] -= amount
        data["cash"] -= amount


def payNotBankLoan(data, type):
    if data["expenses"][type][0]["totalCost"] <= data["cash"]:
        data["cash"] -= data["expenses"][type][0]["totalCost"]
        data["expenses"][type][0] = {"monthly": 0, "totalCost": 0}
