import unittest
import colander
import borobudur.storage.mongo
import pymongo

class Friend(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    age = colander.SchemaNode(colander.Int())

class Friends(colander.SequenceSchema):
    friend = Friend()

class Person(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    age = colander.SchemaNode(colander.Int())
    friends = Friends()

class TestMongoSerializer(unittest.TestCase):

    def setUp(self):
        friend_1 = dict(name="erasmus", age=25)
        friend_2 = dict(name="saranggi", age=24)
        self.person = dict(name="lalala", age=25, friends=[friend_1, friend_2])
        self.schema = Person()

        self.connection = pymongo.Connection('localhost', 27017)
        self.db = self.connection['test']
        self.collection = self.db['test']

    def test_deserialize(self):
        result = borobudur.storage.mongo.mapping_deserializer(self.person, self.schema)
        self.assertEqual(self.person, result)

    def test_serialize(self):
        deserialized = borobudur.storage.mongo.mapping_deserializer(self.person, self.schema)
        result = borobudur.storage.mongo.mapping_serializer(deserialized, self.schema)
        self.assertEqual(self.person, result)

    def tearDown(self):
        pass
