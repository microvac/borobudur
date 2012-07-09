import colander
from colander import (\
    null, Integer, String, Date, DateTime, Float, Decimal, Time, Boolean
    )

def make_schemas(default_shema, **named_schemas):
    result = {"": default_shema}
    for name in named_schemas:
        result[name] = named_schemas.get(name)
    return result

def clone_node(source, target):
    target.typ = source.typ
    target.preparer = source.preparer
    target.validator = source.validator
    target.default = source.default
    target.missing = source.missing
    target.name = source.name
    target.raw_title = source.raw_title
    target.title = source.title
    target.description = source.description
    target.widget = source.widget
    target._order = source._order

    target.children = []
    for child in source.children:
        target.children.append(child)

class ObjectId(object):
    def serialize(self, node, appstruct):
        from bson.objectid import ObjectId as OID
        if appstruct is None:
            return null
        if not isinstance(appstruct, OID):
            raise colander.Invalid(node, 'Input is not ObjectId')
        return appstruct.__str__()

    def deserialize(self, node, cstruct):
        from bson.objectid import ObjectId
        from bson.objectid import InvalidId
        if cstruct is null:
            return None
        try:
            result = ObjectId(cstruct)
        except TypeError:
            raise colander.Invalid(node, 'input is not a string')
        except InvalidId:
            raise colander.Invalid(node, 'input is not a valid id')
        return result

class Currency(Integer):
    pass

class File(Integer):
    pass

class TypedNode(colander.SchemaNode):

    def __init__(self, **kwargs):
        super(TypedNode, self).__init__(self.typ, **kwargs)


    def clone(self):
        cloned = self.__class__()
        clone_node(self, cloned)
        return cloned

class StringNode(TypedNode):
    typ = String()

class BooleanNode(TypedNode):
    typ = Boolean()

class IntegerNode(TypedNode):
    typ = Integer()

class FloatNode(TypedNode):
    typ = Float()

class DecimalNode(TypedNode):
    typ = Integer()

class DateTimeNode(TypedNode):
    typ = DateTime()

class DateNode(TypedNode):
    typ = Date()

class TimeNode(TypedNode):
    typ = Time()

class FileNode(TypedNode):
    typ = File()

class CurrencyNode(TypedNode):
    typ = Currency()

class ObjectIdNode(TypedNode):
    typ = ObjectId()

class MappingNode(colander.SchemaNode):

    def __init__(self, *args, **kwargs):
        super(MappingNode, self).__init__(colander.Mapping())

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
        cloned = MappingNode()
        clone_node(self, cloned)
        return cloned

class SequenceNode(colander.SchemaNode):

    def __init__(self, child):
        super(SequenceNode, self).__init__(colander.Sequence())
        child = child.clone()
        child.name = "child"
        self.add(child)

    def clone(self):
        cloned = self.__class__(self.children[0])
        return cloned
