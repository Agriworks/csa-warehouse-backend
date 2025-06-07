from fastapi import FastAPI
import pymongo
from typing import List
from fastapi.responses import JSONResponse
import json
from bson import json_util

from parameters import MONGODB_URL

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Connect to mongodb
# Create a connection to MongoDB
client = pymongo.MongoClient(MONGODB_URL)
db = client['fpohub']
collection = db['companies']


@app.get("/items", response_model=List[dict])
async def get_all_items():
    # Get all documents and parse BSON to JSON
    documents = list(collection.find({}))
    # Convert ObjectId to string for proper JSON serialization
    json_documents = json.loads(json_util.dumps(documents))
    # Return formatted JSON response with indentation
    return JSONResponse(
        content=json_documents,
        media_type="application/json",
        headers={"Content-Disposition": "inline"},
        background=None,
        status_code=200
    )