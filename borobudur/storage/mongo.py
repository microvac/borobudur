from borobudur.storage import Storage, StorageException, SearchConfig
from borobudur.model import CollectionRefNode, ModelRefNode
from borobudur.schema import ObjectId, MappingNode, Date, Currency, SequenceNode
from datetime import datetime, date

from pymongo import ASCENDING, DESCENDING

import colander

class StorageContext(object):

    def __init__(self, connection, reference_types):
        self.reference = {}
        for type in reference_types:
            self.reference[type.model] = type(self, connection)

    def get(self, model):
        return self.reference.get(model, None)

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
    #if "_id" in obj:
    #    result["_id"] = obj["_id"]
    for child_schema in schema.children:
        child_obj = obj[child_schema.name]
        result[child_schema.name] = serialize_child(child_obj, child_schema, serialize_child)
    return result

def mapping_deserializer(obj, schema, deserialize_child):
    result = {}
    #if "_id" in obj:
    #    result["_id"] = obj["_id"]
    if obj is None:
        return None
    for child_schema in schema.children:
        if child_schema.name in obj:
            child_obj = obj[child_schema.name]
            result[child_schema.name] = deserialize_child(child_obj, child_schema, deserialize_child)
        else:
            #Todo: consider missing values implementation
            result[child_schema.name] = None
    return result

def date_serializer(obj, schema=None, func=None):
    return datetime(year=obj.year, month=obj.month, day=obj.day)

def date_deserializer(obj, schema=None, func=None):
    return date(year=obj.year, month=obj.month, day=obj.day)

serializers = {
    colander.String: null_converter,
    colander.Int: null_converter,
    colander.Float: null_converter,
    colander.DateTime: null_converter,
    colander.Boolean: null_converter,
    #colander.Decimal:
    colander.Sequence: sequence_converter,
    colander.Mapping: mapping_serializer,
    ObjectId: null_converter,
    Date: date_serializer,
    Currency: null_converter,
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
    ObjectId: null_converter,
    Date: date_deserializer,
    Currency: null_converter,
}

class MongoStorageException(StorageException):
    pass

class MongoStorage(Storage):

    db_name = None
    collection_name = None
    model = None

    def __init__(self, context, connection):
        self.context = context
        self.connection = connection

        self.db = self.connection[self.db_name]
        self.collection = self.db[self.collection_name]

    def insert(self, obj, schema=None):
        result = mapping_serializer(obj, schema, self.serialize)
        self.collection.insert(result)
        return result

    def update(self, obj, schema=None):
        serialized = mapping_serializer(obj, schema, self.serialize)
        result = self.flatten(serialized)
        self.collection.update({self.model.id_attribute: self.model.id_type(obj[self.model.id_attribute])},
                               {"$set": result},
                              )
        return self.one(obj[self.model.id_attribute], schema)

    def delete(self, id):
        result = self.collection.find_one({self.model.id_attribute: self.model.id_type(id)})
        if not result:
            raise ValueError("Error in deleting - There is no such id as: %s" % id.__str__())
        self.collection.remove({self.model.id_attribute: self.model.id_type(id)})
        return True

    def one(self, id, schema=None):
        result = self.collection.find_one({self.model.id_attribute: self.model.id_type(id)})
        if result:
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

    def serialize(self, obj, schema, serialize_child):
        if type(schema)==ModelRefNode:
            return obj[schema.target.id_attribute]
        else:
            return serializers[type(schema.typ)](obj, schema, serialize_child)

    def deserialize(self, obj, schema, deserialize_child):
        storage = self.context.get(schema.target) if type(schema)==ModelRefNode else None
        if storage is None:
            return deserializers[type(schema.typ)](obj, schema, deserialize_child)
        else:
            result = storage.one(obj, schema)
            return result

    def flatten(self, item, prefix=""):
        result = {}
        if isinstance(item, list):
            for index, it in enumerate(item):
                subprefix = prefix+"."+str(index)
                result.update(self.flatten(it, subprefix))
        elif isinstance(item, dict):
            for key, value in item.items():
                if key == "_id":
                    continue
                if isinstance(value, list):
                    for index, it in enumerate(value):
                        subprefix = prefix+"."+key+"."+str(index) if prefix else key+"."+str(index)
                        result.update(self.flatten(it, subprefix))
                elif isinstance(value, dict):
                    subprefix = prefix+"."+key if prefix else key
                    result.update(self.flatten(value, subprefix))
                else:
                    subprefix = prefix+"."+key if prefix else key
                    result[subprefix] = value
        else:
            if prefix != "_id":
                result[prefix] = item
        return result

    def get_field_list(self, schema):
        if schema is None: return None
        result = []
        for child in schema.children:
            result.append(child.name)
        return result

    def extract_query(self, params):
        return {}

    def __str__(self):
        return "%s mongo storage on %s - %s" % (self.model.__class__.__name__, self.db_name, self.collection_name)

class EmbeddedMongoStorage(Storage):

    model = None
    parent_storage = None
    attribute_path = None
    empty_schema = None

    def __init__(self, context, connection):
        self.context = context
        self.parent_storage = self.parent_storage(context, connection)

    def insert(self, parent_id, obj, schema=None):
        parent_schema = self.build_parent_schema(schema)
        parent = self.parent_one(parent_id, parent_schema)

        serialized = mapping_serializer(obj, schema, self.serialize)
        collection = parent[self.attribute_path]
        collection.append(serialized)
        index = len(collection) - 1
        update_result = self.parent_update(parent_id, parent, parent_schema)
        result = update_result[self.attribute_path][index]

        return result

    def update(self, parent_id, obj, schema=None):
        parent_schema = self.build_parent_schema(schema)
        parent = self.parent_one(parent_id, parent_schema)

        serialized = mapping_serializer(obj, schema, self.serialize)
        collection = parent[self.attribute_path]
        index = self.find(obj[self.model.id_attribute], collection)
        collection[index] = serialized
        update_result = self.parent_update(parent_id, parent, parent_schema)
        result = update_result[self.attribute_path][index]

        return result

    def delete(self, parent_id, id):
        parent_schema = self.build_parent_schema()
        parent = self.parent_one(parent_id, parent_schema)

        collection = parent[self.attribute_path]
        index = self.find(id, collection)
        collection.pop(index)
        update_result = self.parent_update(parent_id, parent, parent_schema)

        return True

    def one(self, parent_id, id, schema=None):
        parent_schema = self.build_parent_schema(schema)
        parent = self.parent_one(parent_id, parent_schema)

        collection = parent[self.attribute_path]
        index = self.find(id, collection)

        return collection[index]

    def all(self, parent_id, query=None, config=None, schema=None):
        parent_schema = self.build_parent_schema(schema)
        parent = self.parent_one(parent_id, parent_schema)

        if not config:
            config = SearchConfig(0, 0)

        if config.limit:
            collection = parent[self.attribute_path][config.skip:config.skip+config.limit]
        else:
            collection = parent[self.attribute_path][config.skip:len(parent[self.attribute_path])]

        return collection

    def count(self, parent_id, query=None):
        parent_schema = self.build_parent_schema()
        parent = self.parent_one(parent_id, parent_schema)

        collection = parent[self.attribute_path]

        return len(collection)

    def serialize(self, obj, schema, serialize_child):
        storage = self.context.get(schema.target) if type(schema)==ModelRefNode else None
        if storage is None:
            return serializers[type(schema.typ)](obj, schema, serialize_child)
        else:
            result = storage.update(obj, schema)
            ref = result[storage.model.id_attribute]
            return ref

    def deserialize(self, obj, schema, deserialize_child):
        storage = self.context.get(schema.target) if type(schema)==ModelRefNode else None
        if storage is None:
            return deserializers[type(schema.typ)](obj, schema, deserialize_child)
        else:
            result = storage.one(obj, schema)
            return result

    def parent_one(self, parent_id, schema):
        if parent_id[1] is None:
            result = self.parent_storage.one(parent_id[0], schema)
        else:
            result = self.parent_storage.one(parent_id[1], schema)
        return result

    def parent_update(self, parent_id, obj, schema):
        if parent_id[1] is None:
            result = self.parent_storage.update(obj, schema)
        else:
            result = self.parent_storage.update(parent_id[1], obj, schema)
        return result

    def find(self, id, sequence):
        for index, item in enumerate(sequence):
            if item.get(self.model.id_attribute) == id:
                return index
        return None

    def build_parent_schema(self, schema=None):
        if schema is None:
            schema = self.empty_schema

        structure = {
            self.attribute_path: SequenceNode(schema)
        }
        return MappingNode(**structure)

    def __str__(self):
        return "%s mongo embedded storage with parent %s on %s" % (self.model.__name__, self.parent_storage.__class__.__name__, self.attribute_path)

