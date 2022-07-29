import math
from src.basic import borrowLoan


def pollution(data, payFiftyK=False):
    if payFiftyK:
        if data["cash"] < 50000:
            loan = math.ceil((50000 - data["cash"])/1000) * 1000
            borrowLoan.borrowLoan(data, loan)
        data["cash"] -= 50000
    if not payFiftyK:
        highest = [0, 0]
        for i in data["assets"]:
            if i == "realestate":
                iteration = 0
                for item in data["assets"][i]:
                    try:
                        if item["value"] > highest[1]:
                            highest = [iteration, item["value"]]
                        iteration += 1
                    except IndexError:
                        highest = [iteration, item["value"]]
                        iteration += 1
        data["assets"]["realestate"].pop(highest[0])


def checkPollution(data):
    highest = ["", 0]
    for i in data["assets"]:
        if i == "realestate":
            iteration = 0
            for item in data["assets"][i]:
                try:
                    if item["value"] > highest[2]:
                        highest = [i, iteration, item["value"]]
                    iteration += 1
                except IndexError:
                    highest = [i, iteration, item["value"]]
                    iteration += 1
    return highest != ["", 0]
