import bson
from borobudur.storage import Storage, StorageException, SearchConfig
from borobudur.model import CollectionRefNode, ModelRefNode, RefNode, Model, Collection
from borobudur.schema import ObjectId, MappingNode, Date, Currency, SequenceNode
from datetime import datetime, date

from pymongo import ASCENDING, DESCENDING

import colander

class StorageContext(object):

    reference = {}

    def set(self, model, storage):
        self.reference[model] = storage

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

def object_id_serializer(obj, schema=None, func=None):
    return obj if obj is not None else bson.ObjectId()

serializers = {
    colander.String: null_converter,
    colander.Int: null_converter,
    colander.Float: null_converter,
    colander.DateTime: null_converter,
    colander.Boolean: null_converter,
    #colander.Decimal:
    colander.Sequence: sequence_converter,
    colander.Mapping: mapping_serializer,
    ObjectId: object_id_serializer,
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

def merge_array(source, target):
    result = []
    for index, value in enumerate(source):
        if isinstance(value, dict):
            target_value = target[index] if len(target) > index else {}
            result.append(merge_document(value, target_value))
        elif isinstance(value, list):
            target_value = target[index] if len(target) > index else []
            result.append(merge_document(value, target_value))
        else:
            result.append(value)
    return result

def merge_document(source, target):
    for key, value in source.items():
        if isinstance(value, dict):
            target_value = target[key] if key in target else {}
            target[key] = merge_document(value, target_value)
        elif isinstance(value, list):
            target_value = target[key] if key in target else []
            target[key] = merge_array(value, target_value)
        else:
            target[key] = value
    return target

class MongoStorageException(StorageException):
    pass

class BaseStorage(object):
    def serialize(self, obj, schema, serialize_child):
        if isinstance(schema, RefNode):
            storage = self.context.get(schema.target)
            if storage is not None:
                id = obj
                if isinstance(obj, Model):
                    id = obj.id
                if isinstance(obj, Collection):
                    id = [m.id for m in obj.models]
                return id

            if isinstance(obj, Model):
                obj = obj.attributes
            if isinstance(obj, Collection):
                obj = obj.models

        return serializers[type(schema.typ)](obj, schema, serialize_child)

    def deserialize(self, obj, schema, deserialize_child):
        if isinstance(schema, RefNode):
            storage = self.context.get(schema.target)
            if storage is not None:
                if isinstance(schema, CollectionRefNode):
                    obj = [storage.one(item, schema.child) for item in obj]
                    return Collection(obj, schema.target, schema_name=schema.schema_name)
                else:
                    obj = storage.one(obj, schema)
                    return schema.target(obj, schema_name=schema.schema_name)

        result = deserializers[type(schema.typ)](obj, schema, deserialize_child)
        if isinstance(schema, RefNode):
            if isinstance(schema, CollectionRefNode):
                return Collection(result, schema.target, schema_name=schema.schema_name)
            else:
                return schema.target(result, schema_name=schema.schema_name)
        return result

class MongoStorage(Storage, BaseStorage):

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
        self.pre_insert(result)
        self.collection.insert(result)
        if result:
            result = mapping_deserializer(result, schema, self.deserialize)
        return result

    def pre_insert(self, appstruct):
        pass

    def update(self, obj, schema=None):
        serialized = mapping_serializer(obj, schema, self.serialize)
        previous = self.collection.find_one({self.model.id_attribute: self.model.id_type(obj[self.model.id_attribute])})
        result = merge_document(serialized, previous)

        #mongo doesn't receive set _id
        if "_id" in result:
            del result["_id"]

        self.collection.update({self.model.id_attribute: self.model.id_type(obj[self.model.id_attribute])},
                               result
                              )
        deserialized = mapping_deserializer(result, schema, self.deserialize)
        return deserialized

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


    def flatten(self, item, prefix=""):
        result = {}
        if isinstance(item, list):
            for index, it in enumerate(item):
                subprefix = prefix+"."+str(index)
                result.update(self.flatten(it, subprefix))
        elif isinstance(item, dict):
            for key, value in item.items():
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

    def __str__(self):
        return "%s mongo storage on %s - %s" % (self.model.__class__.__name__, self.db_name, self.collection_name)

class EmbeddedMongoStorage(Storage, BaseStorage):

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

        collection = parent[self.attribute_path]
        collection.add(obj)
        index = len(collection) - 1
        update_result = self.parent_update(parent_id, parent, parent_schema)
        result = update_result[self.attribute_path][index]

        return result.attributes

    def update(self, parent_id, obj, schema=None):
        parent_schema = self.build_parent_schema(schema)
        parent = self.parent_one(parent_id, parent_schema)

        collection = parent[self.attribute_path]
        index = self.find(obj[self.model.id_attribute], collection)
        collection.models[index] = obj
        update_result = self.parent_update(parent_id, parent, parent_schema)
        result = update_result[self.attribute_path][index]

        return result.attributes

    def delete(self, parent_id, id):
        parent_schema = self.build_parent_schema()
        parent = self.parent_one(parent_id, parent_schema)

        collection = parent[self.attribute_path]
        index = self.find(id, collection)
        collection.models.pop(index)
        update_result = self.parent_update(parent_id, parent, parent_schema)

        return True

    def one(self, parent_id, id, schema=None):
        parent_schema = self.build_parent_schema(schema)
        parent = self.parent_one(parent_id, parent_schema)

        collection = parent[self.attribute_path]
        index = self.find(self.model.id_type(id), collection)

        return collection[index].attributes

    def all(self, parent_id, query=None, config=None, schema=None):
        parent_schema = self.build_parent_schema(schema)
        parent = self.parent_one(parent_id, parent_schema)

        if not config:
            config = SearchConfig(0, 0)

        if config.limit:
            collection = parent[self.attribute_path][config.skip:config.skip+config.limit]
        else:
            collection = parent[self.attribute_path][config.skip:len(parent[self.attribute_path])]

        return [m.attributes for m in collection]

    def count(self, parent_id, query=None):
        parent_schema = self.build_parent_schema()
        parent = self.parent_one(parent_id, parent_schema)

        collection = parent[self.attribute_path]

        return len(collection)

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
        for index, item in enumerate(sequence.models):
            if item.get(self.model.id_attribute) == id:
                return index
        return None

    def build_parent_schema(self, schema=None):
        if schema is None:
            schema = self.empty_schema

        parent_id_attribute = self.parent_storage.model.id_attribute
        parent_id_node = filter(lambda c: c.name==parent_id_attribute, self.parent_storage.model.get_schema("").children)[0]

        schema_name = None
        for name,value in self.model.schemas.items():
            if value == schema:
                schema_name = name
                break
        else:
            raise ValueError("cannot find schema")

        structure = {
            parent_id_attribute: parent_id_node,
            self.attribute_path: CollectionRefNode(self.model, schema_name)
        }
        return MappingNode(**structure)

    def __str__(self):
        return "%s mongo embedded storage with parent %s on %s" % (self.model.__name__, self.parent_storage.__class__.__name__, self.attribute_path)

