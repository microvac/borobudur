from bson.objectid import ObjectId
import colander
import borobudur.jslib.backbone as backbone
from borobudur.schema import clone_node

class RefNode(colander.SchemaNode):
    pass

class Model(backbone.Model):
    """
    """

    contains_file = False

    id_attribute = "_id"
    id_type = ObjectId

    schemas = {}
    storage_url = None

    has_json_body = False

    def __init__(self, attributes=None, storage_root=None, schema_name=None, parent=None):
        self.schema_name = schema_name
        self.storage_root = storage_root
        if schema_name is not None:
            self.schema = self.__class__.get_schema(schema_name)
        else:
            self.schema = None

        self.parent = parent
        self.idAttribute = self.id_attribute

        super(Model, self).__init__(attributes)

    @classmethod
    def get_schema(cls, schema_name=""):
        return cls.schemas[schema_name]

    def url(self):
        id = None if self.isNew() else self.id
        current = self.parent
        while current is not None:
            if id is not None:
                id = "%s/%s" % (id, current.id)
            else:
                id = current

        result = "%s/%s" % (self.storage_root, self.storage_url)
        if id is not None:
            result = "%s/%s" % (result, id)
        if self.has_json_body and self.schema_name is not None:
            result += "?s="+self.schema_name
        return result

    def validate(self, attributes):
        if self.schema is None:
            return None

        try:
            self.schema.deserialize(attributes)
        except colander.Invalid as e:
            return e
        return None

    def set(self, attrs, silent=False):
        """
        Performs model creation if child attribute schema are colander.Mapping or colander.Sequence
        """

        copy = {}

        for key in iter(attrs):
            child = attrs[key]

            if self.schema is not None and key in self.schema:
                child_schema = self.schema[key]
                child = child_schema.deserialize(child)
                if isinstance(child_schema, RefNode):
                    child = child_schema.create_target(child)
            copy[key] = child

        return super(Model, self).set(copy, {"silent":silent})

    def toJSON(self):
        """
        overrides with deep toJSON
        ie. if a child is a borobudur.Model, convert that thing to JSON too
        """

        result =  super(Model, self).toJSON()
        for key in iter(result):
            value = result[key]
            if isinstance(value, Model) or isinstance(value, Collection):
                result[key] = value.toJSON()
        return result

    def fetch(self, options=None):
        data  = {}
        if self.schema_name is not None:
            data["s"] = self.schema_name
        if options is None:
            options = {}
        options["data"] = data
        super(Model, self).fetch(options)

    def save(self, options=None):
        #todo hack
        self.has_json_body = True
        super(Model, self).save(options)
        self.has_json_body = False

    """

        if self.storage is None:
            raise RuntimeError("cannot destroy without storage")

        if self.is_new():
            raise RuntimeError("model is not saved cannot delete")

        self.storage.delete(self.id)
    """

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, value):
        attrs = {}
        attrs[name] = value
        self.set(attrs)

    def __delitem__(self, key):
        raise NotImplementedError()

    # Methods converted to python underscore-separated style
    def is_new(self): return self.isNew()
    def is_valid(self):return self.isValid()
    def as_dict(self):return self.toJSON()
    def has_changed(self, attr=None):return self.hasChanged(attr)
    def changed_attributes(self, diff=None):return self.changedAttributes(diff)

class Collection(backbone.Collection):

    def __init__(self, models=None, model=Model, schema_name=None):
        options = {"model": model}
        self.schema_name = schema_name
        super(Collection, self).__init__(models, options)

    def create(self):
        return self.model(schema_name=self.schema_name)


    def __iter__(self):
        return self.models

    def _prepareModel(self, model, options=None):
        if type(model) != self.model:
            return self.model(model, schema_name=self.schema_name)
        else:
            return model


class ModelRefNode(RefNode):
    """
    prambanan:type target c(object)
    """

    def __init__(self, target, schema_name="", **kwargs):
        super(ModelRefNode, self).__init__(colander.Mapping(), **kwargs)
        self.target = target
        self.schema_name = schema_name

        node = target.get_schema(schema_name)
        for child in node.children:
            self.children.append(child)

    def create_target(self, attributes):
        if attributes is None:
            return None
        return self.target(attributes, self.schema_name)

    def clone(self):
        cloned = self.__class__(self.target, self.schema_name)
        clone_node(self, cloned)
        return cloned


class CollectionRefNode(RefNode):

    def __init__(self, target, schema_name="", **kwargs):
        super(CollectionRefNode, self).__init__(colander.Sequence(), **kwargs)

        self.target = target
        self.schema_name = schema_name

        child = ModelRefNode(target, schema_name)
        child.name = "child"
        self.add(child)

    def create_target(self, attributes):
        if attributes is None:
            return None
        return Collection(attributes, model=self.target, schema_name = self.schema_name)

    def clone(self):
        cloned = self.__class__(self.target, self.schema_name)
        clone_node(self, cloned)
        return cloned

