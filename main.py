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
from mongoConnection import playerLogin, getPlayerData, resetPlayer, mongoClient, createCard
from src.basic import paycheck
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


class DoodadCard(BaseModel):
    cardType: str
    cashflow: int
    cash: int
    baby: bool
    cashflowType: str
    token: str
    description: str


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


@app.delete("/end-game")
async def deleteGame():
    # TODO when the game is over/no players been in for a long time, delete the game
    pass


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


@app.post("/card/add/doodad")
async def addCardData(cardData: DoodadCard):
    if cardData.token in authTokens:
        createCard.createCard(cardData, "doodad")
        return True
    return False


@app.post("/start-game")
async def startGame(res: GetID):
    ID = res.ID
    currentGame = loadCurrentGame(ID)
    currentGame.startGame()
    return res


@app.post("/paycheck")
async def Paycheck(ID: GetID):
    playerData = getPlayerData.getPlayerData(tokens[ID.ID])["playerData"]
    paycheck.paycheck(playerData)
    db["player"].update_one({"email": tokens[ID.ID]}, {"$set": {"playerData": playerData}})
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
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.post("/choice/Sell")
async def buyCard(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    sellItem = currentGame.findFirstValue(currentGame.currentCard["name"])
    currentGame.sellCard(sellItem, currentGame.currentCard["price"], IDs.amount, currentGame.currentCard["name"])
    if currentGame.currentAction == "CAPITALGAIN" or currentGame.currentAction == "CASHFLOW":
        currentGame.changeAction("MARKET")
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
    return getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
