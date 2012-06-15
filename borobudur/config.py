from pyramid.renderers import render_to_response
from pyramid.view import view_config
import borobudur

from lxml import etree
from pyramid.response import Response
from borobudur.asset import SimplePackCalculator
from borobudur.model import Model
import borobudur.schema

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

        return Response(etree.tostring(el, pretty_print=True))

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

def make_storage_view(schema_namespace, storage, schemas):

    class View(object):

        def __init__(self, request):
            self.request = request
            if request.params.get("s"):
                self.schema = schemas.get(schema_namespace, request.params.get("s"))
            else:
                self.schema = schemas.get(schema_namespace)

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
            sequence_schema = borobudur.schema.anonymous_sequence(self.schema)
            results = storage.all(schema=self.schema)
            serialized = sequence_schema.serialize(results)
            return render_to_response("json", serialized)

    return View

def add_borobudur_app(config, app, asset_manager, base_template, client_entry_point):

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

    for name, storage, schemas in app.storages:
        storage_view = make_storage_view(name, storage, schemas)

        config.add_route("list_"+name, app.root+app.api_root+"storages/"+name)
        config.add_route("create_"+name, app.root+app.api_root+"storages/"+name)
        config.add_route("read_"+name, app.root+app.api_root+"storages/"+name+"/{id}")
        config.add_route("update_"+name, app.root+app.api_root+"storages/"+name+"/{id}")
        config.add_route("delete_"+name, app.root+app.api_root+"storages/"+name+"/{id}")

        config.add_view(storage_view, route_name="list_"+name, attr="list", request_method="GET", renderer="json")
        config.add_view(storage_view, route_name="create_"+name, attr="create", request_method="POST", renderer="json")
        config.add_view(storage_view, route_name="read_"+name, attr="read", request_method="GET", renderer="json")
        config.add_view(storage_view, route_name="update_"+name, attr="update", request_method="PUT", renderer="json")
        config.add_view(storage_view, route_name="delete_"+name, attr="delete", request_method="DELETE", renderer="json")

def includeme(config):
    config.add_directive('add_borobudur_app', add_borobudur_app)
