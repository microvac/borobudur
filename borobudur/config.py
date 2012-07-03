from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.view import view_config

import borobudur
import borobudur.schema
import borobudur.storage
import borobudur.storage.mongo

from borobudur.asset import SimplePackCalculator
from borobudur.model import Model

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

def wrap_pyramid_view(page_callback, base_template, asset_manager, calculator, entry_point):
    """
    loaded_page: id
    loaded_bundles = list of bundles
    """

    def view(request):
        el = etree.Element("div")
        base_template.render(el, Model())
        el = el[0]

        app_state = AppState()
        document = Document(el)

        def page_success(load_flow):
            asset_manager.write_all(load_flow, calculator, entry_point)

        load_callbacks = {
            "success": page_success
        }

        page_callback(app_state, request.matchdict, document, load_callbacks)

        return Response(etree.tostring(el, pretty_print=True, method="html"))

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

def make_embedded_storage_view(model, storage, level):

    class View(object):

        def __init__(self, request):
            self.request = request
            self.schema = model.get_schema(request.params.get("s", ""))

            id = None
            current_id_level = 0
            while current_id_level < level:
                id_name = "id%d" % current_id_level
                id = (self.request.matchdict[id_name], id)
                current_id_level += 1

            self.id = id

        def create(self):
            appstruct = self.schema.deserialize(self.request.json_body)
            result = storage.insert(self.id, appstruct, self.schema)
            serialized = self.schema.serialize(result)
            return render_to_response("json", serialized)

        def read(self):
            result = storage.one(self.id, self.request.matchdict["id"], self.schema)
            serialized = self.schema.serialize(result)
            return render_to_response("json", serialized)

        def update(self):
            appstruct = self.schema.deserialize(self.request.json_body)
            result = storage.update(self.id, appstruct, self.schema)
            serialized = self.schema.serialize(result)
            return render_to_response("json", serialized)

        def delete(self):
            pass

        def list(self):
            skip = self.request.params.get("ps", 0)
            limit = self.request.params.get("pl", 0)
            config = borobudur.storage.SearchConfig(skip, limit)

            results = storage.all(self.id, config=config, schema=self.schema)
            sequence_schema = borobudur.schema.SequenceSchema(self.schema)
            serialized = sequence_schema.serialize(results)
            return render_to_response("json", serialized)

    return View

def make_storage_view(model, storage):

    class View(object):

        def __init__(self, request):
            self.request = request
            self.schema = model.get_schema(request.params.get("s", ""))

        def create(self):
            appstruct = self.schema.deserialize(self.request.json_body)
            result = storage.insert(appstruct, self.schema)
            serialized = self.schema.serialize(result)
            return render_to_response("json", serialized)

        def read(self):
            result = storage.one(self.request.matchdict["id"], self.schema)
            serialized = self.schema.serialize(result)
            return render_to_response("json", serialized)

        def update(self):
            appstruct = self.schema.deserialize(self.request.json_body)
            result = storage.update(appstruct, self.schema)
            serialized = self.schema.serialize(result)
            return render_to_response("json", serialized)

        def delete(self):
            result = storage.delete(self.request.matchdict["id"])
            return render_to_response("json", result)

        def list(self):
            skip = self.request.params.get("ps", 0)
            limit = self.request.params.get("pl", 0)
            sort_order = self.request.params.get("so")
            sort_criteria = self.request.params.get("sc")
            sorts = None
            if sort_criteria and sort_order:
                sorts = borobudur.storage.SearchSort(sort_criteria, sort_order)
            elif sort_criteria:
                sorts = borobudur.storage.SearchSort(sort_criteria)

            config = borobudur.storage.SearchConfig(skip, limit, sorts)

            results = storage.all(schema=self.schema, config=config)
            sequence_schema = borobudur.schema.SequenceSchema(self.schema)
            serialized = sequence_schema.serialize(results)
            return render_to_response("json", serialized)

    return View

def expose_storage(config, app, storage):

    model = storage.model
    name = model.__name__
    storage_url = model.storage_url

    level = 0
    current = storage
    while getattr(current, "parent_storage", None):
        current = current.parent_storage
        level += 1

    if level:
        storage_view = make_embedded_storage_view(model, storage, level)
    else:
        storage_view = make_storage_view(model, storage)

    for i in range(level):
        storage_url += "/{id%d}" % i

    config.add_route("list_"+name, app.root+app.api_root+"storages/"+storage_url)
    config.add_route("create_"+name, app.root+app.api_root+"storages/"+storage_url)
    config.add_route("read_"+name, app.root+app.api_root+"storages/"+storage_url+"/{id}")
    config.add_route("update_"+name, app.root+app.api_root+"storages/"+storage_url+"/{id}")
    config.add_route("delete_"+name, app.root+app.api_root+"storages/"+storage_url+"/{id}")

    config.add_view(storage_view, route_name="list_"+name, attr="list", request_method="GET", renderer="json")
    config.add_view(storage_view, route_name="create_"+name, attr="create", request_method="POST", renderer="json")
    config.add_view(storage_view, route_name="read_"+name, attr="read", request_method="GET", renderer="json")
    config.add_view(storage_view, route_name="update_"+name, attr="update", request_method="PUT", renderer="json")
    config.add_view(storage_view, route_name="delete_"+name, attr="delete", request_method="DELETE", renderer="json")

def add_borobudur_app(config, app, asset_manager, base_template, client_entry_point, storages):

    calculator = SimplePackCalculator(app)

    for  route, page_type_id, callback in app.get_leaf_pages():
        route_name = app.name+"."+page_type_id.replace(":", ".")

        route = app.root+route
        config.add_route(route_name, route)

        view = wrap_pyramid_view(callback, base_template, asset_manager, calculator, client_entry_point)
        config.add_view(view, route_name=route_name)

    al_route_name = app.name+"._api."+"asset.list"
    config.add_route(al_route_name, app.root+app.api_root+"assets/list/{page_type_id}")
    al_view = asset_list_view(asset_manager, calculator, client_entry_point)
    config.add_view(al_view, route_name=al_route_name)

    ac_route_name = app.name+"._api."+"asset.changed"
    config.add_route(ac_route_name, app.root+app.api_root+"assets/changed/{page_type_id}")
    ac_view = asset_changed_view(asset_manager, calculator, client_entry_point)
    config.add_view(ac_view, route_name=ac_route_name)

    for storage in storages:
        expose_storage(config, app, storage)

def includeme(config):
    config.add_directive('add_borobudur_app', add_borobudur_app)
