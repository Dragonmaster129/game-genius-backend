from src import totalUp

externalData = {
    "totalIncome": 13200,
    "totalExpenses": 9650,
    "passive": 0,
    "cashflow": 3550,
    "cash": None,
    "player": 3,
    "profession": "Doctor",
    "auditor": "Sam",
    "savings": 400,
    "assets": {
        "salary": 13200,
        "interest": [
            {"name": "thingy", "value": 40, "key": 1},
            {"name": "notherone", "value": 50, "key": 2},
            {"name": "notherone", "value": 50, "key": 3},
            {"name": "notherone", "value": 50, "key": 4},
            {"name": "notherone", "value": 50, "key": 5},
        ],
        "dividends": [
            {"name": "2Big", "value": 30, "key": 1}
        ],
        "realestate": [
            {
                "name": "STARTERHOUSE",
                "size": 1,
                "cost": 55000,
                "mortgage": 50000,
                "downpay": 5000,
                "value": 200,
                "key": 1,
            },
            {
                "name": "STARTERHOUSE",
                "size": 1,
                "cost": 55000,
                "mortgage": 48000,
                "downpay": 7000,
                "value": 400,
                "key": 2,
            },
            {
                "name": "4-PLEX",
                "size": 4,
                "cost": 55000,
                "mortgage": 48000,
                "downpay": 7000,
                # "value": 400,
                "key": 3,
            },
        ],
        "land": [
            {
                "name": "Land",
                "size": 20,
                "cost": 30000,
                "mortgage": 15000,
                "downpay": 15000,
                "value": -150,
                "key": 1
            }
        ],
        "business": [
            # {
            #     "name": "CARD1",
            #     "cost": 200,
            #     "downpay": 200,
            #     "key": 1
            # },
            # {
            #     "name": "CARD2",
            #     "value": 500
            # }
        ],
        "stock": [
            {"name": "OK4U", "option": "PUT", "turns": 2, "amount": 1000, "strikePrice": 40, "costPerShare": 1,
             "key": 1},
            {"name": "OK4U", "option": "REGULAR", "amount": 1000, "costPerShare": 1, "key": 2},
            {"name": "OK4U", "option": "CALL", "turns": 3, "amount": 1000, "strikePrice": 15, "costPerShare": 1,
             "key": 3},
            {"name": "MYT4U", "option": "SHORT", "amount": 1000, "strikePrice": 50, "key": 4}
        ],
    },
    "expenses": {
        "taxes": 3420,
        "mortgage": {"monthly": 1900, "totalCost": 202000},
        "school": {"monthly": 750, "totalCost": 150000},
        "car": {"monthly": 380, "totalCost": 19000},
        "creditCard": {"monthly": 270, "totalCost": 9000},
        "retail": {"monthly": 50, "totalCost": 1000},
        "other": 2880,
        "child": {
            "count": 0,
            "costPer": 640,
        },
        "loan": 0,
        "insurance": 0,
    },
}


def updateData(data):
    data["totalIncome"] = totalUp.totalUp(data["assets"])
    data["totalExpenses"] = totalUp.totalUp((data["expenses"]))
    data["passive"] = totalUp.totalUp(data["assets"])-data["assets"]["salary"]
    data["cashflow"] = data["totalIncome"]-data["totalExpenses"]
    if data["cash"] is None:
        data["cash"] = data["cashflow"] + data["savings"]
