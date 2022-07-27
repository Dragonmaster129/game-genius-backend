from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import uuid
from bson import json_util
import copy
import time
import threading

from sampledata import data
from pydantic import BaseModel
from mongoConnection import playerLogin, getPlayerData, resetPlayer, mongoClient, createCard, deleteCard
from src.objects import game
# from src import totalUp

# App initialization
app = FastAPI()

externalData = copy.deepcopy(data.externalData)
data.updateData(externalData)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8080/play",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = mongoClient.client("cashflowDB")


class LoginData(BaseModel):
    email: str
    password: str


class AddCard(BaseModel):
    token: str
    card: object
    cardType: str


class BeginningCard(BaseModel):
    token: str
    title: str
    description: str
    cash: int
    stock: list
    realestate: list


class CreateGame(BaseModel):
    player: str
    name: str


class GetID(BaseModel):
    ID: str


class GetCard(BaseModel):
    ID: str
    gameID: str


class GetChoice(GetCard):
    amount: int


tokens = {"1": "test@test.com", "31f29295f838405ca6d9eaa37e287f2f": "test@test.com"}
authTokens = {"1": "test@test.com"}
websockets = {}
professions = []
temps = db["initialData"]
temp = temps.find({})
for i in temp:
    professions.append(i["profession"])

# beginning
# capitalgain
# cashflow
# doodad
# game
# initialData
# markets
# player


def deleteGames():
    while True:
        time.sleep(60)
        gameList = db["game"].find({}, {"_id": 0, "ID": True, "timeStamp": True})
        for Game in gameList:
            try:
                if time.time() - Game["timeStamp"] > 2 * 60 * 60 * 24 * 7:
                    db.game.delete_one({"ID": Game["ID"]})
            except KeyError:
                db.game.delete_one({"ID": Game["ID"]})


deleteThread = threading.Thread(target=deleteGames, daemon=True)
deleteThread.start()


def loadCurrentGame(gameID):
    currentGame = game.Game(gameID, [])
    currentGame.loadSaveData(websockets)
    return currentGame


@app.get("/data/{tokenID}")
async def getData(tokenID):
    if tokenID in tokens:
        return json_util.dumps(getPlayerData.getPlayerData(tokens[tokenID]))
    return "invalid token"


@app.get("/getcard")
async def getCard(auth: str = 0, ID: str = 0, collection: str = ""):
    if auth in tokens:
        card = db[collection].find({"ID": ID})[0]
        card.pop("_id")
        return card
    return False


@app.delete("/delete-card")
async def DeleteCard(auth: str = 0, ID: str = 0, collection: str = ""):
    if auth in tokens:
        deleteCard.deleteCard(collection, ID)
        return True
    return False



@app.get("/cards")
async def getCards():
    beginning = db["beginning"].find()
    capitalgain = db["capitalgain"].find()
    cashflow = db["cashflow"].find()
    doodad = db["doodad"].find()
    initialData = db["initialData"].find()
    market = db["market"].find()
    allCards = {"beginning": [], "capitalgain": [], "cashflow": [], "doodad": [], "initialData": [], "market": []}
    for i in beginning:
        i.pop("_id")
        allCards["beginning"].append(i)
    for i in capitalgain:
        i.pop("_id")
        allCards["capitalgain"].append(i)
    for i in cashflow:
        i.pop("_id")
        allCards["cashflow"].append(i)
    for i in doodad:
        i.pop("_id")
        allCards["doodad"].append(i)
    for i in initialData:
        i.pop("_id")
        allCards["initialData"].append(i)
    for i in market:
        i.pop("_id")
        allCards["market"].append(i)
    return allCards


@app.get("/game")
async def getPlayersCurrentGame(ID: GetID):
    return db["player"].find({"email": tokens[ID.ID]}, {"_id": 0, "gameID": True})[0]["gameID"]


@app.get("/games")
async def getGames():
    gameList = db["game"].find({"gameStarted": False})
    newGameList = []
    for i in gameList:
        i.pop("_id")
        newGameList.append(i)
    newGameList.reverse()
    # TODO sort through the data and return a list
    return newGameList


@app.post("/create-game")
async def createGame(Game: CreateGame):
    # TODO get the data and create the game
    # choose the ID randomly and create a player list. Append the players to the player list and
    # have the player list at the start have the number of players that it is limited to.
    gameID = uuid.uuid4().hex
    db["game"].insert_one({
        "name": Game.name,
        "ID": gameID,
        "timeStamp": time.time(),
        "playerList": [tokens[Game.player]],
        "currentAction": "STARTGAME",
        "currentCard": {},
        "currentTarget": 0,
        "currentTurn": 0,
        "beginningOrder": [],
        "capitalOrder": [],
        "cashflowOrder": [],
        "doodadOrder": [],
        "marketOrder": [],
        "gameStarted": False,
    })
    return json.dumps({"name": Game.name, "ID": gameID})


@app.post("/login")
async def login(request: LoginData):
    time.sleep(1)
    if playerLogin.login(request.email, request.password):
        token = uuid.uuid4().hex
        tokens[token] = request.email
        if playerLogin.auth(request.email):
            authTokens[token] = request.email
            return json.dumps([token, 1])
        return json.dumps([token, 0])
    else:
        return False


@app.post("/reset/{tokenID}/")
async def reset(tokenID):
    if tokenID in tokens:
        resetPlayer.initializePlayerData(tokens[tokenID])
        return True
    return False


@app.post("/card/add")
async def addCardData(cardData: AddCard):
    if cardData.token in authTokens:
        card = cardData.card
        createCard.createCard(card, cardData.cardType)
        return True
    return False


@app.post("/start-game")
async def startGame(res: GetID):
    ID = res.ID
    currentGame = loadCurrentGame(ID)
    currentGame.startGame()
    return res


@app.post("/paycheck")
async def Paycheck(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.receivePaycheck()
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.post("/capitalGain")
async def capitalGain(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.changeAction("CAPITALGAIN")
    currentGame.drawCard()
    currentGame.saveData()
    currentCard = currentGame.sendPlayerTheirOptions()
    return currentCard


@app.post("/cashflow")
async def capitalGain(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.changeAction("CASHFLOW")
    currentGame.drawCard()
    currentGame.saveData()
    currentCard = currentGame.sendPlayerTheirOptions()
    return currentCard


@app.post("/doodad")
async def capitalGain(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.changeAction("DOODAD")
    currentGame.drawCard()
    currentGame.saveData()
    currentCard = currentGame.sendPlayerTheirOptions()
    return currentCard


@app.post("/market")
async def capitalGain(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.changeAction("MARKET")
    currentGame.drawCard()
    currentGame.saveData()
    currentCard = currentGame.sendPlayerTheirOptions()
    return currentCard


@app.post("/charity")
async def capitalGain(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.changeAction("CHARITY")
    currentGame.saveData()
    return {"EVENT": "Got charity"}


@app.post("/baby")
async def capitalGain(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.changeAction("BABY")
    currentGame.saveData()
    return {"EVENT": "Got baby"}


@app.post("/downsized")
async def capitalGain(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.changeAction("DOWNSIZED")
    currentGame.saveData()
    return {"EVENT": "Got downsized"}


@app.post("/end-turn")
async def endTurn(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.nextTurn()
    return {"EVENT": "ENDTURN"}


@app.post("/choice/Buy")
async def buyCard(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.buyItem(currentGame.currentCard["card"], IDs.amount)
    if currentGame.currentAction == "CAPITALGAIN" or currentGame.currentAction == "CASHFLOW":
        currentGame.changeAction("MARKET")
    else:
        currentGame.changeAction("ENDTURN")
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.post("/choice/Take")
async def takeCard(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    try:
        currentGame.REUpgrade(currentGame.currentCard["newProperty"], currentGame.currentCard["name"])
    except KeyError:
        pass
    currentGame.changeAction("ENDTURN")
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.post("/choice/Sell")
async def sellCard(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    if IDs.amount != 0:
        sellItem = currentGame.findFirstValue(currentGame.currentCard["name"])
        if currentGame.currentCard["name"] == "PLEX":
            for i in ["DUPLEX", "4-PLEX", "8-PLEX"]:
                sellItem = currentGame.findFirstValue(i)
                currentGame.sellCard(sellItem, currentGame.currentCard["price"], IDs.amount, currentGame.currentCard["name"])
        try:
            currentGame.sellCard(sellItem, currentGame.currentCard["price"], IDs.amount, currentGame.currentCard["name"])
        except KeyError:
            currentGame.sellCard(sellItem, currentGame.currentCard["card"]["costPerShare"], IDs.amount, currentGame.currentCard["name"])
    if currentGame.currentAction == "CAPITALGAIN" or currentGame.currentAction == "CASHFLOW":
        currentGame.changeAction("MARKET")
    else:
        currentGame.changeAction("ENDTURN")
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.post("/choice/Short")
async def shortCard(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    if currentGame.currentAction == "CAPITALGAIN" or currentGame.currentAction == "CASHFLOW":
        currentGame.changeAction("MARKET")
    else:
        currentGame.changeAction("ENDTURN")
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.websocket("/joinGame")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        res = await websocket.receive_text()
        # await websocket.send_text(f"Message text was: {res}")
        res = json.loads(res)
        # print(res)
        websockets[tokens[res[0]]] = websocket
        db["player"].update_one({"ID": tokens[res[0]]}, {"$set": {"gameID": res[1]}})
        resetPlayer.initializePlayerData(tokens[res[0]])


@app.post("/choice/{slug}")
async def doNothing(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    if currentGame.currentAction == "CAPITALGAIN" or currentGame.currentAction == "CASHFLOW":
        currentGame.changeAction("MARKET")
    elif currentGame.currentAction == "STARTTURN":
        pass
    else:
        currentGame.changeAction("ENDTURN")
    return getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
