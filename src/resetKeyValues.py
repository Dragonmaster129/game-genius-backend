def resetKeyValues(array):
    instance = 0
    for i in array:
        instance += 1
        i["key"] = instance

    return array
