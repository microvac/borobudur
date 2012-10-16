import borobudur
from borobudur import NotFoundException
from zope.interface.interface import Interface
from borobudur.model import Collection
from pyramid.response import Response
import json

class StorageException(Exception):
    pass

class SearchSort(object):
    """
    configuration for sorting, see SearchConfig
    """
    def __init__(self, criteria, order="asc"):
        self.criteria = criteria
        self.order = order

class SearchConfig(object):
    """
    configuration for paging and sorting when search in storage

    ``
        conf = SearchConfig(10, 20)
        conf.sorts.append(SearchSort("name"))
        conf.sorts.append(SearchSort("age", "desc"))
    ``
    """
    def __init__(self, skip=0, limit=0, sorts=None):
        self.skip = skip
        self.limit = limit
        if sorts is None:
            sorts = []
        self.sorts = sorts

def wrap_error(fn):
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except NotFoundException as e:
            err = {}
            err["type"] = "Not Found"
            return Response(json.dumps(err), status=404, content_type="application/json")
    return wrapped

def make_id(model_type, str_id):
    try:
        return model_type.id_type(str_id)
    except Exception:
        raise NotFoundException()

def make_storage_view(model_type):


    class View(object):

        def __init__(self, request):
            self.request = request
            self.storage = request.resources.get_storage(model_type)
            self.schema = model_type.schema

        @wrap_error
        def create(self):
            model = model_type()
            model.set(model.parse(self.request.json_body))
            self.storage.insert(model)
            return model.toJSON()

        @wrap_error
        def update(self):
            id = make_id(model_type, self.request.matchdict["id"])
            model = model_type()
            model.set(model.parse(self.request.json_body))
            if id != model.id:
                raise borobudur.InvalidRequestException("id doesnt matches")

            self.storage.update(model)
            return model.toJSON()

        @wrap_error
        def read(self):
            id = make_id(model_type, self.request.matchdict["id"])
            model = model_type.with_id(id)
            self.storage.one(model)
            return model.toJSON()

        @wrap_error
        def delete(self):
            id = make_id(model_type, self.request.matchdict["id"])
            model = model_type.with_id(id)
            self.storage.delete(model)
            return True

        @wrap_error
        def list(self):
            collection = Collection(model_type)

            skip = self.request.params.get("ps", 0)
            limit = self.request.params.get("pl", 0)
            sort_order = self.request.params.get("so")
            sort_criteria = self.request.params.get("sc")
            query = self.storage.model.deserialize_queries(self.request.params)
            sorts = None
            if sort_criteria and sort_order:
                sorts = borobudur.resource.storage.SearchSort(sort_criteria, sort_order)
            elif sort_criteria:
                sorts = borobudur.resource.storage.SearchSort(sort_criteria)

            config = borobudur.resource.storage.SearchConfig(skip, limit, sorts)

            self.storage.all(collection, query=query, config=config)
            return collection.toJSON()

    return View

class StorageExposer(object):

    def __call__(self, config, resource_root, factory, storage_type):
        model_type = storage_type.model
        name = model_type.__name__
        storage_url = model_type.model_url

        storage_view = make_storage_view(model_type)

        config.add_route("storage.non_id."+name, resource_root+"storages/"+storage_url, factory=factory)
        config.add_route("storage.id."+name, resource_root+"storages/"+storage_url+"/{id}", factory=factory)

        config.add_view(storage_view, route_name="storage.non_id."+name, attr="list", request_method="GET", renderer="json")
        config.add_view(storage_view, route_name="storage.non_id."+name, attr="create", request_method="POST", renderer="json")
        config.add_view(storage_view, route_name="storage.id."+name, attr="read", request_method="GET", renderer="json")
        config.add_view(storage_view, route_name="storage.id."+name, attr="update", request_method="PUT", renderer="json")
        config.add_view(storage_view, route_name="storage.id."+name, attr="delete", request_method="DELETE", renderer="json")


class IStorage(Interface):
    """
    Interface that define contracts for Borobudur storage implementations
    """

    def insert(self, obj, schema=None):
        """
        Create new record in storage which represent obj

        - obj is a valid result of colander serialization
        - save mutated obj if change obj after save,
            e.g. auto generate id sets obj[id]
        - schema defines what fields in obj to be saved
        - if schema is None, save all given field

        raise StorageException if something wrong
        returns saved mutated obj
        """

    def update(self, obj, schema=None):
        """
        Update obj representation in storage

        - obj is a valid result of colander serialization
        - save mutated obj if change obj after save
        - schema defines what fields in obj to be saved
        - if schema is None, save all given field

        raise StorageException if something wrong
        returns saved mutated obj
        """

    def delete(self, id):
        """
        delete a single record in storage identified by id

        raise StorageException if something wrong

        returns void
            if implementation delete without assuring such records exists before,
            but assured that if such records exists, it will be deleted
        returns True
            if implementation assured that such record exists, and that records deleted
        raise ValueError
            if implementation provide checking existence of records, and does not find it
        """

    def one(self, id, schema=None):
        """
        get a single record in storage identified by id

        - schema defines what fields will be retrieved
        - if schema is None, retrieve all available fields

        raise StorageException if something wrong
        returns obj that can be deserialized by colander
        returns None if not finding anything
        """

    def all(self, query=None, config=None, schema=None):
        """
        get a list of records that matches query


        - query is implementation specific i.e. any object that help implementation to find something, query can be None
        - config is borobudur.storage.SearchConfig
        - schema defines what fields will be retrieved
        - if schema is None, retrieve all available fields

        raise StorageException if something wrong
        returns list of obj that can be deserialized by colander
        """

    def count(self, query=None):
        """
        get number of records that matches query

        - query is implementation specific i.e. any object that help implementation to find something, query can be None

        raise StorageException if something wrong
        returns number
        """

    # delete all that dummy methods
    del insert, update, delete, one, all, count
