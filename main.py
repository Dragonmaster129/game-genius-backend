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
from mongoConnection import playerLogin, getPlayerData, resetPlayer, mongoClient, createCard, deleteCard, \
    updateCard, createUser
from src.objects import game
# from src import totalUp

# App initialization
app = FastAPI()

externalData = copy.deepcopy(data.externalData)
data.updateData(externalData)

origins = [
    "http://192.168.1.99.tiangolo.com",
    "https://192.168.1.99.tiangolo.com",
    "http://192.168.1.99",
    "http://192.168.1.99:8080",
    "https://jcp-game-genius-frontend.herokuapp.com.tiangolo.com",
    "https://jcp-game-genius-frontend.herokuapp.com",
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


class UpdateCard(AddCard):
    cardID: str


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


class GetSellChoice(BaseModel):
    ID: str
    gameID: str
    amount: int
    sellItem: list


class GetLoanChoice(BaseModel):
    ID: str
    gameID: str
    loanType: str
    amount: int


tokens = {}
authTokens = {}
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


@app.get("/")
async def Init():
    return "Base state"


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


@app.patch("/card/update")
async def UpdateCard(update: UpdateCard):
    if update.token in tokens:
        updateCard.updateCard(update.card, update.cardType, update.cardID)


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
    return newGameList


@app.post("/create-game")
async def createGame(Game: CreateGame):
    # choose the ID randomly and create a player list. Append the players to the player list and
    # have the player list at the start have the number of players that it is limited to.
    gameID = uuid.uuid4().hex
    db["game"].insert_one({
        "name": Game.name,
        "ID": gameID,
        "timeStamp": time.time(),
        "playerList": [],
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
        return json.dumps([token, 0])
    else:
        return False


@app.post("/signup")
async def signup(request: LoginData):
    time.sleep(1)
    player = createUser.createUser(request.email, request.password)
    if player == "Email Duplicate":
        return 1
    return 2


@app.post("/auth")
async def auth(request: LoginData):
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
    currentGame.sendPlayerTheirOptions()
    currentGame.saveData()
    return True


@app.post("/cashflow")
async def capitalGain(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.changeAction("CASHFLOW")
    currentGame.drawCard()
    currentGame.sendPlayerTheirOptions()
    currentGame.saveData()
    return True


@app.post("/doodad")
async def capitalGain(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.changeAction("DOODAD")
    currentGame.drawCard()
    currentGame.sendPlayerTheirOptions()
    currentGame.saveData()
    return True


@app.post("/market")
async def capitalGain(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.changeAction("MARKET")
    currentGame.drawCard()
    currentGame.sendPlayerTheirOptions()
    currentGame.saveData()
    return True


@app.post("/charity")
async def capitalGain(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.changeAction("CHARITY")
    currentCard = currentGame.sendPlayerCharityOptions()
    currentGame.saveData()
    return currentCard


@app.post("/baby")
async def capitalGain(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.changeAction("BABY")
    currentCard = currentGame.sendPlayerBabyOptions()
    currentGame.saveData()
    return currentCard


@app.post("/downsized")
async def capitalGain(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.changeAction("DOWNSIZED")
    currentCard = currentGame.sendPlayerDownsizedOptions()
    currentGame.saveData()
    return currentCard


@app.post("/end-turn")
async def endTurn(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.nextTurn()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])
    currentGame.saveData()
    return playerData


@app.post("/pay-back-loan")
async def payBackLoan(IDs: GetCard):
    currentGame = loadCurrentGame(IDs.gameID)
    email = tokens[IDs.ID]
    for i in range(len(currentGame.playerList)):
        if currentGame.playerList[i].playerData["email"] == email:
            currentGame.currentTarget = i
    return currentGame.getLiabilities()


@app.post("/pay-for-loan")
async def payForLoan(ID: GetLoanChoice):
    currentGame = loadCurrentGame(ID.gameID)
    currentGame.payBackLoan(ID.loanType, ID.amount)
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[ID.ID])["playerData"]
    return playerData


@app.post("/choice/Buy")
async def buyCard(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    try:
        currentGame.buyItem(currentGame.currentCard["card"], IDs.amount)
    except KeyError:
        currentGame.buyItem(currentGame.currentCard, IDs.amount)
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
async def sellCard(IDs: GetSellChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    email = tokens[IDs.ID]
    for i in range(len(currentGame.playerList)):
        if currentGame.playerList[i].playerData["email"] == email:
            currentGame.currentTarget = i
    try:
        currentGame.sellCard(IDs.sellItem, currentGame.currentCard["price"], currentGame.currentCard["size"])
    except KeyError:
        currentGame.sellCard(IDs.sellItem, currentGame.currentCard["card"]["costPerShare"], IDs.amount)
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.post("/choice/Short")
async def shortCard(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    try:
        card = copy.deepcopy(currentGame.currentCard["card"])
    except KeyError:
        card = copy.deepcopy(currentGame.currentCard)
    card["option"] = "SHORT"
    currentGame.buyItem(card, IDs.amount)
    if currentGame.currentAction == "CAPITALGAIN" or currentGame.currentAction == "CASHFLOW":
        currentGame.changeAction("MARKET")
    else:
        currentGame.changeAction("ENDTURN")
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.post("/choice/OK")
async def OKCard(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    try:
        if currentGame.currentAction == "DOODAD":
            currentGame.doodad(currentGame.currentCard["cash"], currentGame.currentCard["cashflow"], currentGame.currentCard["category"])
        elif currentGame.currentAction == "BABY":
            currentGame.getBaby()
        elif currentGame.currentAction == "DOWNSIZED":
            currentGame.downsizedCurrentPlayer()
        elif currentGame.currentCard["type"] == "Trade Improves/Recession Strikes":
            currentGame.recessionTradeImproves(currentGame.currentCard["amount"])
    except KeyError:
        pass
    email = tokens[IDs.ID]
    if email == currentGame.getEmailList()[currentGame.currentTarget]:
        if currentGame.currentAction != "STARTTURN":
            currentGame.changeAction("ENDTURN")
        currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.post("/sellNegative")
async def sellNegative(IDs: GetSellChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    email = tokens[IDs.ID]
    for i in range(len(currentGame.playerList)):
        if currentGame.playerList[i].playerData["email"] == email:
            currentGame.currentTarget = i
    currentGame.sellNegative(IDs.sellItem)
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.post("/choice/Get Option")
async def getOptionOnRealEstate(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.getOption()
    currentGame.changeAction("MARKET")
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.post("/choice/Give")
async def GiveCard(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.getCharity()
    currentGame.changeAction("ENDTURN")
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.post("/choice/Insure")
async def insurePlayer(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.getInsurance(currentGame.currentCard["cost"])
    currentGame.changeAction("ENDTURN")
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.post("/choice/Pay")
async def pay50K(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.pollutionHitsPLayerToRightAll(True)
    currentGame.changeAction("ENDTURN")
    currentGame.saveData()
    playerData = getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
    return playerData


@app.post("/choice/Lose")
async def loseProperty(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    currentGame.pollutionHitsPLayerToRightAll(False)
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
        websockets[tokens[res[0]]] = websocket
        playerList = db["game"].find({"ID": res[1]})[0]["playerList"]
        playerList.append(tokens[res[0]])
        db["game"].update_one({"ID": res[1]}, {"$set": {"playerList": playerList}})
        db["player"].update_one({"ID": tokens[res[0]]}, {"$set": {"gameID": res[1]}})
        resetPlayer.initializePlayerData(tokens[res[0]])


@app.post("/choice/{slug}")
async def doNothing(IDs: GetChoice):
    currentGame = loadCurrentGame(IDs.gameID)
    email = tokens[IDs.ID]
    if currentGame.currentCard != {}:
        if email == currentGame.getEmailList()[currentGame.currentTarget]:
            if currentGame.currentAction == "CAPITALGAIN" or currentGame.currentAction == "CASHFLOW":
                currentGame.changeAction("MARKET")
            elif currentGame.currentAction == "STARTTURN":
                pass
            else:
                currentGame.changeAction("ENDTURN")
    return getPlayerData.getPlayerData(tokens[IDs.ID])["playerData"]
