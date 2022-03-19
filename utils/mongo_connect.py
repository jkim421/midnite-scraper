import pymongo

# connection_str = "mongodb+srv://admin:science2@midnite-db.ujffr.mongodb.net/midnite?retryWrites=true&w=majority"
DB_NAME = "midnite"
COLLECTION_NAM = "shows_mal"

def get_connection_str(password):
  return f"mongodb+srv://admin:{password}@midnite-db.ujffr.mongodb.net/midnite?retryWrites=true&w=majority"

def connect_to_midnite(password):
    connection_str = get_connection_str(password)
    mongo_client = pymongo.MongoClient(connection_str)
    db = mongo_client[DB_NAME]
    collection = db[COLLECTION_NAM]

    return collection
