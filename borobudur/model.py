import bson.objectid
from bson.objectid import ObjectId
import colander
import borobudur.jslib.backbone as backbone
import borobudur.schema as schema
from borobudur.form.widget import Widget
from borobudur.schema import clone_node
from prambanan import get_template, JS
from prambanan.jslib import underscore

class RefNode(colander.SchemaNode):
    pass

def get_sync_options(options, app, schema_name, success, error):
    if options is None:
        options = {}
    options["schema_name"] = schema_name
    options["app"] = app
    options["success"] = success
    options["error"] = error
    return options

methodMap = {
    'create': 'POST',
    'update': 'PUT',
    'delete': 'DELETE',
    'read':   'GET'
};

def borobudur_sync (method, model, options=None):
    type = methodMap[method];
    params = {"type": type, "dataType": 'json'};

    url = model.url(options["app"])
    query = {}
    if options.query:
        query = underscore.extend(options.query)
    if options.schema_name != "":
        query["s"]=options.schema_name
    i = 0
    for key in query:
        url += "?" if i == 0 else "&"
        url += "%s=%s" % (key, query[key])
    params.url = url

    if not options.data and model and (method == 'create' or method == 'update'):
        params.contentType = 'application/json';
        params.data = JS("JSON.stringify(model.toJSON())");

    # Don't process data on a non-GET request.
    if params.type != 'GET':
        params.processData = False;

    # Make the request, allowing the user to override any Ajax options.
    return JS("$.ajax(_.extend(params, options))")

class Model(backbone.Model):
    """
    """

    id_attribute = "_id"
    id_type = ObjectId

    schemas = {"": schema.MappingNode()}
    model_url = None

    sync = borobudur_sync

    def __init__(self, attributes=None, schema_name="", parent=None):
        self.schema_name = schema_name

        self.schema = self.__class__.get_schema(schema_name)

        self.parent = parent
        self.idAttribute = self.id_attribute

        super(Model, self).__init__(attributes)

    @classmethod
    def get_schema(cls, schema_name=""):
        return cls.schemas[schema_name]

    def url(self, app):
        id = None if self.isNew() else self.id
        current = self.parent
        while current is not None:
            if id is not None:
                id = "%s/%s" % (current.id, id)
            else:
                id = current.id
            current = current.parent

        result = "%s/%s" % (app.storage_root, self.model_url)
        if id is not None:
            result = "%s/%s" % (result, id)
        return result

    def set(self, attrs, silent=False):
        """
        Performs model creation if child attribute schema are colander.Mapping or colander.Sequence
        """
        copy = {}

        for key in iter(attrs):
            child = attrs[key]
            if key in self.attributes:
                current_child = self[key]
            else:
                current_child = None

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
                if isinstance(child, Model) and isinstance(current_child, Model) and current_child.id == child.id:
                    current_child.set(child.attributes)
                    child = current_child
                #if new and old child is a collection, just reset that collection
                if isinstance(child, Collection) and isinstance(current_child, Collection):
                    current_child.reset(child.models)
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


    def fetch(self, app, success=None, error=None, options=None):
        options = get_sync_options(options, app, self.schema_name, success, error)
        super(Model, self).fetch(options)

    def save(self, app, success=None, error=None, options=None):
        options = get_sync_options(options, app, self.schema_name, success, error)
        super(Model, self).save({}, options)

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
        return self.__class__(self.attributes, self.schema_name, self.parent)

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

    sync = borobudur_sync

    def __init__(self, model=Model, models=None, schema_name=""):
        if models is None:
            models = []

        self.schema_name = schema_name
        self.schema = model.get_schema(self.schema_name)
        self.query = {}

        options = {"model": model}
        super(Collection, self).__init__(models, options)

    def url(self):
        if not self.storage_root:
            self.storage_root = "/app/storages"
        return "%s/%s" % (self.storage_root, self.model.model_url)

    def create(self, model, app, success=None, error=None, options=None):
        model = self._prepareModel(model, options)
        self.add(model, options);
        def wrapped_success(next_model, resp):
            if success is not None:
                success(next_model, resp)
            else:
                next_model.trigger('sync', model, resp, options)
        model.save(app, wrapped_success, error, options)

    def fetch(self, app, success=None, error=None, options=None):
        options = get_sync_options(options, app, self.schema_name, success, error)
        options["query"] = self.query
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
        if cstruct is None:
            cstruct = {}

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
        return Collection(self.target, appstruct, schema_name = self.schema_name)

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

class CollectionRefWidget(ModelRefWidget):
    def to_pstruct(self, name, cstruct):
        if cstruct is None:
            cstruct = []
        return super(CollectionRefWidget, self).to_pstruct(name, cstruct)

