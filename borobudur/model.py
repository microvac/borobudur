import bson.objectid
from bson.objectid import ObjectId
import colander
import borobudur.jslib.backbone as backbone
import borobudur.schema as schema
from borobudur.form.widget import Widget
from borobudur.schema import clone_node
from prambanan import get_template

class RefNode(colander.SchemaNode):
    pass

class Model(backbone.Model):
    """
    """

    contains_file = False

    id_attribute = "_id"
    id_type = ObjectId

    schemas = {}
    model_url = None

    has_json_body = False

    def __init__(self, attributes=None, storage_root=None, schema_name=None, parent=None):
        self.schema_name = schema_name
        self.storage_root = storage_root

        if schema_name is not None:
            self.schema = self.__class__.get_schema(schema_name)
        else:
            self.schema = None

        self.save_schema_name = None
        self.serialize_schema = None

        self.parent = parent
        self.idAttribute = self.id_attribute

        super(Model, self).__init__(attributes)

    @classmethod
    def get_schema(cls, schema_name=""):
        return cls.schemas[schema_name]

    def url(self):
        if self.storage_root is None:
            raise ValueError("trying to get url of model with no storage root")

        id = None if self.isNew() else self.id
        current = self.parent
        while current is not None:
            if id is not None:
                id = "%s/%s" % (current.id, id)
            else:
                id = current.id
            current = current.parent

        result = "%s/%s" % (self.storage_root, self.model_url)
        if id is not None:
            result = "%s/%s" % (result, id)
        if self.has_json_body:
            schema_name = self.schema_name
            if self.save_schema_name is not None:
                schema_name = self.save_schema_name
            if schema_name is not None:
                result += "?s="+schema_name
        return result

    def validate(self, attributes):
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

                #special case for setting id on ref
                if child is not None:
                    if not isinstance(child, Model) and isinstance(child_schema, RefNode):
                        if key in self.attributes:
                            current_child = self[key]
                            if isinstance(current_child, Model):
                                if current_child.id == child:
                                    continue
                                else:
                                    raise ValueError("cannot change model attr to different id. attr %s. current %s set to %s" % (key, current_child.id, child))

                #if new and old model have the id, use the old one by setting all new attributes to it
                #this make all callbacks not lost
                if isinstance(child, Model):
                    if key in self.attributes:
                        current_child = self[key]
                        if isinstance(current_child, Model) and current_child.id == child.id:
                            current_child.set(child.attributes)
                            child = current_child


            copy[key] = child

        return super(Model, self).set(copy, {"silent":silent})

    def get(self, name, dft=None):
        if name in self.attributes:
            return self.attributes[name]
        return dft


    def toJSON(self):
        """
        overrides with deep toJSON
        ie. if a child is a borobudur.Model, convert that thing to JSON too
        """
        schema = self.schema
        if self.serialize_schema is not None:
            schema = self.serialize_schema

        if schema is not None:
            result = {}
            for child in schema.children:
                result[child.name]=child.serialize(self.get(child.name, None))
            return result
        else:
            return super(Model, self).toJSON()

    def parse(self, response):
        results = {}
        for key in response:
            child = response[key]
            if self.schema is not None and key in self.schema:
                child_schema = self.schema[key]
                child = child_schema.deserialize(child)
            results[key] = child
        return results


    def fetch(self, options=None):
        data  = {}
        if self.schema_name is not None and self.schema_name != "":
            data["s"] = self.schema_name
        if options is None:
            options = {}
        options["data"] = data
        super(Model, self).fetch(options)

    def save(self, schema_name=None, options=None):
        if schema_name is not None:
            self.serialize_schema = self.__class__.get_schema(schema_name)
        self.has_json_body = True
        self.save_schema_name = schema_name

        super(Model, self).save({}, options)

        self.has_json_body = False
        self.serialize_schema = None
        self.save_schema_name = None

    @staticmethod
    def serialize_queries(queries):
        return {}

    @staticmethod
    def deserialize_queries(params):
        return {}

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, value):
        attrs = {}
        attrs[name] = value
        self.set(attrs)

    def __delitem__(self, key):
        raise NotImplementedError()

    def clone(self):
        return self.__class__(self.attributes, self.storage_root, self.schema_name, self.parent)

    def as_dict(self, schema_name=None):
        if schema_name is not None:
            self.serialize_schema = self.__class__.get_schema(schema_name)

        result = self.toJSON()

        self.serialize_schema = None

        return result

    # Methods converted to python underscore-separated style
    def is_new(self): return self.isNew()
    def is_valid(self):return self.isValid()

    def has_changed(self, attr=None):return self.hasChanged(attr)
    def changed_attributes(self, diff=None):return self.changedAttributes(diff)

class Collection(backbone.Collection):

    def __init__(self, models=None, model=Model, storage_root=None, schema_name=None):
        options = {"model": model}
        self.schema_name = schema_name
        self.query = {}
        super(Collection, self).__init__(models, options)
        self.schema = self.model.get_schema(self.schema_name)

    def url(self):
        return "%s/%s" % (self.storage_root, self.model.model_url)

    def create(self):
        return self.model(schema_name=self.schema_name)

    def fetch(self, options=None):
        data  = {}
        if self.schema_name is not None:
            data["s"] = self.schema_name
        for key in self.query:
            data[key] = self.query[key]
        if options is None:
            options = {}
        options["data"] = data
        super(Collection, self).fetch(options)

    def _prepareModel(self, model, options=None):
        if type(model) != self.model:
            return self.model(model, schema_name=self.schema_name)
        else:
            return model

    def __iter__(self):
        return self.models

    def __len__(self):
        return self.length

    def parse(self, response):
        results = []
        for obj in response:
            attrs = {}
            for key in obj:
                child = obj[key]
                if self.schema is not None and key in self.schema:
                    child_schema = self.schema[key]
                    child = child_schema.deserialize(child)
                attrs[key] = child
            results.append(self.model(attrs, schema_name=self.schema_name))
        return results

    #If key > len(self.models) append at the end
    def __setitem__(self, key, value):
        if type(value) != type(self.model()):
            raise TypeError()
        try:
            self.models[key] = value
        except IndexError:
            options = {"at": key}
            self.add(value, options)

    def __getitem__(self, key):
        return self.at(key)

class ModelRefNode(RefNode):
    """
    prambanan:type target c(object)
    """

    def __init__(self, target, schema_name="", nullable=False, **kwargs):
        super(ModelRefNode, self).__init__(colander.Mapping(), **kwargs)
        self.target = target
        self.schema_name = schema_name
        self.nullable = nullable

        node = target.get_schema(schema_name)
        for child in node.children:
            self.children.append(child)

    def serialize(self, appstruct):
        if appstruct is None:
            if self.nullable:
                return None
            appstruct = {}

        if isinstance(appstruct, Model):
            appstruct = appstruct.attributes
        result = super(ModelRefNode, self).serialize(appstruct)

        return result

    def deserialize(self, cstruct=colander.null):
        if cstruct is None and self.nullable:
            return None

        if not isinstance(cstruct, dict):
            d = {}
            d[self.target.id_attribute] = cstruct
            cstruct = d
        appstruct = super(ModelRefNode, self).deserialize(cstruct)

        return self.target(appstruct, schema_name=self.schema_name)

    def clone(self):
        cloned = self.__class__(self.target, self.schema_name)
        clone_node(self, cloned)
        return cloned

class ModelRefWidget(Widget):
    template = get_template('zpt', ('borobudur', 'form/templates/model_ref.pt'))
    hidden = True

    def serialize(self, element, field, cstruct, readonly=False):
        if cstruct in (colander.null, None):
            cstruct = colander.null
        return field.renderer(self.template, element, field, cstruct=cstruct)

    def deserialize(self, field, pstruct):
        if not pstruct:
            return colander.null
        return pstruct

    def to_pstruct(self, name, cstruct):
        def process_dict(process, name, item):
            results = []
            results.append(["__start__", "%s:mapping" % name])
            for child in item:
                results.extend(process(child, item[child]))
            results.append(["__end__", "%s:mapping" % name])
            return results

        def process_list(process, name, item):
            results = []
            results.append(["__start__", "%s:sequence" % name])
            for child in item:
                results.extend(process("", child))
            results.append(["__end__", "%s:sequence" % name])
            return results

        def process(name, item):
            if isinstance(item, dict):
                return process_dict(process, name, item)
            elif isinstance(item, list):
                return process_list(process, name, item)
            else:
                return [[name, '' if item is None else str(item)]]

        return process(name, cstruct)


class CollectionRefNode(RefNode):

    def __init__(self, target, schema_name="", **kwargs):
        super(CollectionRefNode, self).__init__(colander.Sequence(), **kwargs)

        self.target = target
        self.schema_name = schema_name

        child = ModelRefNode(target, schema_name)
        child.name = "child"
        self.child = child
        self.add(child)

    def deserialize(self, cstruct=colander.null):
        appstruct = super(CollectionRefNode, self).deserialize(cstruct)
        return Collection(appstruct, model=self.target, schema_name = self.schema_name)

    def serialize(self, appstruct=colander.null):
        if appstruct is None:
            return None

        if isinstance(appstruct, Collection):
            appstruct = appstruct.models
        return super(CollectionRefNode, self).serialize(appstruct)

    def clone(self):
        cloned = self.__class__(self.target, self.schema_name)
        clone_node(self, cloned)
        return cloned

