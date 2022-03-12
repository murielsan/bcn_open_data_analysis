from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

db = MongoClient(os.getenv("URL")).core


def get_data(collection, filter={}, project={"_id": 0}, limit=0, skip=0):
    return list(db[collection].find(filter, project).limit(limit).skip(skip))


def insert_one_data(collection, data):
    return db[collection].insert_one(data)


def distinct(collection, field):
    return db[collection].distinct(field)


def insert_one_with_pass(user, password, collection, data):
    srv = os.getenv("CLUSTER")
    try:
        url = f"mongodb+srv://{user}:{password}@{srv}"
        print(url)
        db_write = MongoClient(url).core
        return db_write[collection].insert_one(data)
    except:
        return False    