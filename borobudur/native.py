from lxml import etree
from pyramid.response import Response
from pyquery import PyQuery
from borobudur.asset import PrambananModuleBundle
import os

__all__ = ["create_dom_query", "wrap_pyramid_view"]

def create_dom_query(el):
    def dom_query(selector=None):
        if selector is None:
            return PyQuery(el)
        else:
            return PyQuery(el)(selector)
    return dom_query

def add_modules(manager, dom_query, name, modules, env):
    if not modules:
        return
    abs_dir = os.path.join("testapp", "static", "b", name)
    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)
    dir = "b/"+name+"/"
    bundle = PrambananModuleBundle(abs_dir, dir, manager, modules, filters="uglifyjs", output="b/"+name+".js")
    for url in bundle.urls(env):
        dom_query.append("<script type='text/javascript' src='%s'> </script>\n" % url)

def wrap_pyramid_view(fn, app, part):

    def view(request):
        el = etree.Element("div")
        app.base_template.render(el)
        el = el[0]
        request.document = el
        request.dom_query = create_dom_query(el)

        request.app_state = app.get_state()

        fn(request)

        body = request.dom_query("body")
        add_modules(app.prambanan_manager, body, app.name, app.modules, app.asset_env)
        for part in app.parts:
            name = "%s.%s" % (app.name, part.name)
            add_modules(app.prambanan_manager, body, name, part.modules, app.asset_env)

        return Response(etree.tostring(el))

    return view

