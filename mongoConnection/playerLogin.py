from mongoConnection import mongoClient, authentication


def login(email, password):
    db = mongoClient.client("cashflowDB")
    player = db["player"].find({"email": email})[0]
    if authentication.matchHashedText(player["pwd"], password):
        return True
    else:
        return False


def auth(email):
    db = mongoClient.client("cashflowDB")
    player = db["player"].find({"email": email})[0]
    if player["auth"] == 1:
        return True
    else:
        return False


# loginSuccessful = login("test@test.com", "RandomPassword")
# if loginSuccessful:
#     print("Logged in successfully")
# else:
#     print("Failed login, bad credentials")
