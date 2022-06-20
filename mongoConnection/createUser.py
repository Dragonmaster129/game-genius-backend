from mongoConnection import authentication
import time


def createUser(email, pwd):
    playerData = {
        "email": email,
        "pwd": authentication.hashText(pwd),
        "gameID": 0,
        "createdDate": time.ctime(time.time()),
    }
    return playerData


user = createUser("test1@test.com", "RandomPassword")
