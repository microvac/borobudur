import unittest
from borobudur.model import ModelRefNode
import borobudur.schema
import colander


class TestRef(unittest.TestCase):

    def test_ref(self):
        class ReferencedSchema(object):
            age = colander.SchemaNode(colander.Integer())

        class ReferenceHolder(object):
            @staticmethod
            def get_schema(schema_name=""):
                return borobudur.schema.schema_node_from_class(ReferencedSchema)

        class ReferencingSchema(object):
            name = colander.SchemaNode(colander.String())
            ref = ModelRefNode(ReferenceHolder)

        schema = borobudur.schema.schema_node_from_class(ReferencingSchema)
        obj = schema.deserialize({"name": "Kutumbaba", "ref": {"age": 2}})
        print obj

