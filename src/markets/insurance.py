def getInsurance(data, insuranceCostPerMonth):
    data["expenses"]["insurance"] = insuranceCostPerMonth
    return data


def checkInsurance(data):
    return data["expenses"]["insurance"] > 0
