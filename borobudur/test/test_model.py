import unittest
import borobudur
import borobudur.schema
import borobudur.storage
import colander

class TestModel(unittest.TestCase):

    def test_create(self):
        a = borobudur.Model()
        self.assertIsNot(a, None)
        self.assertIs(a.get("name"), None)

        a = borobudur.Model({"name": "Joko Suprianto"})
        self.assertEqual(a.get("name"), "Joko Suprianto")

    def test_event(self):
        a = borobudur.Model()
        counter = [0]

        def on_change(model, name):
            counter[0] = counter[0] + 1
            print name

        a.on("change:name", on_change)

        #counter should increment
        a.set({"name": "lalala"})
        self.assertEqual(counter[0], 1)

        #name equals counter should stay
        a.set({"name": "lalala"})
        self.assertEqual(counter[0], 1)

        a.set({"name": "lala"})
        self.assertEqual(counter[0], 2)

    def test_eq(self):
        a = borobudur.Model({"aaa": "4"})
        b = borobudur.Model({"aaa": "4"})
        c = borobudur.Model({"aaa": "5"})

        self.assertEqual(a, b)
        self.assertNotEqual(a, c)


###########################################
# Model with schema
###########################################

#some schema
repository = borobudur.schema.SchemaRepository()
phone = repository.add_mapping("Phone", {
    "number": colander.SchemaNode(colander.String()),
})

friend = repository.add_mapping("Friend", {
    "rank": colander.SchemaNode(colander.Int(), validator=colander.Range(0, 9999)),
    "name": colander.SchemaNode(colander.String()),
    "phone": phone
    })

#create model that creating child by finding namespace in model registry
model_registry = {}
class BaseModel(borobudur.Model):
    def create_child_from_schema(self, attributes, schema):
        return model_registry[schema.schema_namespace](attributes, {"schema": schema})
class PhoneModel(BaseModel): pass
class FriendModel(BaseModel): pass
model_registry["Phone"]=PhoneModel
model_registry["Friend"]=FriendModel

#test it
class TestModelWithSchema(unittest.TestCase):

    def test_relational(self):
        #model with schema auto created
        a = FriendModel({
            "name": "supriadi",
            "rank": 3,
            "phone": {"number": {"8823234"}}
        }, {"schema": friend})
        self.assertTrue(isinstance(a.get("phone"), PhoneModel))

        #model without schema auto created
        b = FriendModel({
            "name": "supriadi",
            "rank": 3,
            "phone": {"number": {"8823234"}}
        })
        self.assertFalse(isinstance(b.get("phone"), PhoneModel))

    def test_validate(self):
        a = FriendModel({
            "name": "supriadi",
            "rank": 3,
            "phone": {"number": {"8823234"}}
        })
        a.schema = friend
        self.assertTrue(a.is_valid())

        b = FriendModel({
            "name": "supriadi",
            "rank": "kutumbaba",
            "phone": {"number": {"8823234"}}
        })
        b.schema = friend
        self.assertFalse(b.is_valid())

        c = FriendModel({
            "name": "supriadi",
            "rank": 20000,
            "phone": {"number": {"8823234"}}
        })
        c.schema = friend
        self.assertFalse(c.is_valid())

    def test_auto_deserialization(self):
        a = FriendModel({
            "name": "supriadi",
            "rank": "5000",
            "phone": {"number": 8823234}
        }, {"schema": friend})

        self.assertEqual(a.get("rank"), 5000)
        self.assertNotEqual(a.get("rank"), "5000")

        self.assertEqual(a.get("phone").get("number"), "8823234")
        self.assertNotEqual(a.get("phone").get("number"), 8823234)

###########################################
# Model with dummy storage
###########################################

class DummyStorage(borobudur.storage.Storage):
    pass

