import borobudur
import bson
from borobudur import NotFoundException
from borobudur.resource.storage import StorageException, SearchConfig
from borobudur.model import CollectionRefNode, ModelRefNode, RefNode, Model, Collection, CollectionRef, ModelRef
from borobudur.schema import ObjectId, MappingNode, Date, Currency, SequenceNode, DateTime
from datetime import datetime, date

from pymongo import ASCENDING, DESCENDING, Connection

import colander


#### Serializer and deserializers ###
# serializer should be forgiving on non existing items that make adding child schema later easier
# deserializer should harsher, spawning errors in times

def null_converter(obj, schema=None, func=None):
    return obj

def sequence_serializer(obj, schema, converter):
    result = []
    child_schema = schema.children[0]
    for child_obj in obj:
        result.append(converter(child_obj, child_schema, converter))
    return result

def collection_serializer(obj, schema, deserialize_child):
    return sequence_serializer(obj.models, schema, deserialize_child)

def sequence_deserializer(obj, schema, converter):
    if obj is None:
        obj = []

    result = []
    child_schema = schema.children[0]
    for child_obj in obj:
        result.append(converter(child_obj, child_schema, converter))
    return result

def collection_deserializer(obj, schema, deserialize_child):
    objs = sequence_deserializer(obj, schema, deserialize_child)
    return Collection(schema.typ.target, objs)

def mapping_serializer(obj, schema, serialize_child):
    result = {}
    for child_schema in schema.children:
        child_obj = obj[child_schema.name]
        result[child_schema.name] = serialize_child(child_obj, child_schema, serialize_child)
    return result

def model_serializer(obj, schema, serialize_child):
    result = {}
    for child_schema in schema.children:
        if child_schema.name not in obj:
            continue
        child_obj = obj[child_schema.name]
        result[child_schema.name] = serialize_child(child_obj, child_schema, serialize_child)
    return result


def mapping_deserializer(obj, schema, deserialize_child):
    if obj is None:
        obj = {}

    result = {}
    for child_schema in schema.children:
        if child_schema.name not in obj:
            child_obj = None
        else:
            child_obj = obj[child_schema.name]
        result[child_schema.name] = deserialize_child(child_obj, child_schema, deserialize_child)

    return result

def model_deserializer(obj, schema, deserialize_child):
    attrs = mapping_deserializer(obj, schema, deserialize_child)
    return schema.typ.target(attrs)

def date_serializer(obj, schema=None, func=None):
    return datetime(year=obj.year, month=obj.month, day=obj.day)

def date_deserializer(obj, schema=None, func=None):
    if obj is None:
        return None
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
    colander.Sequence: sequence_serializer,
    colander.Mapping: mapping_serializer,
    ObjectId: object_id_serializer,
    Date: date_serializer,
    Currency: null_converter,
    CollectionRef: collection_serializer,
    ModelRef: model_serializer,

}

deserializers = {
    colander.String: null_converter,
    colander.Int: null_converter,
    colander.Float: null_converter,
    colander.DateTime: null_converter,
    colander.Boolean: null_converter,
    #colander.Decimal:
    colander.Sequence: sequence_deserializer,
    colander.Mapping: mapping_deserializer,
    ObjectId: null_converter,
    Date: date_deserializer,
    Currency: null_converter,
    CollectionRef: collection_deserializer,
    ModelRef: model_deserializer,
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
    if target is None:
        target = {}
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
    exposed = True

    def serialize(self, obj, schema, serialize_child):
        if isinstance(schema, RefNode):
            if obj is None and schema.typ.nullable:
                return None

            if isinstance(schema, ModelRefNode):

                storage = self.request.resources.get_storage(schema.typ.target)

                #todo hack
                if isinstance(storage, EmbeddedMongoStorage):
                    storage = None

                if storage is not None:
                    return obj.id

        return serializers[type(schema.typ)](obj, schema, serialize_child)

    def deserialize(self, obj, schema, deserialize_child):
        if isinstance(schema, RefNode):
            if obj is None and schema.typ.nullable:
                return None

            if isinstance(schema, ModelRefNode):
                storage = self.request.resources.get_storage(schema.typ.target)

                #todo hack
                if isinstance(storage, EmbeddedMongoStorage):
                    storage = None

                if storage is not None:
                    return schema.typ.target.with_id(obj)

        return deserializers[type(schema.typ)](obj, schema, deserialize_child)

class MongoStorage(BaseStorage):

    connection_holder = None
    db_name = None
    collection_name = None
    model = None

    def __init__(self, request):
        self.request = request
        self.connection = self.connection_holder.connection

        self.db = self.connection[self.db_name]
        self.collection = self.db[self.collection_name]

    def one(self, model):
        query_doc = {model.id_attribute: model.id}

        result = self.collection.find_one(query_doc)
        if not result:
            raise NotFoundException()

        deserialized = mapping_deserializer(result, model.schema, self.deserialize)
        model.set(deserialized)

    def insert(self, model):
        #todo bad smell, asymmetric model serializer yet mapping deserializer
        serialized = model_serializer(model, model.schema, self.serialize)
        self.collection.insert(serialized)
        deserialized = mapping_deserializer(serialized, model.schema, self.deserialize)
        model.set(deserialized)

    def update(self, model):
        serialized = model_serializer(model, model.schema, self.serialize)
        query_doc = {model.id_attribute: model.id}

        previous = self.collection.find_one(query_doc)
        if not previous:
            raise NotFoundException()

        serialized = merge_document(serialized, previous)

        self.collection.update(query_doc, serialized)

        deserialized = mapping_deserializer(serialized, model.schema, self.deserialize)
        model.set(deserialized)

    def delete(self, model):
        query_doc = {model.id_attribute: model.id}
        result = self.collection.find_one(query_doc)
        if not result:
            raise NotFoundException()

        self.collection.remove(query_doc)


    def all(self, collection, query=None, config=None):
        if config is None:
            config = SearchConfig(0, 0)

        cursor = self.collection.find(spec=query,
                                      fields=self.get_field_list(collection.model.schema),
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

        collection.reset()
        for item in cursor:
            collection.add(mapping_deserializer(item, collection.model.schema, self.deserialize))

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

class EmbeddedMongoStorage(BaseStorage):

    model = None
    parent_storage = None
    attribute_path = None
    empty_schema = None

    def __init__(self, request):
        self.request = request
        self.parent_storage = self.parent_storage(request)

    def insert(self, model):
        parent = model.parent
        self.parent_storage.one(parent)

        collection = parent[self.attribute_path]
        index = len(collection)

        collection.add(model)
        self.parent_storage.update(parent)

        model.set(collection[index].attributes)

    def update(self, model):
        parent = model.parent
        self.parent_storage.one(parent)

        collection = parent[self.attribute_path]
        index = self.find(model.id, collection)

        collection[index] = model
        self.parent_storage.update(parent)

        model.set(collection[index].attributes)

    def one(self, model):
        parent = model.parent
        self.parent_storage.one(parent)

        collection = parent[self.attribute_path]
        index = self.find(model.id, collection)

        model.set(collection[index].attributes)

    def delete(self, model):
        raise NotImplementedError()

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

    def find(self, id, sequence):
        for index, item in enumerate(sequence.models):
            if item.id == id:
                return index
        return None

    def build_parent_schema(self, schema=None):
        parent_id_attribute = self.parent_storage.model.id_attribute
        parent_id_node = filter(lambda c: c.name==parent_id_attribute, self.parent_storage.model.schema.children)[0]

        structure = {
            parent_id_attribute: parent_id_node,
            self.attribute_path: CollectionRefNode(self.model)
        }
        return MappingNode(**structure)

    def __str__(self):
        return "%s mongo embedded storage with parent %s on %s" % (self.model.__name__, self.parent_storage.__class__.__name__, self.attribute_path)

def make_embedded_storage_view(model_type, level):

    class View(object):

        def __init__(self, request):
            self.request = request
            self.schema = model_type.schema
            self.storage = request.resources.get_storage(model_type)

            parents = []
            current_id_level = 0
            current_storage = self.storage
            while current_id_level < level:
                id_name = "id%d" % current_id_level
                current_storage = current_storage.parent_storage
                id = current_storage.model.id_type(self.request.matchdict[id_name])
                parents.append(current_storage.model.with_id(id))
                current_id_level += 1

            self.parents = parents

        def set_parents(self, model):
            current = model
            for parent in self.parents:
                current.parent = parent
                current = parent

        def create(self):
            model = model_type()
            model.set(model.parse(self.request.json_body))
            self.set_parents(model)
            self.storage.insert(model)
            return model.toJSON()

        def read(self):
            model = model_type.with_id(model_type.id_type(self.request.matchdict["id"]))
            self.set_parents(model)
            self.storage.one(model)
            return model.toJSON()

        def update(self):
            model = model_type()
            model.set(model.parse(self.request.json_body))
            self.set_parents(model)
            self.storage.update(model)
            return model.toJSON()

        def delete(self):
            pass

        def list(self):
            skip = self.request.params.get("ps", 0)
            limit = self.request.params.get("pl", 0)
            config = borobudur.resource.storage.SearchConfig(skip, limit)

            results = self.storage.all(self.id, config=config, schema=self.schema)
            sequence_schema = borobudur.schema.SequenceNode(self.schema)
            serialized = sequence_schema.serialize(results)
            return serialized

    return View

class EmbeddedStorageExposer(object):

    def __call__(self, config, resource_root, factory, storage_type):

        model = storage_type.model
        name = model.__name__
        storage_url = model.model_url

        level = 0
        current = storage_type
        while getattr(current, "parent_storage", None):
            current = current.parent_storage
            level += 1

        storage_view = make_embedded_storage_view(model, level)

        for i in range(level):
            storage_url += "/{id%d}" % i

        config.add_route("storage.non_id."+name, resource_root+"storages/"+storage_url, factory=factory)
        config.add_route("storage.id."+name, resource_root+"storages/"+storage_url+"/{id}", factory=factory)

        config.add_view(storage_view, route_name="storage.non_id."+name, attr="list", request_method="GET", renderer="json")
        config.add_view(storage_view, route_name="storage.non_id."+name, attr="create", request_method="POST", renderer="json")
        config.add_view(storage_view, route_name="storage.id."+name, attr="read", request_method="GET", renderer="json")
        config.add_view(storage_view, route_name="storage.id."+name, attr="update", request_method="PUT", renderer="json")
        config.add_view(storage_view, route_name="storage.id."+name, attr="delete", request_method="DELETE", renderer="json")

class ConnectionHolder(object):
    """
    simple class that allows connection to lazily configured
    """
    connection = None

    def bind(self, host, port):
        if self.connection is not None:
            raise ValueError("connection is already bind")
        self.connection = Connection(host, port)
