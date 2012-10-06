import prambanan
import pramjs.elquery
import pramjs.backbone
from .native import *

query_el = pramjs.elquery.ElQuery

is_server = not prambanan.is_js

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

def get_qname(cls):
    return "%s:%s" % (cls.__module__, cls.__name__)

def dotted_subscript(container, dotted_name):
    result = container
    for name in dotted_name.split("."):
        result = result[name]
    return result

class App(object):

    def __init__(self, root, routing_policy, routes, settings):
        self.root = root
        self.routing_policy = routing_policy
        self.routes = routes
        self.settings = settings
        self.property_names = []

        self.router = Router(self)
        self.model_caches = {}
        self.counter = 0

    def next_count(self):
        self.counter += 1
        return self.counter

    def add_property(self, name, value):
        self.property_names.append(name)
        setattr(self, name, value)

    def serialize(self):
        results = {}

        routing_policy = {}
        routing_policy["qname"] = get_qname(self.routing_policy.__class__)
        routing_policy["value"] = self.routing_policy.serialize(self)
        results["routing_policy"] = routing_policy

        properties = []
        for property_name in self.property_names:
            property = getattr(self, property_name)
            property_qname = get_qname(property.__class__)
            property_value = property.serialize()
            properties.append({
                "name": property_name,
                "qname": property_qname,
                "value": property_value
            })
        results["properties"] = properties
        results["counter"] = self.counter

        return results

    def deserialize(self, serialized):
        serialized_routing_policy = serialized["routing_policy"]
        routing_policy_type = prambanan.load_module_attr(serialized_routing_policy["qname"])
        routing_policy = prambanan.JS("new routing_policy_type()")
        routing_policy.deserialize(self, serialized_routing_policy["value"])
        self.routing_policy = routing_policy

        serialized_properties = serialized["properties"]
        for serialized_property in serialized_properties:
            property_name = serialized_property["name"]
            property_type = prambanan.load_module_attr(serialized_property["qname"])
            property = prambanan.JS("new property_type()")
            property.deserialize(serialized_property["value"])
            self.add_property(property_name, property)

        self.counter = serialized["counter"]

