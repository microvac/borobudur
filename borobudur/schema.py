import colander
import operator

class SchemaRepository(object):

    def __init__(self):
        self.schemas = {}

    def register(self, schema):
        key = schema.schema_namespace if (schema.schema_name == "") else ("%s.%s" % (schema.schema_namespace, schema.schema_name))
        self.schemas[key] = schema
        return schema

    def get(self, schema_namespace, schema_name = ""):
        key = schema_namespace if (schema_name == "") else ("%s.%s" % (schema_namespace, schema_name))
        return self.schemas[key]

    def add_mapping(self, schema_namespace, nodes):
        schema = colander.SchemaNode(colander.Mapping())
        schema.schema_name = ""
        schema.schema_namespace = schema_namespace

        for key, child in sorted(nodes.items(), key=lambda (k,v):  v._order):
            child = child.clone()
            child.name = key
            schema.add(child)

        return self.register(schema)

    def add_sequence(self, schema_namespace, child):
        schema = colander.SchemaNode(colander.Sequence())
        schema.schema_name = child.schema_name
        schema.schema_namespace = schema_namespace

        child = child.clone()
        child.name = "child"
        schema.add(child)

        return self.register(schema)

    def add_child(self, schema_namespace, schema_name, options={}):
        return self.modify(self.get(schema_namespace), schema_name, options)


    def modify(self, source, schema_name, options={}):
        #clone because we modifying source children list
        schema = source.clone()
        schema.schema_name = schema_name
        schema.schema_namespace = source.schema_namespace

        if "remove" in options:
            removed_names = options["remove"]
            children = schema.children
            for i in xrange(len(children) - 1, -1, -1):
                if children[i].name in removed_names:
                    del children[i]

        if "alter" in options:
            altered_children = options["alter"]
            children = schema.children
            for i in xrange(len(children) - 1, -1, -1):
                if children[i].name in altered_children:
                    #clone because we change child name, and it can be used elsewhere
                    child = altered_children[children[i].name]
                    child = child.clone()
                    child.name = children[i].name
                    children[i] = child

        if "add" in options:
            added_children = options["add"]
            for key, child in added_children.items():
                #clone because we change child name, and it can be used elsewhere
                child = child.clone()
                child.name = key
                schema.add(child)

        return self.register(schema)

def anonymous_mapping(nodes):
    schema = colander.SchemaNode(colander.Mapping())
    for key, child in sorted(nodes.items(), key=lambda (k,v):  v._order):
        child = child.clone()
        child.name = key
        schema.add(child)
    return schema

def anonymous_sequence(child):
    schema = colander.SchemaNode(colander.Sequence())
    child = child.clone()
    child.name = "child"
    schema.add(child)
    return schema
