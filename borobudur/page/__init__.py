from borobudur.model import Model, fetch_children, Collection
from borobudur.resource import fetch_col_children
import prambanan
import borobudur
from borobudur.page.loaders import Loaders
from pramjs.elquery import ElQuery

class AppState(object):
    leaf_page=None
    active_pages = []
    dumped_index = -1
    processed_since_loaded = False

    def dump(self):
        return self.dumped_index

    def load(self, serialized_state):
        self.dumped_index = serialized_state

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
        if not hasattr(request.app, "render_state"):
            setattr(request.app, "render_state", AppState())
        opener = PageOpener(request, handler_id)
        opener.apply(callbacks)

    def dump(self, app):
        results = {}
        results["state"] = app.render_state.dumped_index
        pages = []
        for page in app.render_state.active_pages:
            pages.append(page.dump())
        results["pages"] = pages
        return results

    def load(self, app, serialized):
        app.render_state = AppState()
        app.render_state.load(serialized["state"])
        app.dumped_pages = serialized["pages"]

class PageOpener(object):
    """
    prambanan:type page_types l(c(borobudur.page:Page))
    """

    def __init__(self, request, page_type_id):
        page_type = prambanan.load_module_attr(page_type_id)

        self.request = request
        if hasattr(request.app, "dumped_pages"):
            self.dumped_pages =  request.app.dumped_pages
        else:
            self.dumped_pages = []
        self.page_type_id = page_type_id
        self.render_state = render_state = request.app.render_state

        loaded_index = -1 if render_state.processed_since_loaded else render_state.dumped_index
        render_state.processed_since_loaded = True
        self.load_from = loaded_index + 1

        page_types = []

        persist_page = find_LCA(render_state.leaf_page, page_type)

        current = persist_page
        while current is not None:
            if current.will_reload(request):
                persist_page = current.parent_page
            current = current.parent_page

        current = page_type
        while current is not None and (persist_page is None or current != persist_page.__class__):
            page_types.append(current)
            current = current.parent_page_type

        self.persist_page = persist_page
        self.page_types = list(reversed(page_types))

    def apply(self, callbacks):
        self.callbacks = callbacks

        render_state = self.render_state
        while render_state.leaf_page != self.persist_page:
            it = render_state.leaf_page
            it.destroy()
            render_state.active_pages.pop()
            render_state.leaf_page = it.parent_page

        if len(self.page_types) <= 0:
            return

        self.i = 0
        self.current = None
        if self.i < len(self.page_types):
            self.next()

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

        render_state = self.render_state
        render_state.leaf_page = page
        render_state.active_pages.append(page)

        self.i += 1
        if not stop_load and self.i < len(self.page_types):
            self.next()
        else:
            self.finish()

    def next(self):
        page_type = self.page_types[self.i]
        if borobudur.is_server and page_type.client_only:
            self.i -= 1
            self.finish()
        else:
            page_el_rendered = self.i < self.load_from
            page = page_type(self.request, page_el_rendered)
            page.parent_page = self.render_state.leaf_page

            self.current = page

            if page_el_rendered:
                dumped_page = self.dumped_pages[self.i]
                page.load(dumped_page)
                self.success()
            else:
                loaders = Loaders(self.request)
                page.prepare(loaders)
                loaders.apply(self)

    def finish(self):
        self.render_state.dumped_index = self.i
        self.callbacks.success()


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
                self.add_view("#view-id", SomeView, self.models["users"])

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

    def __init__(self, request, el_rendered):
        self.created_matchdict = request.matchdict
        self.created_params = request.params

        self.request = request
        self.app = request.app
        self.models = {}
        self.views = []
        self.el_rendered = el_rendered

    def prepare(self, loaders):
        pass

    def will_reload(self, matchdict):
        return False

    def open(self):
        pass

    def load(self, serialized):
        ser_models = serialized["models"]
        for name in ser_models:
            ser_model = ser_models[name]
            model_type = prambanan.load_module_attr(ser_model["model_qname"])
            attrs = ser_model["value"]
            def _success(attrs):
                pass
            if ser_model["is_collection"]:
                model = Collection(model_type)
                fetch_col_children(model_type, attrs, self.app.resourcer, _success)
                model.reset(model.parse(attrs))
            else:
                model = prambanan.JS("new model_type()")
                fetch_children(model_type, attrs, self.app.resourcer, _success)
                model.set(model.parse(attrs))
            self.models[name] = model

    def dump(self):
        results = {}
        results["models"] = {}
        for name in self.models:
            model = self.models[name]
            ser_model = {}
            if isinstance(model, Model):
                ser_model["is_collection"] = False
                ser_model["model_qname"] = borobudur.get_qname(model.__class__)
            else:
                ser_model["is_collection"] = True
                ser_model["model_qname"] = borobudur.get_qname(model.model)
            ser_model["value"] = model.toJSON()
            results["models"][name] = ser_model
        return results

    def add_view(self, selector, view_type, model):
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
        els = ElQuery(selector, self.request.document)
        if not els.length:
            raise ValueError("cannot find el with selector '%s' on document" % selector)
        q_el = els

        #clone to replace later when removed
        #pyquery buggy on cloned though, so don't clone on server
        if borobudur.is_server:
            cloned_el = q_el
        else:
            cloned_el = q_el.clone()

        view = view_type(self, q_el[0], model, self.el_rendered)

        self.views.append((selector, view, cloned_el))

    def get_view(self, selector):
        """
        get previously added view
        """
        for view_selector, view, cloned_el in self.views:
            if selector == view_selector:
                return view
        return None

    def destroy(self):
        reversed_views = reversed(self.views)
        for selector, view, cloned_el in reversed_views:
            view.el_query().replaceWith(cloned_el)
            view.remove()

class PagesGroup(object):
    def get_pages(self):
        pass

