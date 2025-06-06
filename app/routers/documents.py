from fastapi import APIRouter, HTTPException, Query
from typing import List
from ..crud import documents as crud_documents
from ..models.documents import DocumentInDB

router = APIRouter(
    prefix="/erp",
    tags=["documents"],
)


@router.get("/{erp_instance_name}/documents", response_model=List[DocumentInDB])
async def read_documents(
    erp_instance_name: str,
    skip: int = 0,
):
    """
    Retrieve documents from a specific ERP instance collection.
    """
    # TODO: Validate ERP name
    documents = crud_documents.get_documents_from_collection(
        collection_name=f"erp_{erp_instance_name}",
        skip=skip,
    )
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found")
    return documents


@router.get("/{erp_instance_name}/documents/{document_id}", response_model=DocumentInDB)
async def read_document_by_id(erp_instance_name: str, document_id: str):
    """
    Retrieve a specific document by its ID from an ERP instance collection.
    """
    document = crud_documents.get_document_by_id_from_collection(
        collection_name=f"erp_{erp_instance_name}", document_id=document_id
    )
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document
