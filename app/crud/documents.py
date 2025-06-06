from pymongo.collection import Collection
from typing import List, Optional
from bson import ObjectId
from ..core.db import get_collection
from ..models.documents import DocumentInDB


def get_documents_from_collection(
    collection_name: str, skip: int = 0, limit: int = 100
) -> List[DocumentInDB]:
    collection: Collection = get_collection(collection_name)
    documents_cursor = collection.find().skip(skip).limit(limit)
    return [DocumentInDB(**doc) for doc in documents_cursor]


def get_document_by_id_from_collection(
    collection_name: str, document_id: str
) -> Optional[DocumentInDB]:
    collection: Collection = get_collection(collection_name)
    doc = collection.find_one({"_id": ObjectId(document_id)})
    if doc:
        return DocumentInDB(**doc)
    return None
