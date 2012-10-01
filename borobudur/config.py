from pyramid.response import Response
from pyramid.renderers import render_to_response

import borobudur
from borobudur.interfaces import IAppConfigurator, IBootstrapSubscriber, IAppRoot
import borobudur.resource.storage
import borobudur.resource.storage.mongo

from borobudur.asset import SimplePackCalculator
from borobudur.model import Model

from lxml import etree
from borobudur.page import AppState

class Callbacks(object):
    def __init__(self, success):
        self.success = success

def wrap_pyramid_view(handler_type_id):
    """
    loaded_page: id
    loaded_bundles = list of bundles
    """

    def view(request):
        routing_policy = request.app.routing_policy
        app_state = routing_policy.create_state()

        def page_success():
            request.app_config.asset_manager.write_all(request, handler_type_id, app_state.dump())

        load_callbacks = Callbacks(page_success)
        routing_policy.apply(request, handler_type_id, app_state, load_callbacks)

        html = etree.tostring(request.document, pretty_print=True, method="html")

        return Response("<!DOCTYPE html>\n" + html)

    return view



def expose(*exposers):
    def decorate(cls):
        setattr(cls, "_exposers", exposers)
        return cls

    return decorate


def try_expose(cls, config, app, factory):
    if hasattr(cls, "_exposers"):
        for exposer in getattr(cls, "_exposers"):
            exposer(config, app, factory, cls)


def create_factory(**kwargs):
    class Factory(object):
        def __init__(self, request):
            self.__dict__.update(kwargs)

    return Factory


class AppResources(object):
    def __init__(self, request, resource_types, storage_type_map):
        self.request = request
        self.resource_types = resource_types
        self.storage_type_map = storage_type_map

    def get_storage(self, model):
        storage_type = self.storage_type_map.get(model, None)
        if storage_type is None:
            return None
        return storage_type(self.request)

r_map = {}

def add_resources(config, name, resource_types, root):
    factory = create_factory(resource_name=name)

    storage_type_map = {}
    for resource_type in resource_types:
        if issubclass(resource_type, borobudur.resource.storage.mongo.MongoStorage) or issubclass(resource_type,
            borobudur.resource.storage.mongo.EmbeddedMongoStorage):
            storage_type_map[resource_type.model] = resource_type
    r_map[name] = (storage_type_map, resource_types, root)
    for resource_type in resource_types:
        try_expose(resource_type, config, root, factory)


def add_borobudur(config, name, app_config, root="/" ):

    factory = create_factory(app_name=name, app_root=root)

    for  route, route_handler_id in app_config.routes:
        route_name = name + "." + route_handler_id.replace(":", ".")

        route = root + route
        config.add_route("page."+route_name, route, factory=factory)

        view = wrap_pyramid_view(route_handler_id)
        config.add_view(view, route_name="page."+route_name)

    config.registry.registerUtility(app_config, IAppConfigurator, name=name)

def get_resources(request):
    storage_type_map, resource_types, resource_root = r_map[request.context.resource_name]
    app_resources = AppResources(request, resource_types=resource_types, storage_type_map=storage_type_map)
    return app_resources


def get_app(request):
    app_root = request.context.app_root
    app_config = request.app_config
    app = borobudur.App(app_root, app_config.routing_policy, app_config.routes, app_config.settings)
    return app


def get_app_config(request):
    app_name = request.context.app_name
    return request.registry.queryUtility(IAppConfigurator, name=app_name)


def get_document(request):
    el = etree.Element("div")
    request.app_config.base_template.render(el, Model())
    el = el[0]
    return el

def add_global_bootstrap_subscriber(config, subscriber_qname):
    config.registry.registerUtility(subscriber_qname, IBootstrapSubscriber, name=subscriber_qname)

def includeme(config):
    config.add_directive('add_borobudur', add_borobudur)
    config.add_directive('add_resources', add_resources)
    config.add_directive('add_global_bootstrap_subscriber', add_global_bootstrap_subscriber)

    config.set_request_property(get_resources, 'resources', reify=True)
    config.set_request_property(get_app, 'app', reify=True)
    config.set_request_property(get_app_config, 'app_config', reify=True)
    config.set_request_property(get_document, 'document', reify=True)

class AppConfigurator(object):
    settings = {}

    def __init__(self, asset_manager, base_template,
                 routing_policy=None,
                 app_state_type=AppState):
        self.asset_manager = asset_manager
        self.base_template = base_template
        self.asset_calculator = SimplePackCalculator(self)
        self.module_names = []
        self.routes = []
        self.bootstrap_subscribers = []

        if routing_policy is None:
            routing_policy = borobudur.DefaultRoutingPolicy()

        self.routing_policy = routing_policy
        self.app_state_type = app_state_type

    def add_route(self, route, handler_type):
        handler_id = "%s:%s" % (handler_type.__module__, handler_type.__name__)
        self.add_route_conf(route, handler_id)

    def add_route_conf(self, route, route_handler_id):
        self.routes.append((route, route_handler_id))

        module = route_handler_id.split(":")[0]
        if not module in self.module_names:
            self.module_names.append(module)

    def add_bootstrap_subscriber(self, subscriber_qname):
        self.bootstrap_subscribers.append(subscriber_qname)

    def get_bootstrap_subscribers(self, request):
        results = self.bootstrap_subscribers[:]
        for name, value in request.registry.getUtilitiesFor(IBootstrapSubscriber):
            results.append(value)
        return results

