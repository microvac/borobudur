from borobudur.resource.channel import socketio_service
from borobudur.resource.storage.mongo import MongoStorage, EmbeddedMongoStorage

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
    def __init__(self, request, resource_types, storage_type_map, service_id_map):
        self.request = request
        self.resource_types = resource_types
        self.storage_type_map = storage_type_map
        self.service_id_map = service_id_map

    def get_storage(self, model):
        storage_type = self.storage_type_map.get(model, None)
        if storage_type is None:
            return None
        return storage_type(self.request)

    def get_service(self, id):
        service_type = self.service_id_map[id]
        return service_type(self.request)

r_map = {}

def add_resources(config, name, resource_types, root):
    factory = create_factory(resources_name=name)

    storage_type_map = {}
    service_id_map = {}
    for resource_type in resource_types:
        if issubclass(resource_type, MongoStorage) or issubclass(resource_type, EmbeddedMongoStorage):
            storage_type_map[resource_type.model] = resource_type
        if hasattr(resource_type, "id"):
            service_id_map[resource_type.id] = resource_type

    r_map[name] = (storage_type_map, service_id_map, resource_types, root)
    for resource_type in resource_types:
        try_expose(resource_type, config, root, factory)

    channel_name = "%s/channels" % name
    config.add_route(channel_name, "socket.io/*remaining")
    config.add_view(socketio_service, route_name=channel_name)

def get_resources(request):
    storage_type_map, service_id_map, resource_types, resource_root = r_map[request.context.resources_name]
    app_resources = AppResources(request, resource_types=resource_types, storage_type_map=storage_type_map, service_id_map=service_id_map)
    return app_resources

def includeme(config):
    config.add_directive('add_resources', add_resources)
    config.set_request_property(get_resources, 'resources', reify=True)
