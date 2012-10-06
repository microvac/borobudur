from borobudur.model import Model, fetch_children, Collection
from borobudur.resource import fetch_col_children
import prambanan
import borobudur
from borobudur.page.loaders import Loaders
from pramjs.elquery import ElQuery

class StopLoadException(Exception):
    pass

def find_LCA(current_page, target_page_type):
    pages = []
    page_types = []

    while current_page:
        pages.append(current_page)
        current_page = current_page.parent_page

    while target_page_type:
        page_types.append(target_page_type)
        target_page_type = target_page_type.parent_page_type

    result = None
    while len(pages) and len(page_types):
        page = pages.pop()
        page_type = page_types.pop()
        if page.__class__ != page_type:
            return result
        result = page
    return result

class PageRoutingPolicy(object):
    """
    prambanan:type page_types l(c(borobudur.page:Page))
    """

    def apply(self, request, handler_id, callbacks):
        if not hasattr(request.app, "opener"):
            setattr(request.app, "opener", PageOpener())

        request.app.opener.apply(request, handler_id, callbacks)

    def dump(self, app):
        results = {}
        results["opener"] = app.opener.dump()
        return results

    def load(self, app, serialized):
        app.opener = PageOpener()
        app.opener.load(serialized["opener"])

class PageOpener(object):
    """
    prambanan:type page_types l(c(borobudur.page:Page))
    """

    def __init__(self):
        self.leaf_page = None
        self.active_pages = []
        self.dumped = None

    def apply(self, request, page_type_id, callbacks):
        self.request = request
        self.page_type_id = page_type_id
        self.callbacks = callbacks

        self.page_types = []
        self.i = 0
        self.current = None

        if self.dumped is None:
            self.init_new()
        else:
            self.init_dumped()

        if len(self.page_types) <= 0:
            return

        if self.i < len(self.page_types):
            self.next()

    def init_dumped(self):
        dumped_page_types = self.dumped["page_types"]
        for dumped_page_type in dumped_page_types:
            self.page_types.append(prambanan.load_module_attr(dumped_page_type))

        dumped_pages = self.dumped["pages"]
        self.i = 0
        for dumped_page in dumped_pages:
            page_type = prambanan.load_module_attr(dumped_page["qname"])
            page = prambanan.JS("new page_type(self.request)")
            page.parent_page = self.leaf_page
            page.load(dumped_page["value"])
            self.active_pages.append(page)
            self.leaf_page = page
            self.i += 1

        self.dumped = None


    def init_new(self):
        page_type = prambanan.load_module_attr(self.page_type_id)

        page_types = []

        persist_page = find_LCA(self.leaf_page, page_type)

        current = persist_page
        while current is not None:
            if current.will_reload(self.request):
                persist_page = current.parent_page
            current = current.parent_page

        current = page_type
        while current is not None and (persist_page is None or current != persist_page.__class__):
            page_types.append(current)
            current = current.parent_page_type

        self.page_types = list(reversed(page_types))

        while self.leaf_page != persist_page:
            it = self.leaf_page
            it.destroy()
            self.active_pages.pop()
            self.leaf_page = it.parent_page



    def success(self):
        page = self.current
        stop_load = False
        try:
            page.open()
        except StopLoadException as e:
            stop_load = True

        def el_query(selector):
            return ElQuery(selector, self.request.document)

        if page is not None:
            if page.title is not None:
                el_query("title").html(page.title)
            if page.keywords is not None:
                el_query("meta[name='keywords']").attr("content", page.keywords)
            if page.description is not None:
                el_query("meta[name='description']").attr("content", page.description)

        self.leaf_page = page
        self.active_pages.append(page)

        self.i += 1
        if not stop_load and self.i < len(self.page_types):
            self.next()
        else:
            self.finish()

    def next(self):
        page_type = self.page_types[self.i]
        if borobudur.is_server and page_type.client_only:
            self.partial_finish()
        else:
            page = page_type(self.request)
            page.parent_page = self.leaf_page

            self.current = page

            loaders = Loaders(self.request)
            page.prepare(loaders)
            loaders.apply(self)

    def finish(self):
        self.callbacks.success()

    def partial_finish(self):
        self.i -= 1
        self.callbacks.success()

    def load(self, serialized):
        self.dumped = serialized

    def dump(self):
        results = {}
        pages = []
        for page in self.active_pages:
            ser_page = {}
            ser_page["qname"] = borobudur.get_qname(page.__class__)
            ser_page["value"] = page.dump()
            pages.append(ser_page)

        page_types = []
        for page_type in self.page_types:
            page_types.append(borobudur.get_qname(page_type))

        results["pages"] = pages
        results["page_types"] = page_types

        return results

class Page(object):
    """
    Borobudur's routing consists of mappings from url pattern to ``Page``. When a url pattern matches,
    borobudur will create an instance of the supplied Page. a ``Page`` can have a parent page, and that parent can also
    have another parent, Borobudur will create a page hierarchy, and opening them from top to down

    When a page is opened, it typically manages its models (e.g. by retrieving from ``Resources``) and renders views
    based on its models. On a browser, retrieving models must be done asynchronously, and pages code can be ugly
    really fast. Fortunately, Page API hides them  (and page's code can be flat) by its two overiddable methods:

    * ``prepare``: all async invoking operation should be done here
    * ``open``: invoked when all async operation finished.

    They can be used like this::

        class SomePage(Page):
            def prepare(self, loaders):
                self.models["users"] = User({"id": 1})
                loaders.fetch_models("users")

            def open(self):
                self.add_view("#view-id", SomeView, "users")

    **Attributes**

        client_only
            if True tells borobudur to only open it on client
        parent_page_type
            type of parent page
        parent_page
            created and set by borobudur based on ``parent_page_type``
        styles
            what css styles must be loaded when this page is open

    When a Page is opened, borobudur will set html document attributes based on these Page's attributes:

        title
            sets to ``<title>{title}</title>``
        keywords
            sets to ``<meta name="keywords" content="{keywords}" />``
        description
            sets to ``<meta name="description" content="{description}" />``

    """
    client_only = False

    parent_page_type = None
    parent_page = None

    styles=[]

    title=None
    keywords=None
    description=None

    def __init__(self, request):
        self.created_matchdict = request.matchdict
        self.created_params = request.params

        self.request = request
        self.app = request.app
        self.models = {}
        self.views = []

    def prepare(self, loaders):
        pass

    def will_reload(self, matchdict):
        return False

    def open(self):
        pass

    def load(self, serialized):
        for name in serialized["models"]:
            qname, is_collection, attrs = serialized["models"][name]
            model_type = prambanan.load_module_attr(qname)
            def _success(attrs):
                pass
            if is_collection:
                model = Collection(model_type)
                fetch_col_children(model_type, attrs, self.app.resourcer, _success)
                model.reset(model.parse(attrs))
            else:
                model = prambanan.JS("new model_type()")
                fetch_children(model_type, attrs, self.app.resourcer, _success)
                model.set(model.parse(attrs))
            self.models[name] = model

        for view_selector, view_id, view_qname, dotted_model_name, cloned_html, view_value in serialized["views"]:
            view_el = ElQuery("[data-view-id='%s']" % view_id,self.request.document)
            view_type = prambanan.load_module_attr(view_qname)
            view_model = borobudur.dotted_subscript(self.models, dotted_model_name)
            cloned_el = ElQuery(cloned_html)
            view = prambanan.JS("new view_type(self, view_el[0], view_model)")
            self.views.append((view_selector, view, cloned_el, dotted_model_name))

    def dump(self):
        import json
        import StringIO
        results = {}

        results["models"] = {}
        for name in self.models:
            model = self.models[name]
            if isinstance(model, Model):
                is_collection = False
                qname = borobudur.get_qname(model.__class__)
            else:
                is_collection = True
                qname = borobudur.get_qname(model.model)
            attrs = model.toJSON()
            results["models"][name] = (qname, is_collection, attrs)

        results["views"] = []
        for view_selector, view, cloned_el, dotted_model_name in self.views:
            view.q_el.attr("data-view-id", str(view.id))
            div = ElQuery("<div></div>")
            div.append(cloned_el)
            out = StringIO.StringIO()
            results["views"].append((view_selector, view.id, borobudur.get_qname(view.__class__), dotted_model_name, div.html(), view.dump()))

        return results

    def add_view(self, selector, view_type, dotted_model_name):
        """
        add view to document

        Arguments
            id
                html element id to be replaced by view
            view_type
                ``View``'s type to be created
            model
                model to be pass to view

        prambanan:type view_type c(borobudur.view:View)

        """

        model = borobudur.dotted_subscript(self.models, dotted_model_name)

        els = ElQuery(selector, self.request.document)
        if not els.length:
            raise ValueError("cannot find el with selector '%s' on document" % selector)
        q_el = els

        #clone to replace later when removed
        #pyquery buggy on cloned though, so after cloning, find q_el again
        cloned_el = q_el.clone()
        if borobudur.is_server:
            q_el = ElQuery(selector, self.request.document)

        view = view_type(self, q_el[0], model)

        view.render()

        self.views.append((selector, view, cloned_el, dotted_model_name))

    def get_view(self, selector):
        """
        get previously added view
        """
        for view_selector, view, cloned_el, dotted_model_name in self.views:
            if selector == view_selector:
                return view
        return None

    def destroy(self):
        reversed_views = reversed(self.views)
        for selector, view, cloned_el, dotted_model_name in reversed_views:
            view.el_query().replaceWith(cloned_el)
            view.remove()


class PagesGroup(object):
    def get_pages(self):
        pass

