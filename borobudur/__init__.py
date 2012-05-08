import jslib.backbone
import colander

class Model(jslib.backbone.Model):
    """
    """
    schema = None
    storage = None

    def __init__(self, attributes=None, options=None):
        if options is not None and "schema" in options:
            self.schema = options["schema"]

        if options is not None and "storage" in options:
            self.storage = options["storage"]

        super(Model, self).__init__(attributes, options)


    def validate(self, attributes):
        try:
            self.schema.deserialize(attributes)
        except colander.Invalid as e:
            return e
        return None

    def set(self, attrs, options=None):
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

        super(Model, self).set(copy, options)

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

    def fetch(self, options=None):
        if self.storage is None:
            raise RuntimeError("cannot fetch without storage")

        if self.id is None:
            raise RuntimeError("cannot fetch without id")

        self.set(self.storage.get(self.id. self.schema))

    def save(self, value=None, options=None):
        if self.storage is None:
            raise RuntimeError("cannot save without storage")

        if self.is_new():
            self.storage.insert(self.to_appstruct(), self.schema)
        else:
            self.storage.update(self.to_appstruct(), self.schema)

    def destroy(self, options=None):
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



