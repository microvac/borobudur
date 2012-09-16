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
        el = self.request.document.el_query("#"+id)[0]
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

    def load_model(self, model_name, model_type, schema_name, **attrs):
        loader = self.loaders.model(model_name, model_type, self.app.storage_root, schema_name, None)
        for attr_name in attrs:
            loader.attr(attr_name, attrs.get(attr_name))

    def destroy(self):
        reversed_views = reversed(self.views)
        for id, view in reversed_views:
            view.el_query().replaceWith("<div id='"+id+"'/>")
            view.remove()

class PagesGroup(object):
    def get_pages(self):
        pass
