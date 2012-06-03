import prambanan
from .native import *

is_server = not prambanan.is_js

def add_borobudur_app(config, app_root, app):
    i = 0
    for route, name, view in app.get_pyramid_views():
        i += 1
        route = app_root+route
        config.add_route(name, route)
        config.add_view(view, route_name=name)


def includeme(config):
    config.add_directive('add_borobudur_app', add_borobudur_app)
