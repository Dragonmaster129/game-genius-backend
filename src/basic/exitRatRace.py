def exitRace(data):
    if data["totalExpenses"]*2 < data["passive"]:
        return True
    else:
        return False
