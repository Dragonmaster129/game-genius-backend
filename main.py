from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import uuid
from bson import json_util
import copy
import time
# from pymongo import MongoClient

from sampledata import data
from pydantic import BaseModel
from mongoConnection import playerLogin, getPlayerData, resetPlayer, mongoClient, createCard
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


tokens = {"1": "test@test.com"}
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


@app.get("/data/{tokenID}")
async def getData(tokenID):
    if tokenID in tokens:
        return json_util.dumps(getPlayerData.getPlayerData(tokens[tokenID]))
    return "invalid token"


@app.get("/games")
async def getGames():
    gameList = db["game"].find({"gameStarted": 0})
    # TODO sort through the data and return a list


@app.post("/create-game")
async def createGame():
    # TODO get the data and create the game
    pass


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


@app.get("/activateEvent")
async def activateEvent():
    for i in websockets.keys():
        await websockets[i].send_text("SENT")


@app.websocket("/joinGame")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        res = await websocket.receive_text()
        # await websocket.send_text(f"Message text was: {res}")
        # print(res)
        websockets[tokens[res[0]]] = websocket
