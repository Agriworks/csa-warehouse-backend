## Load authorization credentials

import os
from dotenv import load_dotenv

load_dotenv()

USER_NAME = os.getenv("ERP_USERNAME")
ERP_PASSWORD = os.getenv("ERP_PASSWORD")
MONGODB_URL = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DATABASE_NAME = os.getenv("MONGODB_DATABASE_NAME", "csa-datastore")
