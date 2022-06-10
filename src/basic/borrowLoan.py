def borrowLoan(data, amount):
    data["expenses"]["loan"] += amount
    data["cash"] += amount
