from src.basic import sell, borrowLoan
import math


def forcedSale(cardType, data, price):
    # cardType = ["stock", "OK4U"]
    # property = ["realestate", 1]
    i = cardType[0]
    if i == "stock" and i == cardType[0]:
        items = []
        for item in range(len(data["assets"][i])):
            if data["assets"][i][item]["name"] == cardType[1]:
                items.append(item)
        for item in items[::-1]:
            option = data["assets"]["stock"][item]["option"]
            if price == 0 and (option == "REGULAR" or option == "CALL"):
                data["assets"]["stock"].pop(item)
            elif price == 0 and (option == "SHORT" or option == "PUT"):
                sell.sell(["assets", "stock", item+1], data, True, price, data["assets"][i][item]["amount"])
            elif price != 0 and (option == "REGULAR" or option == "SHORT"):
                sell.sell(["assets", "stock", item+1], data, True, price, data["assets"][i][item]["amount"])
    if (i == "realestate" or i == "land") and i == cardType[0]:
        sell.sell(["assets", i, cardType[1]+1], data, True, price)

    if data["cash"] < 0:
        loan = 0 - data["cash"]
        loan = math.ceil(loan/1000)*1000
        borrowLoan.borrowLoan(data, loan)

    # print(data["assets"][i])
    # sell.sell(itemData, data, True, price)


def findHighest(data):
    highest = ["", 0]
    for i in data["assets"]:
        if i == "realestate" or i == "land":
            iteration = 0
            for item in data["assets"][i]:
                try:
                    if item["value"] > highest[2]:
                        highest = [i, iteration, item["value"]]
                    iteration += 1
                except IndexError:
                    highest = [i, iteration, item["value"]]
                    iteration += 1
    return highest
