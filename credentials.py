## Load authorization credentials

import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("ERP_USERNAME")
password = os.getenv("ERP_PASSWORD")
mongodb_uri = os.getenv("MONGODB_URI")
mongodb_db_name = os.getenv("MONGODB_DATABASE_NAME")
