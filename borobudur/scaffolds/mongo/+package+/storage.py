from borobudur.storage.mongo import MongoStorage, ConnectionHolder
from ent

mongo_connection_holder = ConnectionHolder()

class FriendStorage(MongoStorage):
    collection_holder = mongo_connection_holder
    db_name = "test"
    collection_name ="friends"
    model = Friend

