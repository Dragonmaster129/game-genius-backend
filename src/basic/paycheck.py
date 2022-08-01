from src.basic import borrowLoan
import math


def paycheck(data):
    if 0-data["cashflow"] > data["cash"]:
        amount = 0-data["cashflow"] - data["cash"]
        amount = math.ceil(amount/1000) * 1000
        borrowLoan.borrowLoan(data, amount)
    data["cash"] += data["cashflow"]
