import pymongo

connection_str = "mongodb+srv://admin:science2@midnite-db.ujffr.mongodb.net/midnite?retryWrites=true&w=majority"
db_name = "midnite"
# collection_name = "shows_jikan"
collection_name = "shows_mal"

def connect_to_midnite():
    mongo_client = pymongo.MongoClient(connection_str)
    db = mongo_client[db_name]
    collection = db[collection_name]

    return collection
