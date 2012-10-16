import inspect
import json
from pyramid.response import Response
from borobudur import NotFoundException, InvalidRequestException

class ServiceExposer(object):

    def __call__(self, config, resource_root, factory, service_type):

        def make_view(name):
            def view(request):
                json_body = request.json_body
                args = []
                if json_body is not None:
                    args = json_body
                try:
                    result =  getattr(service_type(request), name)(*args)
                    if hasattr(result, "toJSON"):
                        return result.toJSON()
                    return result
                except NotFoundException as e:
                    err = {}
                    err["type"] = "Not Found"
                    return Response(json.dumps(err), status=404, content_type="application/json")
                except InvalidRequestException as e:
                    err = {}
                    err["message"] = e.message
                    return Response(json.dumps(err), status=400, content_type="application/json")
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
