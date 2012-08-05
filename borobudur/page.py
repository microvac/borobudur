import borobudur
import prambanan
from prambanan.jslib import underscore
import prambanan.jslib.underscore

class Page(object):
    """
        a page manage models and views
    """
    title=None
    keywords=None
    description=None

    client_only = False

    parent_page_type = None
    parent_page = None

    styles=[]

    def __init__(self, app, matchdict, document, el_rendered):
        self.app = app
        self.storage_root = app.root + app.api_root + "storages"

        self.matchdict = matchdict
        self.document = document
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
        prambanan:type view_type c(borobudur.view:View)
        """
        el = self.document.el_query("#"+id)[0]
        view = view_type(self, el, model, self.el_rendered)
        self.views.append((id, view))

    def load_model(self, model_name, model_type, schema_name, **attrs):
        loader = self.loaders.model(model_name, model_type, self.storage_root, schema_name, None)
        for attr_name in attrs:
            loader.attr(attr_name, attrs.get(attr_name))

    def get_view(self, id):
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
