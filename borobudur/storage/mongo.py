from borobudur.storage import Storage

class MongoStorage(Storage):

    def __init__(self, db, collection_name, embedded_path=None):
        pass


db = None;
userStorage = MongoStorage(db, "users")
portofolioStorage = MongoStorage(db, "users", "portofolios")

config.expose_storage(userStorage, route_name="/app/storage/users")
