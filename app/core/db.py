from pymongo import MongoClient
import credentials

client = MongoClient(credentials.mongodb_uri)
db = client[credentials.mongodb_db_name]


def get_database():
    return db


def get_collection(collection_name: str):
    database = get_database()
    return database[collection_name]
