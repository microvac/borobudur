from borobudur.storage import (
    Storage,
    StorageException,
    SearchConfig
    )
import borobudur.schema as schema

from pymongo import (
    ASCENDING,
    DESCENDING,
    Connection)
from bson.dbref import DBRef
from bson.objectid import ObjectId

import colander


class StorageContext(object):

    def __init__(self):
        self.connection = None
        self.registry = {}

    def connect(self, host=None, port=None):
        self.connection = Connection(host, port)

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
        return self.registry.get(name)

def null_converter(obj, schema=None, func=None):
    return obj

def sequence_converter(obj, schema, converter):
    result = []
    child_schema = schema.children[0]
    for child_obj in obj:
        result.append(converter(child_obj, child_schema, converter))
    return result

def mapping_serializer(obj, schema, serialize_child):
    result = {}
    if "_id" in obj:
        result["_id"] = obj["_id"]
    for child_schema in schema.children:
        child_obj = obj[child_schema.name]
        result[child_schema.name] = serialize_child(child_obj, child_schema, serialize_child)
    return result

def mapping_deserializer(obj, schema, deserialize_child):
    result = {}
    if "_id" in obj:
        result["_id"] = obj["_id"]
    for child_schema in schema.children:
        if child_schema.name in obj:
            child_obj = obj[child_schema.name]
            result[child_schema.name] = deserialize_child(child_obj, child_schema, deserialize_child)
        else:
            #Todo: consider missing values implementation
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
    colander.Mapping: mapping_serializer,
    schema.Ref: null_converter,
}

deserializers = {
    colander.String: null_converter,
    colander.Int: null_converter,
    colander.Float: null_converter,
    colander.DateTime: null_converter,
    colander.Boolean: null_converter,
    #colander.Decimal:
    colander.Sequence: sequence_converter,
    colander.Mapping: mapping_deserializer,
    schema.Ref: null_converter,
}

class MongoStorageException(StorageException):
    pass

class MongoStorage(Storage):

    id_attribute = "_id"
    id_type = ObjectId

    def __init__(self, connection, db, collection_name):
        self.connection = connection
        self.db = self.connection[db]
        self.collection = self.db[collection_name]

    def insert(self, obj, schema=None):
        result = mapping_serializer(obj, schema, self.serialize)
        self.collection.insert(result)
        return result

    def serialize(self, obj, schema, serialize_child):
        storage = self.context.registry.get(schema.schema_namespace) if hasattr(schema, "schema_namespace") else None
        if storage is None:
            return serializers[type(schema.typ)](obj, schema, serialize_child)
        else:
            result = storage.update(obj, schema)
            ref = DBRef(collection=storage.collection.name, id=result['_id'])
            return ref

    def deserialize(self, obj, schema, deserialize_child):
        storage = self.context.registry.get(schema.schema_namespace) if hasattr(schema, "schema_namespace") else None
        if storage is None:
            return deserializers[type(schema.typ)](obj, schema, deserialize_child)
        else:
            #if context changes collection then the reference cannot be found
            result = storage.one(obj.id, schema)
            return result

    def update(self, obj, schema=None):
        result = mapping_serializer(obj, schema, self.serialize)
        self.collection.update({self.id_attribute: self.id_type(obj.get(self.id_attribute))},
                               result,
                               upsert=True,
                               manipulate=True,
                              )
        #self.collection.save(result) #save = upsert
        return result

    #Todo: cascade delete
    def delete(self, id):
        result = self.collection.find_one({self.id_attribute: self.id_type(id)})
        if not result:
            raise ValueError("Error in deleting - There is no such id as: %s" % id.__str__())
        self.collection.remove({self.id_attribute: self.id_type(id)})
        return True

    def one(self, id, schema=None):
        result = self.collection.find_one({self.id_attribute: self.id_type(id)})
        if result is not None:
            result = mapping_deserializer(result, schema, self.deserialize)
        return result

    def all(self, query=None, config=None, schema=None):
        if config is None:
            config = SearchConfig(0, 0)

        cursor = self.collection.find(spec=query,
                                      fields=self.get_field_list(schema),
                                      skip=config.skip,
                                      limit=config.limit
        )
        #fields args is for optimization by choosing only listed fields in schema

        if config.sorts:
            for sort in config.sorts:
                order = None
                if sort.order == "asc":
                    order = ASCENDING
                elif sort.order == "desc":
                    order = DESCENDING
                cursor.sort(sort.criteria, order)

        result = []
        for item in cursor:
            result.append(mapping_deserializer(item, schema, self.deserialize))
        return result

    def count(self, query=None):
        return self.collection.find(spec=query).count()

    def get_field_list(self, schema):
        if schema is None: return None
        result = []
        for child in schema.children:
            result.append(child.name)
        return result

#connection = Connection('localhost', 27017)
#db = None;
#userStorage = MongoStorage(connection, db, "users")
#portofolioStorage = MongoStorage(connection, db, "users", "portofolios")
#config.expose_storage(userStorage, route_name="/app/storage/users")
