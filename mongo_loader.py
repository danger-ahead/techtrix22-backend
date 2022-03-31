import os
import dotenv

def get_database():
    dotenv.load_dotenv()

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    cluster_name = os.getenv("CLUSTER_NAME")
    database = os.getenv("DATABASE")
    endpoint = os.getenv("CLUSTER_STRING_ENDPOINT")

    
    from pymongo import MongoClient
    import pymongo

    CONNECTION_STRING = "mongodb+srv://{username}:{password}@{cluster_name}.mongodb.net"

    from pymongo import MongoClient
    client = MongoClient(f'{database}')

    print(client.list_databases)

    return client['{database}']
    
if __name__ == "__main__":    
    dbname = get_database()