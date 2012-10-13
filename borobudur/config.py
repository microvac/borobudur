from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response

import borobudur
from borobudur.interfaces import IAppConfigurator, IBootstrapSubscriber, IAppRoot, IAssetCalculator

from borobudur.asset import SimplePackCalculator
from borobudur.model import Model

from lxml import etree

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

        def page_success():
            request.app_config.asset_manager.write_all(request, handler_type_id)

        try:
            load_callbacks = Callbacks(page_success)
            routing_policy.apply(request, handler_type_id, load_callbacks)
        except borobudur.RedirectException as e:
            raise HTTPFound(e.url)

        html = etree.tostring(request.document, pretty_print=True, method="html")

        return Response("<!DOCTYPE html>\n" + html)

    return view



def create_factory(**kwargs):
    class Factory(object):
        def __init__(self, request):
            self.__dict__.update(kwargs)

    return Factory


def add_borobudur(config, name, app_config, root="/" ):

    factory = create_factory(app_name=name, app_root=root)

    for  route, route_handler_id in app_config.routes:
        route_name = name + "." + route_handler_id.replace(":", ".")

        route = root + route
        config.add_route("page."+route_name, route, factory=factory)

        view = wrap_pyramid_view(route_handler_id)
        config.add_view(view, route_name="page."+route_name)

    asset_calculator = app_config.asset_calculator_factory(app_config, name, config.registry)
    config.registry.registerUtility(asset_calculator, IAssetCalculator, name=name)
    config.registry.registerUtility(app_config, IAppConfigurator, name=name)


def get_app(request):
    app_root = request.context.app_root
    app_config = request.app_config
    app = borobudur.App(app_root, app_config.routing_policy, app_config.routes, app_config.settings)
    for name, factory in app_config.app_properties:
        app.add_property(name, factory(request, app))
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
    config.add_directive('add_global_bootstrap_subscriber', add_global_bootstrap_subscriber)

    config.set_request_property(get_app, 'app', reify=True)
    config.set_request_property(get_app_config, 'app_config', reify=True)
    config.set_request_property(get_document, 'document', reify=True)

class AppConfigurator(object):
    settings = {}

    def __init__(self, asset_manager, base_template,
                 routing_policy=None,
                 asset_calculator_factory=None):

        if asset_calculator_factory is None:
            asset_calculator_factory = SimplePackCalculator

        self.asset_manager = asset_manager
        self.base_template = base_template
        self.asset_calculator_factory = asset_calculator_factory
        self.routes = []
        self.bootstrap_subscribers = []
        self.app_properties = []

        if routing_policy is None:
            routing_policy = borobudur.DefaultRoutingPolicy()

        self.routing_policy = routing_policy

    def add_route(self, route, handler_type):
        handler_id = "%s:%s" % (handler_type.__module__, handler_type.__name__)
        self.add_route_conf(route, handler_id)

    def add_route_conf(self, route, route_handler_id):
        self.routes.append((route, route_handler_id))

    def add_bootstrap_subscriber(self, subscriber_qname):
        self.bootstrap_subscribers.append(subscriber_qname)

    def set_app_property(self, name, factory):
        self.app_properties.append((name, factory))

    def get_bootstrap_subscribers(self, registry):
        results = self.bootstrap_subscribers[:]
        for name, value in registry.getUtilitiesFor(IBootstrapSubscriber):
            results.append(value)
        return results

