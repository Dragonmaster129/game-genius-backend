from src import resetKeyValues


def upgrade(change, data, requiredType, changing=None):
    changingIsRequiredType = False
    if changing is None:
        for i in data["assets"]["realestate"]:
            if i["name"] == requiredType:
                changingIsRequiredType = True
    else:
        changingIsRequiredType = data["assets"]["realestate"][changing-1]["name"] == requiredType
    if changingIsRequiredType and change is None:
        return True
    elif not changingIsRequiredType and change is None:
        return False
    elif changingIsRequiredType and change is not None:
        data["assets"]["realestate"].pop(changing-1)
        data["assets"]["realestate"].append(change)

    resetKeyValues.resetKeyValues(data["assets"]["realestate"])
