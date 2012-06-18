import unittest
import borobudur
import borobudur.schema
import borobudur.storage
import borobudur.model
import colander

from borobudur.schema import MappingSchema

class TestModel(unittest.TestCase):

    def test_create(self):
        a = borobudur.model.Model()
        self.assertIsNot(a, None)
        self.assertIs(a.get("name"), None)

        a = borobudur.model.Model({"name": "Joko Suprianto"})
        self.assertEqual(a.get("name"), "Joko Suprianto")

    def test_event(self):
        a = borobudur.model.Model()
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
        a = borobudur.model.Model({"aaa": "4"})
        b = borobudur.model.Model({"aaa": "4"})
        c = borobudur.model.Model({"aaa": "5"})

        self.assertEqual(a, b)
        self.assertNotEqual(a, c)


###########################################
# Model with schema
###########################################


#create model that creating child by finding namespace in model registry
PhoneSchema = MappingSchema(
    number = colander.SchemaNode(colander.String())
)

class Phone(borobudur.model.Model):
    schemas = {
        "": PhoneSchema
    }

FriendSchema = MappingSchema(
    rank= colander.SchemaNode(colander.Int(), validator=colander.Range(0, 9999)),
    name = colander.SchemaNode(colander.String()),
    phone = borobudur.schema.RefSchema(Phone),
)

class Friend(borobudur.model.Model):
    schemas = {
        "": FriendSchema
    }

class TestModelWithSchema(unittest.TestCase):

    def test_relational(self):
        #model with schema auto created
        a = Friend({
            "name": "supriadi",
            "rank": 3,
            "phone": {"number": {"8823234"}}
        }, schema_name =  "")
        self.assertTrue(isinstance(a.get("phone"), Phone))

        #model without schema auto created
        b = Friend({
            "name": "supriadi",
            "rank": 3,
            "phone": {"number": {"8823234"}}
        })
        self.assertFalse(isinstance(b.get("phone"), Phone))

    def test_validate(self):
        a = Friend({
            "name": "supriadi",
            "rank": 3,
            "phone": {"number": {"8823234"}}
        })
        a.schema = Friend.get_schema()
        self.assertTrue(a.is_valid())

        b = Friend({
            "name": "supriadi",
            "rank": "kutumbaba",
            "phone": {"number": {"8823234"}}
        })
        b.schema = Friend.get_schema()
        self.assertFalse(b.is_valid())

        c = Friend({
            "name": "supriadi",
            "rank": 20000,
            "phone": {"number": {"8823234"}}
        })
        c.schema = Friend.get_schema()
        self.assertFalse(c.is_valid())

    def test_auto_deserialization(self):
        a = Friend({
            "name": "supriadi",
            "rank": "5000",
            "phone": {"number": 8823234}
        }, schema_name="")

        self.assertEqual(a.get("rank"), 5000)
        self.assertNotEqual(a.get("rank"), "5000")

        self.assertEqual(a.get("phone").get("number"), "8823234")
        self.assertNotEqual(a.get("phone").get("number"), 8823234)

