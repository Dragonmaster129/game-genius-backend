import math


def totalUp(objToTotal):
    total = 0
    try:
        for baseKey in objToTotal:
            if baseKey == "business":
                card1 = False
                card2 = False
                for iteration in objToTotal[baseKey]:
                    if iteration["name"] == "CARD1":
                        card1 = True
                    if iteration["name"] == "CARD2":
                        card2 = True
                for iteration in objToTotal[baseKey]:
                    if iteration["name"] == "CARD2" and card1:
                        total += iteration["value"]
                    if iteration["name"] == "CARD3" and card1 and card2:
                        total += iteration["value"]
            else:
                try:
                    try:
                        if baseKey == "loan":
                            total += objToTotal[baseKey]/10
                            total = math.floor(total)
                        else:
                            total += objToTotal[baseKey]
                    except:
                        raise TypeError
                except TypeError:
                    for smallObj in objToTotal[baseKey]:
                        try:
                            total += smallObj["value"]
                        except KeyError:
                            try:
                                total += smallObj["monthly"]
                            except KeyError:
                                try:
                                    total += smallObj["count"]*smallObj["costPer"]
                                except KeyError:
                                    pass
    except ValueError:
        print("error")
    return total
