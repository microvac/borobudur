import colander
from colander import (\
    null, SchemaNode, String, Integer, Boolean, Date, DateTime
)

class Currency(Integer):
    pass

class File(Integer):
    pass

class Ref(object):
    def serialize(self, node, appstruct):
        from bson.dbref import DBRef
        from bson.objectid import ObjectId
        if appstruct is None:
            return null
        if not isinstance(appstruct, DBRef):
            raise colander.Invalid(node, 'input is not DBRef')
        return dict(collection=appstruct.collection, id=str(appstruct.id))

    def deserialize(self, node, cstruct):
        from bson.dbref import DBRef
        from bson.objectid import ObjectId
        if cstruct is null:
            return None
        if not isinstance(cstruct, dict):
            raise colander.Invalid(node, 'input is not a dict')
        elif (cstruct.get("collection") is None) or (cstruct.get("id") is None):
            raise colander.Invalid(node, 'input is not a correct reference')
        result = DBRef(collection=cstruct.get("collection"), id=ObjectId(cstruct.get("id")))
        return result

class RefSchema(colander.SchemaNode):
    """
    prambanan:type target c(object)
    """

    def __init__(self, target, schema_name=""):
        self.target = target
        self.schema_name = schema_name

        node = target.get_schema(schema_name).clone()
        self.typ = node.typ
        self.preparer = node.preparer
        self.validator = node.validator
        self.default = node.default
        self.missing = node.missing
        self.name = node.name
        self.raw_title = node.raw_title
        self.title = node.title
        self.description = node.description
        self.widget = node.widget
        self.children = node.children
        self.order = node._order

    def create_target(self, attributes):
        return self.target(attributes, self.schema_name)

    def clone(self):
        """ Clone the schema node and return the clone.  All subnodes
        are also cloned recursively.  Attributes present in node
        dictionaries are preserved."""
        cloned = self.__class__(self.target, self.schema_name)
        return cloned

class SequenceSchema(colander.SchemaNode):
    def __init__(self, child):
        super(SequenceSchema, self).__init__(colander.Sequence())
        child = child.clone()
        child.name = "child"
        self.add(child)

    def clone(self):
        cloned = self.__class__(self.children[0])
        return cloned

class MappingSchema(colander.SchemaNode):

    def __init__(self, *args, **kwargs):
        super(MappingSchema, self).__init__(colander.Mapping())

        children = {}

        for parent in args:
            for child in parent.children:
                children[child.name] = child

        for key in kwargs:
            child = kwargs.get(key)
            child.name = key
            children[key] = child

        for key in children:
            child = children[key]
            child.name = key
            self.add(child)

    def clone(self):
        cloned = MappingSchema()
        cloned.children = list(self.children)
        return cloned
