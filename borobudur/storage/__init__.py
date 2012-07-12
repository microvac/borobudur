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

class Storage(object):
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
