import borobudur
from zope.interface.interface import Interface

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

def make_storage_view(model):

    schemas = {}

    for name, schema in model.schemas.items():
        new_schema = schema.clone()
        for child in new_schema.children:
            child.missing = None
        schemas[name] = new_schema

    class View(object):

        def __init__(self, request):
            self.request = request
            self.storage = request.resources.get_storage(model)
            self.schema = schemas[request.params.get("s", "")]

        def create(self):
            appstruct = self.schema.deserialize(self.request.json_body)
            result = self.storage.insert(appstruct, self.schema)
            serialized = self.schema.serialize(result)
            return serialized

        def read(self):
            result = self.storage.one(self.request.matchdict["id"], self.schema)
            serialized = self.schema.serialize(result)
            return serialized

        def update(self):
            appstruct = self.schema.deserialize(self.request.json_body)
            result = self.storage.update(appstruct, self.schema)
            serialized = self.schema.serialize(result)
            return serialized

        def delete(self):
            result = self.storage.delete(self.request.matchdict["id"])
            return result

        def list(self):
            skip = self.request.params.get("ps", 0)
            limit = self.request.params.get("pl", 0)
            sort_order = self.request.params.get("so")
            sort_criteria = self.request.params.get("sc")
            query = self.storage.model.deserialize_queries(self.request.params)
            sorts = None
            if sort_criteria and sort_order:
                sorts = borobudur.storage.SearchSort(sort_criteria, sort_order)
            elif sort_criteria:
                sorts = borobudur.storage.SearchSort(sort_criteria)

            config = borobudur.storage.SearchConfig(skip, limit, sorts)

            results = self.storage.all(query=query, schema=self.schema, config=config)
            sequence_schema = borobudur.schema.SequenceNode(self.schema)
            serialized = sequence_schema.serialize(results)
            return serialized

    return View

class StorageExposer(object):

    def __call__(self, config, resource_root, factory, storage_type):
        model = storage_type.model
        name = model.__name__
        storage_url = model.model_url

        storage_view = make_storage_view(model)

        config.add_route("non_id"+name, resource_root+"storages/"+storage_url, factory=factory)
        config.add_route("id_"+name, resource_root+"storages/"+storage_url+"/{id}", factory=factory)

        config.add_view(storage_view, route_name="non_id"+name, attr="list", request_method="GET", renderer="json")
        config.add_view(storage_view, route_name="non_id"+name, attr="create", request_method="POST", renderer="json")
        config.add_view(storage_view, route_name="id_"+name, attr="read", request_method="GET", renderer="json")
        config.add_view(storage_view, route_name="id_"+name, attr="update", request_method="PUT", renderer="json")
        config.add_view(storage_view, route_name="id_"+name, attr="delete", request_method="DELETE", renderer="json")


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
