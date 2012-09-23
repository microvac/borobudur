import prambanan
import pramjs.elquery
import pramjs.backbone
from .native import *

query_el = pramjs.elquery.ElQuery

is_server = not prambanan.is_js

def default_route_handler_factory(route_handler_id):
    impl = prambanan.load_module_attr(route_handler_id)

    def handler(request, route_callbacks):
        impl(request)
        route_callbacks["success"]()

    return handler

class AppState(object):

    rendered = False

    def load(self, serialized_state):
        self.rendered = True

    def dump(self):
        return {}

class DefaultRoutingPolicy(object):

    def apply(self, request, handler_id, app_state, callbacks):
        if app_state.rendered:
            app_state.rendered = False
            callbacks.success()
            return

        impl = prambanan.load_module_attr(handler_id)
        impl(request, callbacks)

    def create_state(self):
        return AppState()


class App(object):

    def __init__(self, root, routing_policy, routes, settings):
        self.root = root
        self.routing_policy = routing_policy
        self.routes = routes
        self.settings = settings

        self.router = Router(self)
        self.model_caches = {}

