from borobudur.storage import (
    Storage,
    StorageException,
    )

from pymongo import (
    ASCENDING,
    DESCENDING,
    )
from bson.dbref import DBRef

import colander
import traceback

def null_converter(obj, schema=None, func=None):
    return obj

def sequence_converter(obj, schema, converter):
    result = []
    child_schema = schema.children[0]
    for child_obj in obj:
        result.append(converter(child_obj, child_schema, converter))
    return result

def mapping_serializer(obj, schema, serializer_child):
    result = {}
    if "_id" in obj:
        result["_id"] = obj["_id"]
    for child_schema in schema.children:
        child_obj = obj[child_schema.name]
        result[child_schema.name] = serializer_child(child_obj, child_schema, serializer_child)
    return result

def mapping_deserializer(obj, schema, deserializer_child):
    result = {}
    if "_id" in obj:
        result["_id"] = obj["_id"]
    for child_schema in schema.children:
        if child_schema.name in obj:
            child_obj = obj[child_schema.name]
            result[child_schema.name] = deserializer_child(child_obj, child_schema, deserializer_child)
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
        result = mapping_serializer(obj, schema, self.serialize)
        try:
            self.collection.insert(result)
        except:
            raise MongoStorageException("Error in inserting: \n%s" % traceback.format_exc())
        return result

    def serialize(self, obj, schema, serializer_child):
        storage = self.context.registry.get(schema.schema_namespace) if hasattr(schema, "schema_namespace") else None
        if storage is None:
            return serializers[type(schema.typ)](obj, schema, serializer_child)
        else:
            result = storage.update(obj, schema)
            ref = DBRef(collection=storage.collection.name, id=result['_id'])
            return ref

    def deserialize(self, obj, schema, deserializer_child):
        storage = self.context.registry.get(schema.schema_namespace) if hasattr(schema, "schema_namespace") else None
        if storage is None:
            return deserializers[type(schema.typ)](obj, schema, deserializer_child)
        else:
            #if context changes collection then the reference cannot be found
            result = storage.one(obj.id, schema)
            return result

    def update(self, obj, schema=None):
        try:
            result = mapping_serializer(obj, schema, self.serialize)
            #self.collection.update({'_id': obj['_id']}, result)
            self.collection.save(result) #save = upsert
        except:
            raise MongoStorageException("Error in updating: \n%s" % traceback.format_exc())
        return result

    #Todo: cascade delete
    def delete(self, id):
        if self.collection.find_one({'_id': id}) is None:
            raise ValueError("Error in deleting - There is no such id as: %s" % id.__str__())
        try:
            self.collection.remove({'_id': id})
        except:
            raise MongoStorageException("Error in deleting: \n%s" % traceback.format_exc())
        return True

    #Todo: prevent circular referencing and add lazy loading?
    def one(self, id, schema=None):
        try:
            result = self.collection.find_one({'_id':id})
        except:
            raise MongoStorageException("Error in finding id: %s \n%s" % (id.__str__(), traceback.format_exc()))
        if result is not None:
            result = mapping_deserializer(result, schema, self.deserialize)
        return result

    def all(self, query=None, config=None, schema=None):
        skip = getattr(config, "skip", 0) if config is not None else 0
        limit = getattr(config, "limit", 0) if config is not None else 0
        sort = getattr(config, "sorts", None) if config is not None else None

        try:
            cursor = self.collection.find(spec=query,
                                          fields=self.get_field_list(schema),
                                          skip=skip,
                                          limit=limit
            )
            #fields args is for optimization by choosing only listed fields in schema
        except:
            raise MongoStorageException("Error in searching: \n%s" % traceback.format_exc())

        if sort is not None:
            for sort in config.sorts:
                order = None
                if sort.order == "asc":
                    order = ASCENDING
                elif sort.order == "desc":
                    order = DESCENDING
                #GEO2D, or GEOHAYSTACK?
                cursor.sort(sort.criteria, order)

        result = []
        for item in cursor:
            result.append(mapping_deserializer(item, schema, self.deserialize))
        return result

    def count(self, query=None):
        try:
            return self.collection.find(spec=query).count()
        except:
            raise MongoStorageException("Error in counting: \n%s" % traceback.format_exc())

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
