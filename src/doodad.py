def doodad(data, cash=None, cashflow=None, category=None):
    # data = self.data
    # cash = how much you need to pay in now
    # cashflow = how much you pay in monthly and if there is a cost then you need to add it to card
    # category = which area does the doodad count in, such as, Mortgage, Car Payment, etc.
    if cash is not None:
        data["cash"] -= cash
    if cashflow is not None:
        if category is None or category == "other":
            data["expenses"]["other"] += cashflow
        elif category is not None:
            data["expenses"][category].append({})
            for i in cashflow:
                data["expenses"][category][len(data["expenses"][category])-1][i] = cashflow[i]
    if category == "GOOD":
        data["cash"] += 5000
        data["downsizedImmunity"] = 1

    return data
