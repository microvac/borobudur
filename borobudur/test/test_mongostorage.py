import unittest
import borobudur.schema
import borobudur.storage.context
import borobudur.storage.mongo as mongo
import colander
from pprint import pprint

storage_context = borobudur.storage.context.StorageContext('localhost', 27017)

@storage_context.register("User", "test", "user")
class UserStorage(mongo.MongoStorage):
    pass

@storage_context.register("Project", "test", "project")
class ProjectStorage(mongo.MongoStorage):
    pass

repository = borobudur.schema.SchemaRepository()

comment = repository.add_mapping("Comment", {
    "sender": colander.SchemaNode(colander.String()),
    "message": colander.SchemaNode(colander.String()),
    })

comments = repository.add_sequence("Comments", comment)

project = repository.add_mapping("Project", {
    "name": colander.SchemaNode(colander.String()),
    "comments": comments
})

projects = repository.add_sequence("Projects", project)

user = repository.add_mapping("User", {
    "name": colander.SchemaNode(colander.String()),
    "age": colander.SchemaNode(colander.Int()),
    "projects": projects
})

class TestMongoStorage(unittest.TestCase):

    def setUp(self):
        self.storage_context = storage_context
        self.storage_context.connection.drop_database("test")

        comment_1 = dict(sender="Komentator1", message="Komentator1 disini!")
        comment_2 = dict(sender="Komentator2", message="Komentator2 euy!")
        comment_3 = dict(sender="Komentator3", message="Lapor Komentator3")
        comment_4 = dict(sender="Komentator4", message="...")

        project_1 = dict(name="Project1", comments=[comment_1, comment_2])
        project_2 = dict(name="Project2", comments=[comment_3, comment_4])

        self.user = dict(name="Tester", age=27, projects=[project_1, project_2])

    def test_insert(self):
        user_storage = self.storage_context.get("User")
        obj = user_storage.insert(self.user, user)
        result = user_storage.one(obj['_id'], user)
        pprint(obj)

    def test_update(self):
        user_storage = self.storage_context.get("User")
        test = user_storage.insert(self.user, user)
        obj = user_storage.one(test['_id'], user)
        obj["name"] = "Tralala"
        obj["projects"][0]["comments"][0]["sender"] = "Trululu"
        user_storage.update(obj, user)
        result = user_storage.one(obj['_id'], user)
        self.assertEqual(result, obj)

    def test_delete(self):
        user_storage = self.storage_context.get("User")
        test = user_storage.insert(self.user, user)
        self.assertIsNotNone(user_storage.one(test["_id"], user))
        user_storage.delete(test["_id"])
        self.assertIsNone(user_storage.one(test["_id"], user))



