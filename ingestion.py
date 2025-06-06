## This script pulls documents from ERPNext servers and stores in MongoDB.
# This will run daily at 3am or when needed by CSA IT admin.

import requests
import credentials
import pymongo
from ERPs import ERP

# Connect to MongoDB
uri = credentials.mongodb_uri
client = pymongo.MongoClient(uri)
db = client["csa-datastore"]

# Script runs for each ERP instance
for erp_instance in ERP:

    # Login
    login_url = f"https://{erp_instance.value}/api/method/login?usr={credentials.username}&pwd={credentials.password}"
    session = requests.Session()
    response = session.post(login_url)
    if response.status_code != 200:
        print(f"Could not login to {erp_instance.name}")

    # Select MongoDB collection for the current ERP instance
    erp_collection_name = f"erp_{erp_instance.name.lower()}"
    erp_collection = db[erp_collection_name]

    # Get doctype count
    doctype_count_url = f"https://{erp_instance.value}/api/method/frappe.client.get_count?doctype=DocType"
    response = session.get(doctype_count_url)
    doctype_count = response.json().get("message")

    # Get all doctypes
    list_doctypes_url = f"https://{erp_instance.value}/api/resource/DocType?limit_page_length={doctype_count}"
    response = session.get(list_doctypes_url)
    doctype_names = []
    if response.status_code == 200 and response.json().get("data"):
        for doctype in response.json().get("data"):
            doctype_names.append(doctype.get("name"))
        print(len(doctype_names))

    for doctype in doctype_names:
        print(doctype)

        # Get document count
        document_count_url = f"https://{erp_instance.value}/api/method/frappe.client.get_count?doctype={doctype}"
        response = session.get(document_count_url)
        document_count = 0
        if response.status_code == 200:
            document_count = response.json().get("message")
        print(document_count)

        # Get all documents for the doctype
        list_documents_url = f'https://{erp_instance.value}/api/resource/{doctype}?fields=["*"]&limit_page_length={document_count}'
        # TODO: {doctype} doens't work here - mismatch between doctype_name and label??
        response = session.get(list_documents_url)
        if response.status_code == 200:
            documents_data = response.json().get("data")
            if documents_data:
                documents_to_insert = [
                    {"doctype": doctype, "document_data": doc} for doc in documents_data
                ]
                erp_collection.insert_many(documents_to_insert)
                print(
                    f"Inserted {len(documents_to_insert)} documents from {doctype} into {erp_collection_name}"
                )
            else:
                print(f"No data found for {doctype} despite count {document_count}")
        else:
            print(
                f"Failed to fetch documents for {doctype}. Status: {response.status_code}, Response: {response.text}"
            )

    # Logout
    logout_url = f"https://{erp_instance.value}/api/method/logout"
    response = session.post(logout_url)
    if response.status_code != 200:
        print(f"Could not logout from {erp_instance.name}")
