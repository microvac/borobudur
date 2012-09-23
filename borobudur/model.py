import bson.objectid
from bson.objectid import ObjectId
import colander
import pramjs.backbone as backbone
import pramjs.underscore as underscore
from borobudur.form.widget import Widget
from borobudur.schema import clone_node, MappingNode
from prambanan import get_template, JS

class RefNode(colander.SchemaNode):
    pass

def get_sync_options(options, app, success, error):
    if options is None:
        options = {}
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

def fetch_from_cache(model_type, id, app):
    model_cache = app.model_caches[model_type.model_url]
    if not model_cache:
        return None
    result = model_cache[id]
    if result:
        return result
    else:
        return None

def save_to_cache(model_type, attrs, app):
    model_cache = app.model_caches[model_type.model_url]
    if not model_cache:
        model_cache = {}
        app.model_caches[model_type.model_url] = model_cache
    id = attrs[model_type.id_attribute]
    model_cache[id] = attrs

def fetch_children(model_type, attrs, app, success):
    fetch_count = 0

    started = False

    def item_success():
        global fetch_count
        fetch_count -= 1
        if fetch_count == 0 and started:
            success()

    for child_schema in model_type.schema.children:
        if isinstance(child_schema, ModelRefNode):
            child_value = attrs[child_schema.name]
            child_type = child_schema.typ.target

            if child_value is not None:
                if not isinstance(child_value, dict):
                    def make_model_success(current_name):
                        def child_success(child_attrs):
                            attrs[current_name] = child_attrs
                            item_success()
                        return child_success

                    child_id = child_value
                    fetch_count += 1
                    fetch_child(child_type, child_id, app, make_model_success(child_schema.name))
                else:
                    fetch_count += 1
                    fetch_children(child_type, child_value, app, item_success)

        if isinstance(child_schema, CollectionRefNode):
            child_arr = attrs[child_schema.name]
            child_type = child_schema.children[0].typ.target

            if child_arr is None:
                continue

            for i in range(len(child_arr)):
                child_value = child_arr[i]
                if child_value is not None :
                    if not isinstance(child_value, dict):
                        child_id = child_value
                        def make_col_success(current_i, current_arr):
                            def child_success(child_attrs):
                                current_arr[current_i] = child_attrs
                                item_success()
                            return child_success
                        fetch_count += 1
                        fetch_child(child_type, child_id, app, make_col_success(i, child_arr))
                    else:
                        fetch_count += 1
                        fetch_children(child_type, child_value, app, item_success)

    started = True
    if fetch_count == 0:
        success()

def fetch_child(model_type, id, app, success):
    cache = fetch_from_cache(model_type, id, app)
    if cache is not None:
        return success(cache)

    def fetch_success(attrs):
        def _success():
            save_to_cache(model_type, attrs, app)
            success(attrs)
        fetch_children(model_type, attrs, app, _success)

    params = {"type": "GET", "dataType": 'json'};
    params.url = model_type.with_id(id).url(app)
    params.success = fetch_success
    return JS("$.ajax(params)")


def borobudur_sync (method, model, options=None):
    app = options["app"]

    prev_success = options.success

    def fetch_success(attrs):
        if isinstance(model, Model):
            def _success():
                prev_success(attrs)
            fetch_children(model.__class__, attrs, app, _success)
        else:
            count = 0
            def col_success():
                global count
                count += 1
                if count == len(attrs):
                    prev_success(attrs)
            for item_attrs in attrs:
                fetch_children(model.model, item_attrs, app, col_success)
            if len(attrs) == 0:
                prev_success(attrs)

    options.success = fetch_success

    type = methodMap[method];
    params = {"type": type, "dataType": 'json'};

    url = model.url(options["app"])
    query = {}
    if options.query:
        query = underscore.extend(options.query)
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

    schema = MappingNode()
    model_url = None

    sync = borobudur_sync

    def __init__(self, attributes=None, parent=None):
        self.parent = parent
        self.idAttribute = self.id_attribute

        super(Model, self).__init__(attributes)

    @classmethod
    def with_id(cls, id, parent=None):
        attrs = {}
        attrs[cls.id_attribute] = id
        result = cls(attrs, parent)
        return result

    def url(self, app):
        id = None if self.isNew() else self.id
        current = self.parent
        while current is not None:
            if id is not None:
                id = "%s/%s" % (current.id, id)
            else:
                id = current.id
            current = current.parent

        result = "%s/%s" % (app.settings["storage_root"], self.model_url)
        if id is not None:
            result = "%s/%s" % (result, id)
        return result

    def set(self, attrs, silent=False):
        copy = {}

        for key in iter(attrs):
            child = attrs[key]
            if key in self.attributes:
                current_child = self[key]
            else:
                current_child = None

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

        if schema is not None:
            result = {}
            for child in schema.children:
                value = self.get(child.name, None)
                result[child.name]=child.serialize(value)
            return result
        else:
            return super(Model, self).toJSON()

    def parse(self, response):
        results = {}
        for key in response:
            child = response[key]
            if child is not None and child != "":
                if key in self.schema:
                    child_schema = self.schema[key]
                    child = child_schema.deserialize(child)
                results[key] = child
        return results


    def fetch(self, app, success=None, error=None, options=None):
        options = get_sync_options(options, app, success, error)
        super(Model, self).fetch(options)

    def save(self, app, attributes, success=None, error=None, options=None):
        options = get_sync_options(options, app, success, error)
        super(Model, self).save(attributes, options)

    @staticmethod
    def serialize_queries(queries):
        return {}

    @staticmethod
    def deserialize_queries(params):
        return {}

    def __getitem__(self, name):
        return self.get(name)

    def __contains__(self, key):
        return self.attributes.__contains__(key)

    def __setitem__(self, name, value):
        attrs = {}
        attrs[name] = value
        self.set(attrs)

    def __delitem__(self, key):
        raise NotImplementedError()

    def clone(self):
        return self.__class__(self.attributes, self.parent)

    def asdict(self): return self.toJSON(self)

    # Methods converted to python underscore-separated style
    def is_new(self): return self.isNew()
    def is_valid(self):return self.isValid()

    def has_changed(self, attr=None):return self.hasChanged(attr)
    def changed_attributes(self, diff=None):return self.changedAttributes(diff)

class Collection(backbone.Collection):

    sync = borobudur_sync

    def __init__(self, model=Model, models=None):
        if models is None:
            models = []

        self.query = {}

        options = {"model": model}
        super(Collection, self).__init__(models, options)

    def url(self, app):
        return "%s/%s" % (app.settings["storage_root"], self.model.model_url)

    def create(self, app, model, success=None, error=None, options=None):
        model = self._prepareModel(model, options)
        self.add(model, options);
        def wrapped_success(next_model, resp):
            if success is not None:
                success(next_model, resp)
            else:
                next_model.trigger('sync', model, resp, options)
        model.save(app, wrapped_success, error, options)

    def fetch(self, app, success=None, error=None, options=None):
        options = get_sync_options(options, app, success, error)
        options["query"] = self.query
        super(Collection, self).fetch(options)

    def _prepareModel(self, model, options=None):
        if type(model) != self.model:
            return self.model(model)
        else:
            return model

    def __iter__(self):
        return self.models

    def __len__(self):
        return self.length

    def parse(self, response):
        results = []
        parser = self.model()
        for obj in response:
            results.append(parser.parse(obj))
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

class ModelRef(object):
    """
    prambanan:type target c(object)
    """


    def __init__(self, target, nullable=False, is_ref=True):
        self.target = target
        self.is_ref = is_ref
        self.nullable = nullable

    def serialize(self, node, appstruct):
        if appstruct is None:
            if self.nullable:
                return None
            else:
                return self.target().toJSON()

        if self.is_ref:
            return str(appstruct.id)
        else:
            return appstruct.toJSON()

    def deserialize(self, node, cstruct=colander.null):
        if self.nullable and cstruct is None:
            return None

        if isinstance(cstruct, dict):
            result = self.target()
            result.set(result.parse(cstruct))
            return result
        else:
            id = self.target.id_type(cstruct)
            return self.target.with_id(id)

class ModelRefNode(RefNode):
    def __init__(self, target, nullable=False, is_ref=True, **kwargs):
        if not target:
            print "ea"
        super(ModelRefNode, self).__init__(ModelRef(target, nullable, is_ref), **kwargs)

        if self.widget is None:
            self.widget = ModelRefWidget()

        node = target.schema
        for child in node.children:
            self.children.append(child)


    def clone(self):
        cloned = self.__class__(self.typ.target, self.typ.nullable, self.typ.is_ref)
        clone_node(self, cloned)
        return cloned


class ModelRefWidget(Widget):
    template = get_template('zpt', ('borobudur', 'form/templates/model_ref.pt'))
    hidden = True

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (colander.null, None):
            cstruct = colander.null
        return field.renderer(self.template, field, cstruct=cstruct)

    def deserialize(self, field, pstruct):
        return self.deserialize_pstruct(pstruct, field.schema)

    def deserialize_pstruct(self, pstruct, schema):
        typ = type(schema.typ)
        if typ == colander.Mapping:
            if pstruct == "":
                return colander.null
            for key in pstruct:
                pstruct[key] = self.deserialize_pstruct(pstruct[key], schema[key])
            return pstruct
        if typ == colander.Sequence:
            if pstruct == "":
                return colander.null
            for i in range(len(pstruct)):
                pstruct[i] = self.deserialize_pstruct(pstruct[i], schema.children[0])

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

class CollectionRef(colander.Sequence):

    def __init__(self, target):
        super(CollectionRef, self).__init__()

        self.target = target
        self.nullable = True

    def deserialize(self, node, cstruct=colander.null):
        appstruct = super(CollectionRef, self).deserialize(node, cstruct)
        return Collection(self.target, appstruct)

    def serialize(self, node, appstruct=colander.null):
        if appstruct is None:
            return None

        if isinstance(appstruct, Collection):
            appstruct = appstruct.models

        return super(CollectionRef, self).serialize(node, appstruct)

class CollectionRefNode(RefNode):

    def __init__(self, target, is_ref=True, **kwargs):
        super(CollectionRefNode, self).__init__(CollectionRef(target), **kwargs)

        if self.widget is None:
            self.widget = CollectionRefWidget()
        child = ModelRefNode(target, is_ref=is_ref)
        child.name = "child"
        self.child = child
        self.add(child)

    def clone(self):
        cloned = self.__class__(self.typ.target)
        clone_node(self, cloned)
        return cloned

class CollectionRefWidget(ModelRefWidget):

    def deserialize(self, field, pstruct):
        return self.deserialize_pstruct(pstruct, field.schema)

    def to_pstruct(self, name, cstruct):
        if cstruct is None:
            cstruct = []
        return super(CollectionRefWidget, self).to_pstruct(name, cstruct)

