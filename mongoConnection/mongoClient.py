from pymongo import MongoClient


def client(database):
    mo_c = MongoClient()

    db = mo_c[database]

    # collections = db.list_collection_names()
    # print("collections:", collections)

    # for i in collections:
    #     col = db[i]
    #     print("Collection:", i)
    #     for x in col.find({}):
    #         ID = x.pop("_id")
    #         try:
    #             x.pop("pwd")
    #         except KeyError:
    #             print(x["description"])
    #         # print(x)

    # col = db["doodad"]

    # How to Insert into the collection in the db
    # insert = "n"
    # if insert == "y":
    #     insertDict = {
    #         "description": """You Can't Say No
    # A co-worker asks you to buy cookies
    # to benefit her child's softball team
    # Pay: $20""",
    #         "cash": 20
    #     }
    #     print(insertDict)
    #     x = col.insert_one(insertDict)

    return db
