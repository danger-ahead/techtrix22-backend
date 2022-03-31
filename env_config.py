"""
loads env secrets
"""

import os
import dotenv

dotenv.load_dotenv()
username = os.getenv("ADMIN_USERNAME")
password = os.getenv("PASSWORD")
cluster_name = os.getenv("CLUSTER_NAME")
database = os.getenv("DATABASE")
token_key = os.getenv("TOKEN_KEY")
