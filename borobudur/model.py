from bson.objectid import ObjectId
import prambanan.jslib.underscore as underscore
import colander
import borobudur.jslib.backbone as backbone
import borobudur.schema

class Model(backbone.Model):
    """
    """
    id_attribute = "_id"
    id_type = ObjectId

    schemas = {}
    storage_url = None

    def __init__(self, attributes=None, schema_name=None, parent=None):
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
        id = self.id
        current = self.parent
        while current is not None:
            id = "%s/%s" % (id, current.id)
        return "/app/storages/%s/%s" % (self.storage_url, id)

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
                if isinstance(child_schema, borobudur.schema.RefSchema):
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

    """
    def fetch(self):
        if self.storage is None:
            raise RuntimeError("cannot fetch without storage")

        if self.id is None:
            raise RuntimeError("cannot fetch without id")

        self.set(self.storage.one(self.id. self.schema))

    def save(self, value=None):
        if self.storage is None:
            raise RuntimeError("cannot save without storage")

        obj = self.as_dict()
        if self.is_new():
            self.storage.insert(obj, self.schema)
        else:
            self.storage.update(obj, self.schema)
        self.set(obj)

    def destroy(self):
        if self.storage is None:
            raise RuntimeError("cannot destroy without storage")

        if self.is_new():
            raise RuntimeError("model is not saved cannot delete")

        self.storage.delete(self.id)
    """

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, value):
        self.set({"name":value})

    def __delitem__(self, key):
        raise NotImplementedError()

    # Methods converted to python underscore-separated style
    def is_new(self): return self.isNew()
    def is_valid(self):return self.isValid()
    def as_dict(self):return self.toJSON()
    def has_changed(self, attr=None):return self.hasChanged(attr)
    def changed_attributes(self, diff=None):return self.changedAttributes(diff)

class Collection(backbone.Collection):

    def __iter__(self):
        return self.models


