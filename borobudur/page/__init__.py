import borobudur
from borobudur.page.loaders import Loaders
import prambanan
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

    def apply(self, request, handler_id, app_state, callbacks):
        opener = PageOpener(request, handler_id, app_state)
        opener.apply(callbacks)

    def create_state(self):
        return AppState()

class PageOpener(object):
    """
    prambanan:type page_types l(c(borobudur.page:Page))
    """

    def __init__(self, request, page_type_id, app_state):
        page_type = prambanan.load_module_attr(page_type_id)

        self.request = request
        self.page_type_id = page_type_id
        self.app_state = app_state

        loaded_index = -1 if app_state.processed_since_loaded else app_state.dumped_index
        app_state.processed_since_loaded = True
        self.load_from = loaded_index + 1

        page_types = []

        persist_page = find_LCA(app_state.leaf_page, page_type)

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

        app_state = self.app_state
        while app_state.leaf_page != self.persist_page:
            it = app_state.leaf_page
            it.destroy()
            app_state.active_pages.pop()
            app_state.leaf_page = it.parent_page

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

        app_state = self.app_state
        app_state.leaf_page = page
        app_state.active_pages.append(page)

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
            page.parent_page = self.app_state.leaf_page

            self.current = page

            loaders = Loaders(page)
            page.prepare(loaders)
            loaders.apply(self)

    def finish(self):
        self.app_state.dumped_index = self.i
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
                self.add_view("view-id", SomeView, self.models["users"])

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

    def open(self ):
        pass

    def add_view(self, id, view_type, model):
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
        el = ElQuery("#"+id, self.request.document)[0]
        view = view_type(self, el, model, self.el_rendered)
        self.views.append((id, view))

    def get_view(self, id):
        """
        get previously added view
        """
        for view_id, view in self.views:
            if id == view_id:
                return view
        return None

    def destroy(self):
        reversed_views = reversed(self.views)
        for id, view in reversed_views:
            view.el_query().replaceWith("<div id='"+id+"'/>")
            view.remove()

class PagesGroup(object):
    def get_pages(self):
        pass

