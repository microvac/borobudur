import borobudur
from borobudur.model import Model, Collection, ModelRefNode, CollectionRefNode
from prambanan import JS
from pramjs import underscore

__author__ = 'h'

methodMap = {
    'create': 'POST',
    'update': 'PUT',
    'delete': 'DELETE',
    'read':   'GET'
};

def fetch_from_cache(model_type, id, model_caches):
    model_cache = model_caches[model_type.model_url]
    if not model_cache:
        return None
    result = model_cache[id]
    if result:
        return result
    else:
        return None

def save_to_cache(model_type, attrs, model_caches):
    model_cache = model_caches[model_type.model_url]
    if not model_cache:
        model_cache = {}
        model_caches[model_type.model_url] = model_cache
    id = attrs[model_type.id_attribute]
    model_cache[id] = attrs

def fetch_children(model_type, attrs, resourcer, success):
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
                    fetch_child(child_type, child_id, resourcer, make_model_success(child_schema.name))
                else:
                    fetch_count += 1
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
                        fetch_count += 1
                        fetch_child(child_type, child_id, resourcer, make_col_success(i, child_arr))
                    else:
                        fetch_count += 1
                        fetch_children(child_type, child_value, resourcer, item_success)

    started = True
    if fetch_count == 0:
        success()

def fetch_child(model_type, id, resourcer, success):
    cache = fetch_from_cache(model_type, id, resourcer.model_caches)
    if cache is not None:
        return success(cache)

    def fetch_success(attrs):
        def _success():
            save_to_cache(model_type, attrs, resourcer.model_caches)
            success(attrs)
        fetch_children(model_type, attrs, resourcer, _success)

    params = {"type": "GET", "dataType": 'json'};
    params.url = model_type.with_id(id).url(resourcer.resources_root)
    params.success = fetch_success
    return JS("$.ajax(params)")

def client_sync (method, model, resourcer, success=None, error=None):

    def fetch_success(attrs):
        if isinstance(model, Model):
            def _success():
                if success :
                    success(attrs)
            fetch_children(model.__class__, attrs, resourcer, _success)
        else:
            count = 0
            def col_success():
                global count
                count += 1
                if count == len(attrs) and success:
                    success(attrs)
            for item_attrs in attrs:
                fetch_children(model.model, item_attrs, resourcer, col_success)
            if len(attrs) == 0 and success:
                success(attrs)

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
        params.data = JS("JSON.stringify(model.toJSON())");

    # Don't process data on a non-GET request.
    if params.type != 'GET':
        params.processData = False;

    # Make the request, allowing the user to override any Ajax options.
    return JS("$.ajax(_.extend(params, options))")

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
        elif isinstance(model, Collection):
            model_type = model.model
            storage = self.request.resources.get_storage(model_type)
            storage.all(model)
        else:
            raise ValueError("unsupported model")
        if success is not None:
            success()

    fetch = server_fetch if borobudur.is_server else client_fetch

    def dump(self):
        return {}

    def load(self, serialized):
        pass

class ResourcerFactory(object):

    def __init__(self, resources_name, resources_root):
        self.resources_name = resources_name
        self.resources_root = resources_root

    def __call__(self, request, app):
        request.context.resources_name = self.resources_name
        return Resourcer(request, self.resources_name, self.resources_root)
