import unittest
import borobudur.schema
import borobudur.storage
import borobudur.storage.mongo as mongo
from borobudur.storage.mongo import StorageContext
import colander
from pprint import pprint

storage_context = StorageContext()
storage_context.connect("localhost, 27017")

@storage_context.register("User", "test_mongostorage", "user")
class UserStorage(mongo.MongoStorage):
    pass

@storage_context.register("Project", "test_mongostorage", "project")
class ProjectStorage(mongo.MongoStorage):
    pass

schemas = borobudur.schema.SchemaRepository()

comment = schemas.add_mapping("Comment", {
    "sender": colander.SchemaNode(colander.String()),
    "message": colander.SchemaNode(colander.String()),
    })

comments = schemas.add_sequence("Comments", comment)

project = schemas.add_mapping("Project", {
    "name": colander.SchemaNode(colander.String()),
    "comments": comments
})

projects = schemas.add_sequence("Projects", project)

user = schemas.add_mapping("User", {
    "name": colander.SchemaNode(colander.String()),
    "age": colander.SchemaNode(colander.Int()),
    "projects": projects
})

lazy_projects = borobudur.schema.anonymous_sequence(colander.SchemaNode(borobudur.schema.Ref()))
user_lazy_projects = schemas.modify(user, "lazy", {
    "alter" : {
        "projects": lazy_projects,
    }
})


class TestMongoStorage(unittest.TestCase):

    def setUp(self):
        storage_context.connection.drop_database("test_mongostorage")

        comment_1 = dict(sender="Komentator1", message="Komentator1 disini!")
        comment_2 = dict(sender="Komentator2", message="Komentator2 euy!")
        comment_3 = dict(sender="Komentator3", message="Lapor Komentator3")
        comment_4 = dict(sender="Komentator4", message="...")
        project_1 = dict(name="Project1", comments=[comment_1, comment_2])
        project_2 = dict(name="Project2", comments=[comment_3, comment_4])
        self.user = dict(name="Tester", age=27, projects=[project_1, project_2])

        comment_1b = dict(sender="Kom1b", message="Kom1b disini!")
        comment_2b = dict(sender="Kom2b", message="Kom2b euy!")
        comment_3b = dict(sender="Kom3b", message="Lapor Kom3b!")
        project_1b = dict(name="Project1b", comments=[comment_1b, comment_2b, comment_3b])
        self.user_b = dict(name="UserB", age=25, projects=[project_1b])

    def test_insert(self):
        user_storage = storage_context.get("User")
        obj = user_storage.insert(self.user, user)
        #result = user_storage.one(obj['_id'], user)
        pprint(obj)
        self.assertIsNotNone(obj['_id'])

    def test_update(self):
        user_storage = storage_context.get("User")
        test = user_storage.insert(self.user, user)
        obj = user_storage.one(test['_id'], user)
        obj["name"] = "Tralala"
        obj["projects"][0]["comments"][0]["sender"] = "Trululu"
        user_storage.update(obj, user)
        result = user_storage.one(obj['_id'], user)
        self.assertEqual(result, obj)

    def test_delete(self):
        user_storage = storage_context.get("User")
        test = user_storage.insert(self.user, user)
        self.assertIsNotNone(user_storage.one(test["_id"], user))
        user_storage.delete(test["_id"])
        self.assertIsNone(user_storage.one(test["_id"], user))

    def test_lazy_loading(self):
        user_storage = storage_context.get("User")
        test = user_storage.insert(self.user, user)
        result = user_storage.one(test["_id"], user_lazy_projects)
        self.assertEqual(test, result)

    def test_all_and_count(self):
        storage_context.connection.drop_database("test")
        user_storage = storage_context.get("User")

        test1 = user_storage.insert(self.user, user)
        test2 = user_storage.insert(self.user, user)
        test3 = user_storage.insert(self.user, user)
        test4 = user_storage.insert(self.user, user)
        test5 = user_storage.insert(self.user, user)
        test6 = user_storage.insert(self.user_b, user)
        test7 = user_storage.insert(self.user_b, user)
        test8 = user_storage.insert(self.user_b, user)

        #search all
        result = user_storage.all(query=None, schema=user)
        #pprint(result)
        print("=============================================")
        print("Count: ") + str(len(result))
        print("=============================================")
        self.assertEqual(user_storage.count(query=None), 8)

        #search all with skip and limit
        config = borobudur.storage.SearchConfig(4, 5)
        result = user_storage.all(query=None, config=config, schema=user)
        #pprint(result)
        print("=============================================")
        print("Count: ") + str(len(result))
        print("=============================================")
        self.assertEqual(len(result), 4)

        #search with sort descending
        config = borobudur.storage.SearchConfig(0, 0)
        config.sorts.append(borobudur.storage.SearchSort("name", "desc"))
        result = user_storage.all(query=None, config=config, schema=user)
        #pprint(result)
        print("=============================================")
        print("Count: ") + str(len(result))
        print("=============================================")

        #search with query
        query = {
            "name": "UserB"
        }
        result = user_storage.all(query=query, schema=user)
        #pprint(result)
        print("=============================================")
        print("Count: ") + str(len(result))
        print("=============================================")
        self.assertEqual(user_storage.count(query=query), 3)