# import pymongo, json, time, os, logging
# from new_bot_container.modules.db.mongodb import MongoDriver

def purge(client):
    client.db.command("dropDatabase")


def add_records(client, collection: str, data: dict):
    db = client.db[collection]
    result = db.insert_one(data)
    return result


def get_records(client, collection: str, query: dict):
    db = client.db[collection]
    return list(db.find(query))
