import math


def totalUp(objToTotal):
    total = 0
    try:
        for baseKey in objToTotal:
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
                try:
                    for smallObj in objToTotal[baseKey]:
                        try:
                            total += smallObj["value"]
                            # print(smallObj)
                        except KeyError:
                            pass
                except TypeError:
                    obj = objToTotal[baseKey]
                    try:
                        total += obj["monthly"]
                    except KeyError:
                        total += obj["count"]*obj["costPer"]
    except ValueError:
        print("error")
    return total
