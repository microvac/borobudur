import unittest
from pprint import pprint
from borobudur.jslib.backbone import (
    Model,
    Collection
)

class TestCollection(unittest.TestCase):

    def setUp(self):
        self.id = 0
        self.result = []
        self.collection = Collection()
        def callback(model, collection, options):
            self.result.append(dict(id=model.id, index=options.get("index"), name=model.get("name")))

        self.collection.on("add", callback)
        self.collection.on("remove", callback)

    def prepare(self, add=False):
        self.collection.reset()
        self.id = 0
        self.result = []

        self.tester = Model({"name": "Tester", "age": 23})
        self.tester.id = self.id
        self.id += 1

        self.tester2 = Model({"name": "Tester2", "age": 17})
        self.tester2.id = self.id
        self.id += 1

        self.tester3 = Model({"name": "Tester3", "age": 25})
        self.tester3.id = self.id
        self.id += 1

        if not add:
            models = [self.tester, self.tester2, self.tester3]
            self.collection.add(models, {"silent": True})

    def test_add(self):
        self.prepare(add=True)

        #Add one model
        self.collection.add(self.tester)
        result = dict(id=self.tester.id, index=0, name=self.tester.get("name"))
        self.assertEqual(self.result[0], result)
        self.assertEqual(self.collection.length, 1)
        #pprint(self.result)

        #Add two models
        models = [self.tester2, self.tester3]
        self.collection.add(models)
        result = dict(id=self.tester2.id, index=1, name=self.tester2.get("name"))
        result2 = dict(id=self.tester3.id, index=2, name=self.tester3.get("name"))
        self.assertEqual(self.result[1], result)
        self.assertEqual(self.result[2], result2)
        self.assertEqual(self.collection.length, 3)
        #pprint(self.result)

    def test_remove(self):
        self.prepare()

        #Remove one model
        self.collection.remove(self.tester2)
        result = dict(id=self.tester2.id, index=1, name=self.tester2.get("name"))
        result2 = self.collection.get(self.tester2.id)

        self.assertEqual(self.result[0], result)
        self.assertIsNone(result2)
        self.assertEqual(self.collection.length, 2)

        self.collection.remove(self.tester3)
        result = dict(id=self.tester3.id, index=1, name=self.tester3.get("name"))
        result2 = self.collection.get(self.tester3.id)

        self.assertEqual(self.result[1], result)
        self.assertIsNone(result2)
        self.assertEqual(self.collection.length, 1)

        #Reset and remove multiple models
        self.prepare()

        self.collection.remove([self.tester, self.tester2])
        result = dict(id=self.tester.id, index=0, name=self.tester.get("name"))
        result2 = dict(id=self.tester2.id, index=1, name=self.tester2.get("name"))

        self.assertEqual(self.result[0], result)
        self.assertEqual(self.result[1], result2)
        self.assertEqual(self.collection.length, 1)

    def test_toJSON(self):
        self.prepare()
        pprint(self.collection.toJSON())

    def test_push(self):
        self.prepare()
        tester4 = Model({"name":"Tester4"})
        tester4.id = self.id
        self.id += 1

        self.collection.push(tester4)
        result = dict(id=tester4.id, index=3, name=tester4.get("name"))
        self.assertEqual(self.result[0], result)
        self.assertEqual(self.collection.at(self.collection.length-1), tester4)
        self.assertEqual(self.collection.length, 4)


    def test_pop(self):
        self.prepare()
        model = self.collection.pop()
        self.assertEqual(model, self.tester3)

    def test_unshift(self):
        self.prepare()
        tester4 = Model({"name":"Tester4"})
        tester4.id = self.id
        self.id += 1

        self.collection.unshift(tester4)
        result = dict(id=tester4.id, index=0, name=tester4.get("name"))
        self.assertEqual(self.result[0], result)
        self.assertEqual(self.collection.at(0), tester4)
        self.assertEqual(self.collection.length, 4)

    def test_shift(self):
        self.prepare()
        model = self.collection.shift()
        self.assertEqual(model, self.tester)

    def test_get(self):
        self.prepare()
        model = self.collection.get(1)
        self.assertEqual(model, self.tester2)

    def test_at(self):
        self.prepare()
        model = self.collection.at(self.collection.length-1)
        self.assertEqual(model, self.tester3)

    def test_where(self):
        self.prepare()
        models = self.collection.where({"name": "Tester3"})
        self.assertEqual(models[0], self.tester3)

    def test_pluck(self):
        self.prepare()
        attrs = self.collection.pluck("name")
        pprint(attrs)

    def test_setitem_getitem(self):
        self.prepare()
        tester4 = Model({"name": "Tester4"})

        #Modify existing
        tester4.id = self.collection[2].id
        self.collection[2] = tester4

        #Out of range index
        tester5 = Model({"name": "Tester5"})
        tester5.id = self.id
        self.id += 1
        self.collection[10] = tester5

        a = self.collection[2]
        b = self.collection[3]
        result = dict(id=tester5.id, index=3, name=tester5.get("name"))

        self.assertEqual(self.result[0], result)
        self.assertEqual(self.collection.length, 4)
        self.assertEqual(a, tester4)
        self.assertEqual(b, tester5)


