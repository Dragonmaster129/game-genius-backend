from pymongo import MongoClient
import json

mo_c = MongoClient()

db = mo_c.cashflowDB

collections = db.list_collection_names()
print("collections:", collections)

for i in collections:
    col = db[i]
    print("Collection:", i)
    for x in col.find({}):
        ID = x.pop("_id")
        try:
            x.pop("pwd")
        except KeyError:
            print(x["description"])
        print(x)
        print(ID)
