import inspect
import os
from pyramid.response import Response, FileResponse
from pyramid.renderers import render_to_response
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from zope.interface.interface import Interface

import borobudur
from borobudur.interfaces import IApp
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

def wrap_pyramid_view(page_callback):
    """
    loaded_page: id
    loaded_bundles = list of bundles
    """

    def view(request):
        def page_success(load_flow):
            request.app.asset_manager.write_all(request.app, request.document, load_flow)

        load_callbacks = {
            "success": page_success
        }
        app_state = AppState()
        page_callback(request, app_state, load_callbacks)

        html = etree.tostring(request.document.el, pretty_print=True, method="html")

        return Response("<!DOCTYPE html>\n"+html)

    return view

def asset_list_view(request):
    calculate = request.app.asset_calculator
    page_type_id = request.matchdict["page_type_id"]

    packs = list(calculate(page_type_id))
    styles = ["bootstrap"]

    results = {
        "css": {},
        "js": {},
    }

    asset_manager = request.app.asset_manager
    for type, name, bundle in asset_manager.get_all_bundles(packs, styles):
        results[type][name] = [url for url in bundle.urls(asset_manager.env)]

    return render_to_response("json", results)


def asset_changed_view(request):
    calculate = request.app.asset_calculator
    page_type_id = request.matchdict["page_type_id"]

    import time
    packs = list(calculate(page_type_id))
    styles = ["bootstrap"]

    results = {"js":[], "css":[]}

    asset_manager = request.app.asset_manager

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

def expose(*exposers):
    def decorate(cls):
        setattr(cls, "_exposers", exposers)
        return cls
    return decorate

def try_expose(cls, config, app):
    if hasattr(cls, "_exposers"):
        for exposer in getattr(cls, "_exposers"):
            exposer(config, app, cls)

class AppResources(object):

    def __init__(self, request, registry, resource_types, storage_type_map):
        self.request = request
        self.registry = registry
        self.resource_types = resource_types
        self.storage_type_map = storage_type_map

    def get_storage(self, model):
        storage_type = self.storage_type_map.get(model, None)
        if storage_type is None:
            return None
        return storage_type(self.request)

    def get_connection(self, name):
        return self.registry.queryUtility(IStorageConnection, name=name)

def add_app(config, app, resource_types):

    for  route, page_type_id, callback in app.get_leaf_pages():
        route_name = app.name+"."+page_type_id.replace(":", ".")

        route = app.root+route
        config.add_route(route_name, route)

        view = wrap_pyramid_view(callback)
        config.add_view(view, route_name=route_name)

    al_route_name = app.name+"._api."+"asset.list"
    config.add_route(al_route_name, app.root+app.api_root+"assets/list/{page_type_id}")
    config.add_view(asset_list_view, route_name=al_route_name)

    ac_route_name = app.name+"._api."+"asset.changed"
    config.add_route(ac_route_name, app.root+app.api_root+"assets/changed/{page_type_id}")
    config.add_view(asset_changed_view, route_name=ac_route_name)

    for resource_type in resource_types:
        try_expose(resource_type, config, app)

    config.registry.registerUtility(app, IApp)

    storage_type_map = {}
    for resource_type in resource_types:
        if issubclass(resource_type, borobudur.storage.mongo.MongoStorage) or issubclass(resource_type, borobudur.storage.mongo.EmbeddedMongoStorage):
            storage_type_map[resource_type.model] = resource_type
    def get_resources(request):
        app_resources = AppResources(request, config.registry, resource_types=resource_type, storage_type_map=storage_type_map)
        return app_resources
    config.set_request_property(get_resources, 'resources', reify=True)

    def get_app(request):
            return app
    config.set_request_property(get_app, 'app', reify=True)

    def get_document(request):
        el = etree.Element("div")
        request.app.base_template.render(el, Model())
        el = el[0]
        return Document(el)
    config.set_request_property(get_document, 'document', reify=True)


def add_storage_connection(config, name, connection):
    config.registry.registerUtility(connection, IStorageConnection, name=name)

def includeme(config):
    config.add_directive('add_storage_connection', add_storage_connection)
    config.add_directive('add_app', add_app)

def configure_server_app(app, asset_manager, asset_calculator, base_template, client_entry_point):
    app.asset_manager = asset_manager
    app.base_template = base_template
    app.client_entry_point = client_entry_point
    app.asset_calculator = asset_calculator(app)

