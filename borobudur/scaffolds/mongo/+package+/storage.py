from borobudur.storage.mongo import MongoStorage, StorageContext

storage_context = StorageContext('localhost', 27017)

@storage_context.register("Friend", "test", "friend")
class FriendStorage(MongoStorage):
    pass

