from mongoConnection import authentication, mongoClient
import time


def createUser(email, pwd):
    playerData = {
        "email": email,
        "pwd": authentication.hashText(pwd),
        "gameID": 0,
        "createdDate": time.ctime(time.time()),
    }
    db = mongoClient.client("cashflowDB")
    playerCol = db["player"]

    try:
        if playerCol.find({"email": email})[0]:
            return "Email Duplicate"
    except IndexError:
        playerCol.insert_one(playerData)
    return playerData


# # create 10 unique users
# for i in range(10):
#     user = createUser(f"test{i}@test.com", "RandomPassword")
#     print(user)
