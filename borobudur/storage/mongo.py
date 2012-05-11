from borobudur.storage import (
    Storage,
    StorageException,
    )

from pymongo import (
    Connection,
    )

#from pymongo.objectid import ObjectId

import colander

def null_converter(obj, schema):
    return obj

def sequence_converter(obj, schema):
    result = []
    child_schema = schema.children[0]
    for child_obj in obj:
        result.append(serializers[type(child_schema.typ)](child_obj, child_schema))
    return result

def mapping_serializer(obj, schema):
    result = {}
    for child_schema in schema.children:
        child_obj = obj[child_schema.name]
        result[child_schema.name] = serializers[type(child_schema.typ)](child_obj, child_schema)
    return result

def mapping_deserializer(obj, schema):
    result = {}
    for child_schema in schema.children:
        if child_schema.name in obj:
            child_obj = obj[child_schema.name]
            result[child_schema.name] = serializers[type(child_schema.typ)](child_obj, child_schema)
        else:
            #Todo: consider missing values implementation
            #result[child_schema.name] = default_values[type(child_schema.typ)]
            result[child_schema.name] = None
    return result

serializers = {
    colander.String: null_converter,
    colander.Int: null_converter,
    colander.Float: null_converter,
    colander.DateTime: null_converter,
    colander.Boolean: null_converter,
    #colander.Decimal:
    colander.Sequence: sequence_converter,
    colander.Mapping: mapping_serializer
}

deserializers = {
    colander.String: null_converter,
    colander.Int: null_converter,
    colander.Float: null_converter,
    colander.DateTime: null_converter,
    colander.Boolean: null_converter,
    #colander.Decimal:
    colander.Sequence: sequence_converter,
    colander.Mapping: mapping_deserializer
}

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

    def insert(self, obj, schema=None):
        result = self.deserialize(obj, schema)
        self.collection.insert(result)

    def update(self, obj, schema=None):
        pass

    def delete(self, id):
        pass

    def one(self, id, schema=None):
        #return self.serialize(self.collection.find_one({'_id':ObjectId(id)}), schema)
        pass

    def all(self, query=None, config=None, schema=None):
        pass

    def count(self, query=None):
        pass


#connection = Connection('localhost', 27017)
#db = None;
#userStorage = MongoStorage(connection, db, "users")
#portofolioStorage = MongoStorage(connection, db, "users", "portofolios")
#config.expose_storage(userStorage, route_name="/app/storage/users")
