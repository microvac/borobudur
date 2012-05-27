from pyramid.response import Response
from pyramid.security import authenticated_userid
from lxml import etree
from pyquery import PyQuery as DomQuery
from prambanan.zpt.template import TemplateRegistry

class LoadFlow(object):
    def __init__(self, page_types):
        self.persist_page = True
        self.page_types = page_types

class Router(object):
    leaf_page=True
    active_pages = []

def apply_load_flow(router, load_flow, request):

    while router.leaf_page != load_flow.persist_page:
        it = router.leaf_page
        router.active_pages.pop()
        router.leaf_page = it.parent_page

    page_types = load_flow.page_types

    if len(page_types) <= 0:
        return

    current = [0, None]

    callbacks = {}

    def success():
        page = current[1]
        page.open()
        router.leaf_page = page
        router.active_pages.append(page)

        current[0] += 1
        if current[0] < len(page_types):
            callbacks["run"]()
        else:
            dom_query = request.dom_query
            if page.title is not None:
                dom_query("title").html(page.title)
            if page.keywords is not None:
                dom_query("meta[name='keywords']").attr("content", page.keywords)
            if page.description is not None:
                dom_query("meta[name='description']").attr("content", page.description)


    def run():
        page_type = page_types[current[0]]

        page = page_type(request)
        page.prepare()
        current[1] = page
        page.load(callbacks)

    callbacks["success"] = success
    callbacks["run"] = run
    callbacks["run"]()

def make_callback(app, page_type):

    page_types = []
    current = page_type
    while current is not None:
        page_types.append(current)
        current = current.parent_page_type
    page_types = list(reversed(page_types))

    def cb(request):
        router = Router()
        el = etree.Element("div")
        app.render_base(el)
        el = el[0]

        request.document = el
        request.dom_query = DomQuery(el)

        load_flow = LoadFlow(page_types)
        apply_load_flow(router, load_flow, request)

        return Response(etree.tostring(el))
    return cb

class App(object):
    def __init__(self, package_name, base_template, parts=None):
        self.package_name = package_name
        self.base_template=base_template
        self.parts=parts

        self.templates = TemplateRegistry()
        self.render_base = self.templates.register_py(package_name, base_template)

        self.pages = []

    def register_page(self, page, order, routes):
        for route in routes:
            self.pages.append((page, order, route))
        return page

    def page(self, *routes):
        def decorate(page):
            return self.register_page(page, 0, routes)
        return decorate

    def make_view(self, pages):
        pass

    def get_leaf_pages(self, app_root):
        sorted_pages = sorted(self.pages, key=lambda i: i[1])
        return [(app_root+route, make_callback(self, page)) for page, order, route in sorted_pages]

    def bootstrap(self, app_root):
        i = 0
        for route, leaf in self.get_leaf_pages(app_root):
            i += 1
            name = "borobudur_page"+str(i)
            self.config.add_route(name, route)
            self.config.add_view(leaf, route_name=name)

