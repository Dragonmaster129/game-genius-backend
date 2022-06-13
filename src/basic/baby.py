def addBaby(data):
    if data["expenses"]["child"][0]["count"] < 3:
        data["expenses"]["child"][0]["count"] += 1
        return "added child"
    else:
        return "max amount of children"


def childMarries(data, cost):
    if data["expenses"]["child"][0]["count"] > 0:
        data["expenses"]["child"][0]["count"] -= 1
        data["cash"] -= cost
        return "child married"
    else:
        return "no children"
