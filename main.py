from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json

from sampledata import data
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
    return json.dumps(externalData)
