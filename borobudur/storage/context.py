from pymongo import Connection

class StorageContext(object):

    def __init__(self, host, port):
        self.connection = Connection(host=host, port=port)
        self.registry = {}

    def register(self, name, db, collection):
        def wrapper(storage):
            storage.context = self
            self.registry[name] = storage(self.connection, db, collection)
            return storage
        return wrapper

    def unregister(self, name):
        def wrapper(storage):
            del storage.context
            del storage.connection
            self.registry.pop(name)
            return storage
        return wrapper

    def get(self, name):
        return self.registry[name]











