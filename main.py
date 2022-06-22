from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import uuid
from bson import json_util

from sampledata import data
from pydantic import BaseModel
from mongoConnection import playerLogin, getPlayerData, resetPlayer, mongoClient
import copy

from src import totalUp
# from pymongo import MongoClient

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


class LoginData(BaseModel):
    email: str
    password: str


tokens = {}
professions = []
temps = mongoClient.client("cashflowDB")["initialData"]
temp = temps.find({})
for i in temp:
    professions.append(i["profession"])


@app.get("/data/{tokenID}")
async def getData(tokenID):
    if tokenID in tokens:
        return json_util.dumps(getPlayerData.getPlayerData(tokens[tokenID]))
    return json.dumps("invalid token")


@app.post("/login")
async def login(request: LoginData):
    if playerLogin.login(request.email, request.password):
        token = uuid.uuid4().hex
        tokens[token] = request.email
        return json.dumps(token)
    else:
        return False


@app.post("/reset/{tokenID}/")
async def reset(tokenID):
    if tokenID in tokens:
        resetPlayer.initializePlayerData(tokens[tokenID])
        return True
    return False
