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

class Comment(Model):
    id_attribute = "sender"
    id_type = str

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

@storage_context.register
class UserStorage(mongo.MongoStorage):
    model = User
    db_name = "test_mongostorage"
    collection_name = "user"

@storage_context.register
class ProjectStorage(mongo.MongoStorage):
    model = Project
    db_name = "test_mongostorage"
    collection_name = "project"

@storage_context.register_embedded
class CommentStorage(mongo.EmbeddedMongoStorage):
    parent_storage = ProjectStorage
    attribute_path = "comments"
    model = Comment
    empty_schema = borobudur.schema.MappingSchema(
        sender = colander.SchemaNode(colander.String())
    )

class TestMongoStorage(unittest.TestCase):

    def setUp(self):
        storage_context.connection.drop_database("test_mongostorage")

    def prepare(self):
        comment_1 = dict(sender="Komentator1", message="Komentator1 disini!")
        comment_2 = dict(sender="Komentator2", message="Komentator2 euy!")
        comment_3 = dict(sender="Komentator3", message="Lapor Komentator3")
        comment_4 = dict(sender="Komentator4", message="...")
        comment_1b = dict(sender="Kom1b", message="Kom1b disini!")
        comment_2b = dict(sender="Kom2b", message="Kom2b euy!")
        comment_3b = dict(sender="Kom3b", message="Lapor Kom3b!")
        project_1 = dict(name="Project1", comments=[comment_1, comment_2])
        project_2 = dict(name="Project2", comments=[comment_3, comment_4])
        project_1b = dict(name="Project1b", comments=[comment_1b, comment_2b, comment_3b])

        self.project_storage = storage_context.get(Project)
        self.project_1 = self.project_storage.insert(project_1, project)
        self.project_2 = self.project_storage.insert(project_2, project)
        self.project_1b = self.project_storage.insert(project_1b, project)

        self.user_storage = storage_context.get(User)
        self.user_1 = dict(name="Tester", age=27, projects=[self.project_1, self.project_2])
        self.user_2 = dict(name="UserB", age=25, projects=[self.project_1b])
        self.user_a = self.user_storage.insert(self.user_1, user)
        self.user_b = self.user_storage.insert(self.user_2, user)

    def test_insert(self):
        storage_context.connection.drop_database("test_mongostorage")
        self.prepare()
        self.assertIsNotNone(self.user_a[User.id_attribute])

    def test_update(self):
        storage_context.connection.drop_database("test_mongostorage")
        self.prepare()
        obj = self.user_storage.one(str(self.user_a[User.id_attribute]), user)
        obj["name"] = "Tralala"
        obj["projects"][0]["comments"][0]["sender"] = "Trululu"
        proj_obj = self.project_storage.one(str(self.project_1[Project.id_attribute]), project)
        proj_obj["comments"][0]["sender"] = "Trululu"
        self.project_storage.update(proj_obj, project)
        self.user_storage.update(obj, user)
        result = self.user_storage.one(str(self.user_a[User.id_attribute]), user)
        #pprint(result)
        #pprint(obj)
        self.assertEqual(result, obj)

    def test_delete(self):
        storage_context.connection.drop_database("test_mongostorage")
        self.prepare()
        self.assertIsNotNone(self.user_storage.one(str(self.user_a[User.id_attribute]), user))
        self.user_storage.delete(self.user_a[User.id_attribute])
        self.assertIsNone(self.user_storage.one(str(self.user_a[User.id_attribute]), user))

    def test_lazy_loading(self):
        storage_context.connection.drop_database("test_mongostorage")
        self.prepare()
        result = self.user_storage.one(str(self.user_a[User.id_attribute]), user_lazy_projects)
        self.assertEqual(self.user_a, result)

    def test_all_and_count(self):
        storage_context.connection.drop_database("test_mongostorage")
        self.prepare()

        test1 = self.user_storage.insert(self.user_1, user)
        test2 = self.user_storage.insert(self.user_1, user)
        test3 = self.user_storage.insert(self.user_1, user)
        test4 = self.user_storage.insert(self.user_1, user)
        test5 = self.user_storage.insert(self.user_1, user)
        test6 = self.user_storage.insert(self.user_2, user)
        test7 = self.user_storage.insert(self.user_2, user)
        test8 = self.user_storage.insert(self.user_2, user)

        #search all
        result = self.user_storage.all(query=None, schema=user)
        #pprint(result)
        print("=============================================")
        print("Count: ") + str(len(result))
        print("=============================================")
        self.assertEqual(self.user_storage.count(query=None), 10)

        #search all with skip and limit
        config = borobudur.storage.SearchConfig(4, 10)
        result = self.user_storage.all(query=None, config=config, schema=user)
        #pprint(result)
        print("=============================================")
        print("Count: ") + str(len(result))
        print("=============================================")
        self.assertEqual(len(result), 6)

        #search with sort descending
        config = borobudur.storage.SearchConfig(0, 0)
        config.sorts.append(borobudur.storage.SearchSort("name", "desc"))
        result = self.user_storage.all(query=None, config=config, schema=user)
        #pprint(result)
        print("=============================================")
        print("Count: ") + str(len(result))
        print("=============================================")

        #search with query
        query = { "name": "UserB" }
        result = self.user_storage.all(query=query, schema=user)
        #pprint(result)
        print("=============================================")
        print("Count: ") + str(len(result))
        print("=============================================")
        self.assertEqual(self.user_storage.count(query=query), 4)

    #=============================================
    #This section is for EmbeddedMongoStorage tests
    #=============================================

    def prepare_embedded(self):
        self.comment_storage = storage_context.get_embedded(Comment)

    def test_embedded_insert(self):
        storage_context.connection.drop_database("test_mongostorage")
        self.prepare()
        self.prepare_embedded()

        comment_1 = dict(sender="Commentator_1", message="This is Commentator_1")
        comment_2 = dict(sender="Commentator_2", message="This is Commentator_2")

        project_id = (str(self.project_1[Project.id_attribute]),None)

        self.comment_storage.insert(project_id, comment_1, comment)
        self.comment_storage.insert(project_id, comment_2, comment)

        result_1 = self.comment_storage.one(project_id, comment_1[Comment.id_attribute], comment)
        result_2 = self.comment_storage.one(project_id, comment_2[Comment.id_attribute], comment)

        self.assertEqual(comment_1, result_1)
        self.assertEqual(comment_2, result_2)

    def test_embedded_update(self):
        storage_context.connection.drop_database("test_mongostorage")
        self.prepare()
        self.prepare_embedded()

        comment_1 = dict(sender="Commentator_1", message="This is Commentator_1")
        comment_2 = dict(sender="Commentator_2", message="This is Commentator_2")

        project_id = (str(self.project_1[Project.id_attribute]),None)

        self.comment_storage.insert(project_id, comment_1, comment)
        result = self.comment_storage.one(project_id, comment_1[Comment.id_attribute], comment)
        result["message"] = "LALALALALALA"
        self.comment_storage.update(project_id, result, comment)
        result2 = self.comment_storage.one(project_id, comment_1[Comment.id_attribute], comment)
        self.assertEqual(result, result2)

    def test_embedded_all(self):
        storage_context.connection.drop_database("test_mongostorage")
        self.prepare()
        self.prepare_embedded()

        results = self.comment_storage.all((str(self.project_1[Project.id_attribute]),None), schema=comment)
        count = self.comment_storage.count((str(self.project_1[Project.id_attribute]),None))
        self.assertEqual(len(results), count)






