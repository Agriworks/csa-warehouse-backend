from typing import Any
from pymongo import MongoClient
import parameters
from pymongo.database import Database

client = MongoClient(parameters.MONGODB_URL)
db = client[parameters.MONGODB_DATABASE_NAME]


def get_database() -> Database[Any]:
    return db


def get_client() -> MongoClient[Any]:
    return client


def get_collection(collection_name: str):
    database = get_database()
    return database[collection_name]
