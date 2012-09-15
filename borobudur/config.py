import inspect
import os
from pyramid.response import Response, FileResponse
from pyramid.renderers import render_to_response
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from zope.interface.interface import Interface

import borobudur
from borobudur.interfaces import IAppResources
import borobudur.schema
import borobudur.storage
import borobudur.storage.mongo

from borobudur.storage import IStorageConnection
from borobudur.asset import SimplePackCalculator
from borobudur.model import Model, CollectionRefNode

from lxml import etree

class Document(object):
    def __init__(self, el):
        self.el = el
        self.el_query = borobudur.create_el_query(el)
        self.q_el = borobudur.query_el(el)

class AppState(object):
    leaf_page=None
    active_pages = []
    load_info = False

def wrap_pyramid_view(page_callback, asset_manager, calculator, entry_point):
    """
    loaded_page: id
    loaded_bundles = list of bundles
    """

    def view(request):

        def page_success(load_flow):
            asset_manager.write_all(request.document, load_flow, calculator, entry_point)

        load_callbacks = {
            "success": page_success
        }
        app_state = AppState()
        page_callback(request, app_state, load_callbacks)

        html = etree.tostring(request.document.el, pretty_print=True, method="html")

        return Response("<!DOCTYPE html>\n"+html)

    return view

def asset_list_view(asset_manager, calculate, entry_point):

    def view(request):
        page_type_id = request.matchdict["page_type_id"]

        packs = list(calculate(page_type_id, entry_point))
        styles = ["bootstrap"]

        results = {
            "css": {},
            "js": {},
        }

        for type, name, bundle in asset_manager.get_all_bundles(packs, styles):
            results[type][name] = [url for url in bundle.urls(asset_manager.env)]

        return render_to_response("json", results)

    return view

def asset_changed_view(asset_manager, calculate, entry_point):

    def view(request):
        page_type_id = request.matchdict["page_type_id"]

        import time
        packs = list(calculate(page_type_id, entry_point))
        styles = ["bootstrap"]

        results = {"js":[], "css":[]}

        found = False
        i = 0
        while not found and i < 1000:
            for type, name, bundle in asset_manager.get_all_bundles(packs, styles):
                if asset_manager.env.updater.needs_rebuild(bundle, asset_manager.env):
                    results[type].append(name)
                    found = True
                i += 0
            if not found:
                time.sleep(1)


        return render_to_response("json", results)

    return view

def make_embedded_storage_view(model, level):

    class View(object):

        def __init__(self, request):
            self.request = request
            self.schema = model.get_schema(request.params.get("s", ""))
            self.storage = request.resources.get_storage(model)

            id = None
            current_id_level = 0
            while current_id_level < level:
                id_name = "id%d" % current_id_level
                id = (self.request.matchdict[id_name], id)
                current_id_level += 1

            self.id = id

        def create(self):
            appstruct = self.schema.deserialize(self.request.json_body)
            result = self.storage.insert(self.id, appstruct, self.schema)
            serialized = self.schema.serialize(result)
            return serialized

        def read(self):
            result = self.storage.one(self.id, self.request.matchdict["id"], self.schema)
            serialized = self.schema.serialize(result)
            return serialized

        def update(self):
            appstruct = self.schema.deserialize(self.request.json_body)
            result = self.storage.update(self.id, appstruct, self.schema)
            serialized = self.schema.serialize(result)
            return serialized

        def delete(self):
            pass

        def list(self):
            skip = self.request.params.get("ps", 0)
            limit = self.request.params.get("pl", 0)
            config = borobudur.storage.SearchConfig(skip, limit)

            results = self.storage.all(self.id, config=config, schema=self.schema)
            sequence_schema = borobudur.schema.SequenceNode(self.schema)
            serialized = sequence_schema.serialize(results)
            return serialized

    return View

def make_storage_view(model):

    class View(object):

        def __init__(self, request):
            self.request = request
            self.storage = request.resources.get_storage(model)
            self.schema = model.get_schema(request.params.get("s", ""))

        def create(self):
            appstruct = self.schema.deserialize(self.request.json_body)
            result = self.storage.insert(appstruct, self.schema)
            serialized = self.schema.serialize(result)
            return serialized

        def read(self):
            result = self.storage.one(self.request.matchdict["id"], self.schema)
            serialized = self.schema.serialize(result)
            return serialized

        def update(self):
            appstruct = self.schema.deserialize(self.request.json_body)
            result = self.storage.update(appstruct, self.schema)
            serialized = self.schema.serialize(result)
            return serialized

        def delete(self):
            result = self.storage.delete(self.request.matchdict["id"])
            return result

        def list(self):
            skip = self.request.params.get("ps", 0)
            limit = self.request.params.get("pl", 0)
            sort_order = self.request.params.get("so")
            sort_criteria = self.request.params.get("sc")
            query = self.storage.model.deserialize_queries(self.request.params)
            sorts = None
            if sort_criteria and sort_order:
                sorts = borobudur.storage.SearchSort(sort_criteria, sort_order)
            elif sort_criteria:
                sorts = borobudur.storage.SearchSort(sort_criteria)

            config = borobudur.storage.SearchConfig(skip, limit, sorts)

            results = self.storage.all(query=query, schema=self.schema, config=config)
            sequence_schema = borobudur.schema.SequenceNode(self.schema)
            serialized = sequence_schema.serialize(results)
            return serialized

    return View

def make_file_storage_view(storage_type):

    model = storage_type.model

    class View(object):

        def __init__(self, request):
            self.storage = request.resources.get_storage(model)
            self.request = request
            self.schema = model.get_schema(request.params.get("s", ""))

        def upload(self):
            user_id = authenticated_userid(self.request)
            file = self.request.body_file
            params = self.request.params
            result = self.storage.upload(file, user_id, params, self.schema)
            serialized = self.schema.serialize(result)
            return {"success":True, "file": serialized}

        def download(self):
            id = self.request.matchdict["id"]
            type = self.request.matchdict.get("type", self.storage.default_type)

            path = os.path.join(self.storage.directory, id, type)
            response = FileResponse(path, request=self.request)

            item = self.storage.one(id, self.schema)
            response.content_disposition = 'attachment; filename="%s"' % item["filename"]

            return response

    return View

def expose_storage(config, app, storage_type):

    model = storage_type.model
    name = model.__name__
    storage_url = model.model_url

    level = 0
    current = storage_type
    while getattr(current, "parent_storage", None):
        current = current.parent_storage
        level += 1

    if level:
        storage_view = make_embedded_storage_view(model, level)
    else:
        storage_view = make_storage_view(model)

    for i in range(level):
        storage_url += "/{id%d}" % i

    config.add_route("non_id"+name, app.root+app.api_root+"storages/"+storage_url)
    config.add_route("id_"+name, app.root+app.api_root+"storages/"+storage_url+"/{id}")

    config.add_view(storage_view, route_name="non_id"+name, attr="list", request_method="GET", renderer="json")
    config.add_view(storage_view, route_name="non_id"+name, attr="create", request_method="POST", renderer="json")
    config.add_view(storage_view, route_name="id_"+name, attr="read", request_method="GET", renderer="json")
    config.add_view(storage_view, route_name="id_"+name, attr="update", request_method="PUT", renderer="json")
    config.add_view(storage_view, route_name="id_"+name, attr="delete", request_method="DELETE", renderer="json")

def expose_file_storage(config, app, storage_type):

    model = storage_type.model
    name = model.__name__
    storage_url = model.model_url

    storage_view = make_file_storage_view(storage_type)

    config.add_route("upload_"+name, app.root+app.api_root+"uploads/"+storage_url)
    config.add_route("download_"+name, app.root+app.api_root+"files/"+storage_url+"/{id}")
    config.add_route("typed_download_"+name, app.root+app.api_root+"files/"+storage_url+"/{id}/{type}")

    config.add_view(storage_view, route_name="upload_"+name, attr="upload", request_method="POST", renderer="json")
    config.add_view(storage_view, route_name="download_"+name, attr="download", request_method="GET")
    config.add_view(storage_view, route_name="typed_download_"+name, attr="download", request_method="GET")

def expose_service(config, app, service_type):

    def make_view(name):
        def view(request):
            return getattr(service_type(request), name)()
        return view

    exposed_methods = []
    for name in dir(service_type):
        if not name.startswith("__"):
            method = getattr(service_type, name)
            if inspect.ismethod(method):
                exposed_methods.append(name)

    for method_name in exposed_methods:
        method = make_view(method_name)

        route_name = "service_%s_%s" % (service_type.id, method_name)
        config.add_route(route_name, app.root+app.api_root+"services/"+service_type.id+"/"+method_name)
        config.add_view(method, route_name=route_name, renderer="json")

class AppResources(object):

    storage_type_map = {}
    service_type_map = {}

    def __init__(self, request, registry, storage_types, **kwargs):
        self.request = request
        self.registry = registry
        self.storage_types = storage_types

        for storage_type in storage_types:
            self.storage_type_map[storage_type.model] = storage_type

        self.__dict__.update(kwargs)

    def get_storage(self, model):
        storage_type = self.storage_type_map.get(model, None)
        if storage_type is None:
            return None
        return storage_type(self.request)

    def get_connection(self, name):
        return self.registry.queryUtility(IStorageConnection, name=name)

def borobudurize(config, app, asset_manager, base_template, client_entry_point,
                      storage_types=(), file_storage_types=(), service_types=()):

    calculator = SimplePackCalculator(app, asset_manager.manager)

    for  route, page_type_id, callback in app.get_leaf_pages():
        route_name = app.name+"."+page_type_id.replace(":", ".")

        route = app.root+route
        config.add_route(route_name, route)

        view = wrap_pyramid_view(callback, asset_manager, calculator, client_entry_point)
        config.add_view(view, route_name=route_name)

    al_route_name = app.name+"._api."+"asset.list"
    config.add_route(al_route_name, app.root+app.api_root+"assets/list/{page_type_id}")
    al_view = asset_list_view(asset_manager, calculator, client_entry_point)
    config.add_view(al_view, route_name=al_route_name)

    ac_route_name = app.name+"._api."+"asset.changed"
    config.add_route(ac_route_name, app.root+app.api_root+"assets/changed/{page_type_id}")
    ac_view = asset_changed_view(asset_manager, calculator, client_entry_point)
    config.add_view(ac_view, route_name=ac_route_name)


    for storage_type in storage_types:
        if storage_type.exposed:
            expose_storage(config, app, storage_type)

    for file_storage_type in file_storage_types:
        expose_file_storage(config, app, file_storage_type)

    for service_type in service_types:
        expose_service(config, app, service_type)

    def get_resources(request):
        app_resources = AppResources(request, config.registry, storage_types=storage_types, service_types=service_types)
        return app_resources
    config.set_request_property(get_resources, 'resources', reify=True)

    def get_app(request):
            return app
    config.set_request_property(get_app, 'app', reify=True)

    def get_document(request):
        el = etree.Element("div")
        base_template.render(el, Model())
        el = el[0]
        return Document(el)
    config.set_request_property(get_document, 'document', reify=True)




def add_storage_connection(config, name, connection):
    config.registry.registerUtility(connection, IStorageConnection, name=name)

def includeme(config):
    config.add_directive('add_storage_connection', add_storage_connection)
    config.add_directive('borobudurize', borobudurize)
