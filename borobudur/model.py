import prambanan.jslib.underscore as underscore
import colander
import borobudur.jslib.backbone as backbone

class Model(backbone.Model):
    """
    """

    def __init__(self, attributes=None, schema=None, storage=None):
        self.schema = schema
        self.storage = storage

        super(Model, self).__init__(attributes)


    def validate(self, attributes):
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
            child = None

            if self.schema is not None and key in self.schema:
                child_type = self.schema[key].typ
                if isinstance(child_type, colander.Mapping) or isinstance(child_type, colander.Sequence):
                    child = self.create_child_from_schema(attrs[key], self.schema[key])
                else:
                    child = self.schema[key].deserialize(attrs[key])

            if child is None:
                child = attrs[key]

            copy[key] = child

        super(Model, self).set(copy, {"silent":silent})

    def create_child_from_schema(self, attributes, schema):
        """
        overrides this method if you want to have children automatically become a Model

        returns a borobudur.Model if child created or None if you don't do anything
        """
        return None


    def toJSON(self):
        """
        overrides with deep toJSON
        ie. if a child is a borobudur.Model, convert that thing to JSON too
        """

        result =  super(Model, self).toJSON()
        for key in iter(result):
            value = result[key]
            if isinstance(value, Model):
                result[key] = value.toJSON()
        return result

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

    # Methods converted to python underscore-separated style
    def is_new(self): return self.isNew()
    def is_valid(self):return self.isValid()
    def as_dict(self):return self.toJSON()
    def has_changed(self, attr=None):return self.hasChanged(attr)
    def changed_attributes(self, diff=None):return self.changedAttributes(diff)

class Collection(backbone.Collection):
    pass

