import inspect

class ServiceExposer(object):

    def __call__(self, config, resource_root, factory, service_type):

        def make_view(name):
            def view(request):
                result =  getattr(service_type(request), name)()
                if hasattr(result, "toJSON"):
                    return result.toJSON()
                return result
            return view

        exposed_methods = []
        for name in dir(service_type):
            if not name.startswith("__"):
                method = getattr(service_type, name)
                if inspect.ismethod(method):
                    exposed_methods.append(name)

        for method_name in exposed_methods:
            method = make_view(method_name)

            route_name = "service.%s.%s" % (service_type.id, method_name)
            config.add_route(route_name, resource_root+"services/"+service_type.id+"/"+method_name, factory=factory)
            config.add_view(method, route_name=route_name, renderer="json")
