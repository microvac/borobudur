from pyquery.pyquery import PyQuery
import borobudur
import json
from StringIO import StringIO
from lxml import etree
from pyramid.response import Response
from borobudur.asset import PackCalculator

bootstrap_template = """
    $(function(){
        prambanan.import("prambanan").load_module_attr(%s)(%s);
    });
"""

class Document(object):
    def __init__(self, el):
        self.el = el
        self.el_query = borobudur.create_dom_query(el)
        self.q_el = self.el_query()

class AppState(object):
    leaf_page=None
    active_pages = []
    load_info = False


def wrap_pyramid_view(entry_point, page_id, page_callback, base_template, app, part, calculator):
    """
    loaded_page: id
    loaded_bundles = list of bundles
    """

    def view(request):
        packs = calculator.calculate(app)
        app_pack = packs.app
        part_pack = packs.parts[part.name]
        part_name = "%s.%s" % (app.name, part.name)

        el = etree.Element("div")
        base_template.render(el)
        el = el[0]

        app_state = AppState()
        document = Document(el)

        state = {
            "current_page": page_id,
            "loaded_pack": [app.name, part_name],
            "load_info": False
        }


        def page_success(page, index):
            state["load_info"] = {}
            state["load_info"]["index"] = index

        load_callbacks = {
            "success": page_success
        }

        page_callback(app_state, request.matchdict, document, load_callbacks)

        q_body = document.el_query("body")
        calculator.write_pack(q_body, app.name, app_pack)
        calculator.write_pack(q_body, part_name, part_pack)

        state_out = StringIO()
        entry_point_out = StringIO()
        json.dump(state, state_out)
        json.dump(entry_point, entry_point_out)
        bootstrap = bootstrap_template % (entry_point_out.getvalue(), state_out.getvalue())
        q_bootstrap = PyQuery(etree.Element("script")).html(bootstrap)
        q_body.append(q_bootstrap)

        return Response(etree.tostring(el))

    return view

def add_borobudur_app(config, app, base_template, cache_file, client_entry_point):
    calculator = PackCalculator(cache_file, client_entry_point.split(":")[0])

    for part, route, page_id, callback in app.get_leaf_pages():
        route_name = app.name+"."+part.name+"."+page_id.replace(":", ".")

        route = app.root+route
        config.add_route(route_name, route)

        view = wrap_pyramid_view(client_entry_point, page_id, callback, base_template, app, part, calculator)
        config.add_view(view, route_name=route_name)


def includeme(config):
    config.add_directive('add_borobudur_app', add_borobudur_app)
