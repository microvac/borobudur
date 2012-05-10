from borobudur.storage import (
    Storage,
    StorageException,
    )

from pymongo import (
    Connection,
    )

import colander

class MongoStorageException(StorageException):
    pass

class MongoStorage(Storage):

    def __init__(self, connection, db, collection_name, embedded_path=None):
        self.connection = connection
        self.db = self.connection[db]
        if self.db is None:
            raise MongoStorageException("There is no database named: %s" % db )
        self.collection = self.db[collection_name]
        if self.collection is None:
            raise MongoStorageException("There is no collection named: %s" % collection_name)

    def deserialize(self, obj, schema=None):
        deserialized_obj = None
        if schema is None:
            return obj

        for child in schema.children:
            if isinstance(child.typ, colander.String):
                deserialized_obj[child.name] = obj[child.name]
            elif isinstance(child.typ, colander.Int):
                deserialized_obj[child.name] = obj[child.name]
            elif isinstance(child.typ, colander.Float):
                deserialized_obj[child.name] = obj[child.name]
            elif isinstance(child.typ, colander.DateTime):
                deserialized_obj[child.name] = obj[child.name]
            elif isinstance(child.typ, colander.Boolean):
                deserialized_obj[child.name] = obj[child.name]
            elif isinstance(child.typ, colander.Decimal):
                deserialized_obj[child.name] = obj[child.name]
            elif isinstance(child.typ, colander.Mapping):
                deserialized_obj[child.name] = self.deserialize(obj[child.name], child)
            elif isinstance(child.typ, colander.Sequence):
                deserialized_obj[child.name] = []
                deserialized_obj.append(self.deserialize(obj[child.name], child))
        return deserialized_obj

    def insert(self, obj, schema=None):
        result = self.deserialize(obj, schema)
        #pymongo
        pass

    def update(self, obj, schema=None):
        pass

    def delete(self, id):
        pass

    def one(self, id, schema=None):
        pass

    def all(self, query=None, config=None, schema=None):
        pass

    def count(self, query=None):
        pass


connection = Connection('localhost', 27017)
db = None;
userStorage = MongoStorage(connection, db, "users")
portofolioStorage = MongoStorage(connection, db, "users", "portofolios")

config.expose_storage(userStorage, route_name="/app/storage/users")
