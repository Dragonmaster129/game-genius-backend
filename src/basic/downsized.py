import math
from src.basic import borrowLoan


def downsized(data):
    if data["cash"] < data["totalExpenses"]:
        loan = math.ceil((data["totalExpenses"] - data["cash"])/1000)*1000
        borrowLoan.borrowLoan(data, loan)
    data["cash"] -= data["totalExpenses"]
    data["downsized"] = 2
    return True


def decreaseDownsized(data):
    if data["downsized"] > 0:
        data["downsized"] -= 1
        return True
    else:
        return False
