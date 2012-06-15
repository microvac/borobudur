from pyramid.renderers import render_to_response
from pyramid.view import view_config
import borobudur

from lxml import etree
from pyramid.response import Response
from borobudur.asset import SimplePackCalculator
from borobudur.model import Model

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


def includeme(config):
    config.add_directive('add_borobudur_app', add_borobudur_app)
