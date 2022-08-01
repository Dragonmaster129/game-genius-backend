def borrowLoan(data, amount):
    data["expenses"]["loan"] = int(data["expenses"]["loan"])
    data["expenses"]["loan"] += amount
    data["cash"] += amount
