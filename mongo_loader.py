import os
import dotenv

import env_config


def get_cluster0():
    # dotenv.load_dotenv()

    # username = os.getenv("ADMIN_USERNAME")
    # password = os.getenv("PASSWORD")
    # cluster_name = os.getenv("CLUSTER_NAME")
    # database = os.getenv("DATABASE")
    # endpoint = os.getenv("CLUSTER_STRING_ENDPOINT")

    from pymongo import MongoClient
    import pymongo

    CONNECTION_STRING = (
        "mongodb+srv://"
        + env_config.username
        + ":"
        + env_config.password
        + "@"
        + env_config.cluster_name
        + ".mongodb.net/"
        + env_config.database
        + "?retryWrites=true&w=majority"
    )

    from pymongo import MongoClient

    # techtrix22 project object
    client = MongoClient(CONNECTION_STRING)

    # techtrix22 database object
    db = client["techtrix"]

    return db


if __name__ == "__main__":
    dbname = get_cluster0()
