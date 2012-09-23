import prambanan
import pramjs.elquery
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

    def load(self, serialized_state):
        pass

    def dump(self):
        return {}

class DefaultRoutingPolicy(object):

    state_type = AppState

    def __init__(self, handler_id):
        self.handler_id = handler_id

    def apply(self, request, app_state, callbacks):
        callbacks["success"](app_state)


class App(object):

    def __init__(self, root, routing_policy, routes, settings):
        self.root = root
        self.routing_policy = routing_policy
        self.routes = routes
        self.settings = settings

        self.router = Router(self)
        self.model_caches = {}

