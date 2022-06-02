from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json

from sampledata import data

from src import totalUp
# from pymongo import MongoClient

# App initialization
app = FastAPI()


class Player:
    def __init__(self, data):
        self.data = data


externalData = data.externalData
data.updateData()


players = {
    "player1": Player(externalData),
    "player2": Player(externalData),
    "player3": Player(externalData),
    "player4": Player(externalData)
}

card = {
    "type": "realestate",
    "name": "APARTMENTCOMPLEX",
    "size": 30,
    "cost": 800000,
    "mortgage": 700000,
    "downpay": 100000,
    "value": 4500,
}

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/data")
async def get(request: Request):
    request = request
    return json.dumps(externalData)
