def payLoan(data, amount):
    data["expenses"]["loan"] -= amount
    data["cash"] -= amount
