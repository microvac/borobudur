import borobudur
from borobudur.model import Model, Collection, ModelRefNode, CollectionRefNode
import prambanan
from pramjs import underscore
import pramjs.socketio as socketio

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

def client_sync (method, model, resourcer, query, success=None, error=None):

    def fetch_success(attrs):
        def _success():
            if success :
                success(attrs)
        if isinstance(model, Model):
            resourcer.fill_children(model.__class__, attrs, _success)
        else:
            resourcer.fill_col_children(model.model, attrs, _success)

    def fetch_error(xhr):
        if xhr.status == 400 or xhr.status == 404:
            ex = None
            er_json = prambanan.window.JSON.parse(xhr.responseText)
            if xhr.status == 400:
                ex = borobudur.InvalidRequestException(er_json.message)
            elif xhr.status == 404:
                ex = borobudur.NotFoundException()
            error(ex)
        else:
            print "error fetch"
            print xhr

    options = {}
    options.success = fetch_success
    options.error = fetch_error

    type = methodMap[method];
    params = {"type": type, "dataType": 'json'};

    url = model.url(resourcer.resources_root)
    if query:
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
        try:
            result = method(*args)
            if hasattr(result, "toJSON"):
                self.on_success(result.toJSON())
            else:
                self.on_success(result)
        except borobudur.ResourceException as e:
            self.on_error(e)

    invoke = server_invoke if borobudur.is_server else client_invoke

class Resourcer(object):

    def __init__(self, request=None, resources_name=None, resources_root=None):
        self.request = request
        self.resources_name = resources_name
        self.resources_root = resources_root
        self.model_caches = {}
        self.model_subscriptions = {}

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
        query = None
        if isinstance(model, Collection):
            query = model.query
        return client_sync("read", model, self, query, wrapped_success, error)

    def server_fetch(self, model, success=None, error=None):
        try:
            if isinstance(model, Model):
                model_type = model.__class__
                storage = self.request.resources.get_storage(model_type)
                storage.one(model)
                attrs = model.toJSON()
                def _success():
                    model.set(model.parse(attrs))
                    success()
                self.fill_children(model_type, attrs, _success)
            elif isinstance(model, Collection):
                model_type = model.model
                storage = self.request.resources.get_storage(model_type)
                #todo queries
                storage.all(model, model_type.deserialize_queries(model.query))
                attrs = model.toJSON()
                count = Counter(0)
                def col_success():
                    count.i += 1
                    if count.i == len(attrs) and success:
                        success()
                for item_attrs in attrs:
                    self.fill_children(model.model, item_attrs, col_success)
            else:
                raise ValueError("unsupported model")
        except borobudur.ResourceException as e:
            error(e)

    fetch = server_fetch if borobudur.is_server else client_fetch

    def save(self, model, success=None, error=None):
        method = "create" if model.is_new() else "update"
        def wrapped_success(resp, status, xhr):
            if not model.set(model.parse(resp, xhr)):
                return False;
            if success:
                success(model, resp);
        return client_sync(method, model, self, None, wrapped_success, error)

    def service(self, id, attr, success=None, error=None):
        return ServiceInvoker(self, id, attr, success, error)

    def fetch_from_cache(self, model_type, id):
        if model_type.model_url not in self.model_caches:
            return None

        model_cache = self.model_caches[model_type.model_url]
        if id not in model_cache:
            return None

        return model_cache[id]

    def save_to_cache(self, model_type, attrs):
        if model_type.model_url not in self.model_caches:
            self.model_caches[model_type.model_url] = {}
        model_cache = self.model_caches[model_type.model_url]
        id = attrs[model_type.id_attribute]
        model_cache[id] = attrs

    def client_bare_fetch(self, model_type, id, success):
        params = {"type": "GET", "dataType": 'json'};
        params.url = model_type.with_id(model_type.id_type(id)).url(self.resources_root)
        params.success = success
        return prambanan.JS("$.ajax(params)")

    def server_bare_fetch(self, model_type, id, success):
        model = model_type.with_id(model_type.id_type(id))
        self.request.resources.get_storage(model_type).one(model)
        success(model.toJSON())

    def bare_fetch(self, model_type, id, success):
        cache = self.fetch_from_cache(model_type, id)
        if cache is not None:
            return success(cache)

        def fetch_success(attrs):
            def _success():
                self.save_to_cache(model_type, attrs)
                success(attrs)
            self.fill_children(model_type, attrs, _success)

        if borobudur.is_server:
            self.server_bare_fetch(model_type, id, fetch_success)
        else:
            self.client_bare_fetch(model_type, id, fetch_success)


    def fill_children(self, model_type, attrs, success):
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
                        self.bare_fetch(child_type, child_id, make_model_success(child_schema.name))
                    else:
                        fetch_count.i += 1
                        self.fill_children(child_type, child_value, item_success)

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
                            self.bare_fetch(child_type, child_id, make_col_success(i, child_arr))
                        else:
                            fetch_count.i += 1
                            self.fill_children(child_type, child_value, item_success)

        started = True
        if fetch_count.i == 0:
            success()

    def fill_col_children(self, model_type, attrs, success):
        count = Counter(0)
        def col_success():
            global count
            count.i += 1
            if count.i == len(attrs) and success:
                success()
        for item_attrs in attrs:
            self.fill_children(model_type, item_attrs, col_success)
        if len(attrs) == 0 and success:
            success()

    def subscribe(self, model):
        url = model.single_url()

        if url not in self.model_subscriptions:
            self.model_subscriptions[url] = [[], 0, model.__class__]

        models, count, typ = self.model_subscriptions[url]

        models.append(model)
        self.model_subscriptions[1] = count + 1

        if count == 0:
            self.socket.emit("subscribe_model", url)

    def unsubscribe(self, model):
        url = model.single_url()
        if url in self.model_subscriptions:
            models, count, typ = self.model_subscriptions[url]

            for i, m in enumerate(models):
                if m == model:
                    models[i] = None
                    count -= 1

            self.model_subscriptions[1] = count
            if count <= 0:
                self.socket.emit("unsubscribe_model", url)

    def on_new_request(self):
        self.model_caches = {}

    def on_model_change(self, url, data):
        models, count, typ = self.model_subscriptions[url]
        def on_success():
            for model in models:
                if model is not None:
                    model.set(model.parse(data))
        self.fill_children(typ, data, on_success)

    def on_socket_connected(self):
        print "connected"
        for key in self.model_subscriptions:
            models, count, typ = self.model_subscriptions[key]
            if count > 0:
                self.socket.emit("subscribe_model", key)

    def on_socket_disconnected(self):
        print "disconnect"

    def serialize(self):
        results = {}
        results["resources_root"] = self.resources_root
        results["model_caches"] = self.model_caches
        return results

    def deserialize(self, serialized):
        self.resources_root = serialized["resources_root"]
        self.model_caches = serialized["model_caches"]
        self.socket = socketio.connect("/model")
        self.socket.on('model_change', underscore.bind(self.on_model_change, self))
        self.socket.on('connect', underscore.bind(self.on_socket_connected, self))
        self.socket.on('disconnect', underscore.bind(self.on_socket_disconnected, self))


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
            model_type = prambanan.load_qname(qname)
            def _success(attrs):
                pass
            if is_collection:
                model = Collection(model_type)
                self.app.resourcer.fill_col_children(model_type, attrs,  _success)
                model.reset(model.parse(attrs))
            else:
                model = prambanan.ctor(model_type)()
                self.app.resourcer.fill_children(model_type, attrs, _success)
                model.set(model.parse(attrs))
            self.models[cid] = model

    def serialize(self):
        results = {}
        for cid in self.models:
            model = self.models[cid]
            is_collection = isinstance(model, Collection)
            if is_collection:
                qname = prambanan.to_qname(model.model)
            else:
                qname = prambanan.to_qname(model.__class__)
            attrs = model.toJSON()
            results[cid] = (is_collection, qname, attrs)
        return results
