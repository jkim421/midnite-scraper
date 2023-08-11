import pymongo

DB_NAME = "midnite"
# COLLECTION_NAME = "shows_mal"
COLLECTION_NAME = "shows_jikan"

def get_connection_str(password):
  return f"mongodb+srv://admin:{password}@midnite-db.ujffr.mongodb.net/midnite?retryWrites=true&w=majority"

def connect_to_midnite(password):
    connection_str = get_connection_str(password)
    mongo_client = pymongo.MongoClient(connection_str)
    db = mongo_client[DB_NAME]
    collection = db[COLLECTION_NAME]

    return collection
