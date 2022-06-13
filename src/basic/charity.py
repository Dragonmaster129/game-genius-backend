def getCharity(data):
    if data["cash"] >= data["totalIncome"] / 10:
        data["cash"] -= data["totalIncome"] / 10
        data["charity"] = 3
        return True
    else:
        return False


def turnEnd(data):
    if checkCharity(data):
        data["charity"] -= 1
        return True
    else:
        return False


def checkCharity(data):
    if data["charity"] > 0:
        return True
    else:
        return False
