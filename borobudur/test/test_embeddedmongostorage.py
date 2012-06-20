import unittest
import borobudur.schema
import borobudur.storage
import borobudur.storage.mongo as mongo
from borobudur.storage.mongo import StorageContext
from borobudur.model import Model

import colander
from pprint import pprint

storage_context = StorageContext()
storage_context.connect("localhost, 27017")

comment = borobudur.schema.MappingSchema(
    sender=colander.SchemaNode(colander.String()),
    message=colander.SchemaNode(colander.String()),
)

comments = borobudur.schema.SequenceSchema(comment)

project = borobudur.schema.MappingSchema(
    name=colander.SchemaNode(colander.String()),
    comments=comments,
)

class Project(Model):
    schemas = {
        "": project,
        }
    storage_url = "project"

lazy_projects = borobudur.schema.SequenceSchema(colander.SchemaNode(colander.String()))
projects = borobudur.schema.SequenceSchema(borobudur.schema.RefSchema(Project))

user = borobudur.schema.MappingSchema(
    name=colander.SchemaNode(colander.String()),
    age=colander.SchemaNode(colander.Int()),
    projects=projects,
)

user_lazy_projects = borobudur.schema.MappingSchema(
    name=colander.SchemaNode(colander.String()),
    age=colander.SchemaNode(colander.Int()),
    projects=lazy_projects,
)

class User(Model):
    schemas = {
        "": user,
        "user_lazy_projects": user_lazy_projects,
        }
    storage_url = "user"


@storage_context.register(User)
class UserStorage(mongo.MongoStorage):
    db_name = "test_mongostorage"
    collection_name = "user"

@storage_context.register(Project)
class ProjectStorage(mongo.MongoStorage):
    db_name = "test_mongostorage"
    collection_name = "project"


class TestEmbeddedMongoStorage(unittest.TestCase):

    def setUp(self):
        pass

    def test_insert(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass

    def test_anu(self):
        pass

