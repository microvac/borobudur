import borobudur
from borobudur.model import Model, Collection, ModelRefNode, CollectionRefNode
import prambanan
from pramjs import underscore

__author__ = 'h'

methodMap = {
    'create': 'POST',
    'update': 'PUT',
    'delete': 'DELETE',
    'read':   'GET'
};

class Counter(object):

    def __init__(self, i):
        self.i = i

def fetch_from_cache(model_type, id, model_caches):
    if model_type.model_url not in model_caches:
        return None

    model_cache = model_caches[model_type.model_url]
    if id not in model_cache:
        return None

    return model_cache[id]

def save_to_cache(model_type, attrs, model_caches):
    if model_type.model_url not in model_caches:
        model_caches[model_type.model_url] = {}
    model_cache = model_caches[model_type.model_url]
    id = attrs[model_type.id_attribute]
    model_cache[id] = attrs

def fetch_children(model_type, attrs, resourcer, success):
    fetch_count = Counter(0)

    started = False

    def item_success():
        fetch_count.i -= 1
        if fetch_count.i == 0 and started:
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
                    fetch_count.i += 1
                    fetch_child(child_type, child_id, resourcer, make_model_success(child_schema.name))
                else:
                    fetch_count.i += 1
                    fetch_children(child_type, child_value, resourcer, item_success)

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
                        fetch_count.i += 1
                        fetch_child(child_type, child_id, resourcer, make_col_success(i, child_arr))
                    else:
                        fetch_count.i += 1
                        fetch_children(child_type, child_value, resourcer, item_success)

    started = True
    if fetch_count.i == 0:
        success()

def fetch_col_children(model_type, attrs, resourcer, success):
    count = Counter(0)
    def col_success():
        global count
        count.i += 1
        if count.i == len(attrs) and success:
            success()
    for item_attrs in attrs:
        fetch_children(model_type, item_attrs, resourcer, col_success)
    if len(attrs) == 0 and success:
        success()

def client_fetch(model_type, id, resourcer, success):
    params = {"type": "GET", "dataType": 'json'};
    params.url = model_type.with_id(model_type.id_type(id)).url(resourcer.resources_root)
    params.success = success
    return prambanan.JS("$.ajax(params)")

def server_fetch(model_type, id, resourcer, success):
    model = model_type.with_id(model_type.id_type(id))
    resourcer.request.resources.get_storage(model_type).one(model)
    success(model.toJSON())

def fetch_child(model_type, id, resourcer, success):
    cache = fetch_from_cache(model_type, id, resourcer.model_caches)
    if cache is not None:
        return success(cache)

    def fetch_success(attrs):
        def _success():
            save_to_cache(model_type, attrs, resourcer.model_caches)
            success(attrs)
        fetch_children(model_type, attrs, resourcer, _success)

    if borobudur.is_server:
        return server_fetch(model_type, id, resourcer, fetch_success)
    else:
        return client_fetch(model_type, id, resourcer, fetch_success)

def client_sync (method, model, resourcer, success=None, error=None):

    def fetch_success(attrs):
        def _success():
            if success :
                success(attrs)
        if isinstance(model, Model):
            fetch_children(model.__class__, attrs, resourcer, _success)
        else:
            fetch_col_children(model.model, attrs, resourcer, _success)

    options = {}
    options.success = fetch_success

    type = methodMap[method];
    params = {"type": type, "dataType": 'json'};

    url = model.url(resourcer.resources_root)
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
        params.data = prambanan.JS("JSON.stringify(model.toJSON())");

    # Don't process data on a non-GET request.
    if params.type != 'GET':
        params.processData = False;

    # Make the request, allowing the user to override any Ajax options.
    return prambanan.JS("$.ajax(_.extend(params, options))")


class ServiceInvoker(object):

    def __init__(self, resourcer, service_id, service_attr, on_success, on_error):
        self.resourcer = resourcer
        self.service_id = service_id
        self.service_attr = service_attr
        self.on_success = on_success
        self.on_error = on_error

    def client_invoke(self, *args):
        json = prambanan.window.JSON
        url = "%s/services/%s/%s" % (self.resourcer.resources_root, self.service_id, self.service_attr)
        settings = {
            "data": json.stringify(args),
            "type": "POST",
            "contentType": "application/json; charset=utf-8",
            "dataType": "json",
            "success": self.on_success,
            "error": self.on_error,
            "url": url,
            }
        borobudur.query_el.ajax(settings)

    def server_invoke(self, *args):
        service = self.resourcer.request.resources.get_service(self.service_id)
        method = getattr(service, self.service_attr)
        result = method(*args)
        if hasattr(result, "toJSON"):
            self.on_success(result.toJSON())
        else:
            self.on_success(result)

    invoke = server_invoke if borobudur.is_server else client_invoke

class Resourcer(object):

    def __init__(self, request=None, resources_name=None, resources_root=None):
        self.request = request
        self.resources_name = resources_name
        self.resources_root = resources_root
        self.model_caches = {}

    def client_fetch(self, model, success=None, error=None):
        def wrapped_success(resp, status, xhr):
            if isinstance(model, Model):
                if not model.set(model.parse(resp, xhr)):
                    return False;
            elif isinstance(model, Collection):
                model.reset(model.parse(resp, xhr))
            else:
                raise ValueError("unsupported model")
            if success:
                success(model, resp);
        return client_sync("read", model, self, wrapped_success, error)

    def server_fetch(self, model, success=None, error=None):
        if isinstance(model, Model):
            model_type = model.__class__
            storage = self.request.resources.get_storage(model_type)
            storage.one(model)
            attrs = model.toJSON()
            def _success():
                model.set(model.parse(attrs))
                success()
            fetch_children(model_type, attrs, self,_success)
        elif isinstance(model, Collection):
            model_type = model.model
            storage = self.request.resources.get_storage(model_type)
            #todo queries
            storage.all(model, model_type.deserialize_queries({}))
            attrs = model.toJSON()
            count = Counter(0)
            def col_success():
                count.i += 1
                if count.i == len(attrs) and success:
                    success()
            for item_attrs in attrs:
                fetch_children(model.model, item_attrs, self, col_success)
        else:
            raise ValueError("unsupported model")

    fetch = server_fetch if borobudur.is_server else client_fetch

    def save(self, model, success=None, error=None):
        method = "create" if model.is_new() else "update"
        def wrapped_success(resp, status, xhr):
            if not model.set(model.parse(resp, xhr)):
                return False;
            if success:
                success(model, resp);
        return client_sync(method, model, self, wrapped_success, error)

    def service(self, id, attr, success=None, error=None):
        return ServiceInvoker(self, id, attr, success, error)

    def on_new_request(self):
        self.model_caches = {}

    def serialize(self):
        results = {}
        results["resources_root"] = self.resources_root
        results["model_caches"] = self.model_caches
        return results

    def deserialize(self, serialized):
        self.resources_root = serialized["resources_root"]
        self.model_caches = serialized["model_caches"]

class ResourcerProperty(object):

    def __init__(self, resources_name, resources_root):
        self.resources_name = resources_name
        self.resources_root = resources_root

    def __call__(self, request, app):
        request.context.resources_name = self.resources_name
        return Resourcer(request, self.resources_name, self.resources_root)


class ModelDumper(object):

    def __init__(self, app, resourcer):
        self.app = app
        self.resourcer = resourcer
        self.models = {}

    def dump(self, model):
        if model is None:
            return None

        if model.cid is None:
            model.cid = self.app.next_count()
        if model.cid not in self.models:
            self.models[model.cid] = model
        return model.cid

    def load(self, cid):
        if cid is None:
            return None

        return self.models[cid]

    def deserialize(self, serialized):
        self.models = {}
        for cid in serialized:
            is_collection, qname, attrs = serialized[cid]
            model_type = prambanan.load_module_attr(qname)
            def _success(attrs):
                pass
            if is_collection:
                model = Collection(model_type)
                fetch_col_children(model_type, attrs, self.app.resourcer, _success)
                model.reset(model.parse(attrs))
            else:
                model = prambanan.JS("new model_type()")
                fetch_children(model_type, attrs, self.app.resourcer, _success)
                model.set(model.parse(attrs))
            self.models[cid] = model

    def serialize(self):
        results = {}
        for cid in self.models:
            model = self.models[cid]
            is_collection = isinstance(model, Collection)
            if is_collection:
                qname = borobudur.get_qname(model.model)
            else:
                qname = borobudur.get_qname(model.__class__)
            attrs = model.toJSON()
            results[cid] = (is_collection, qname, attrs)
        return results
