import borobudur
import prambanan
from prambanan.jslib import underscore
import prambanan.jslib.underscore

class BaseLoader(object):
    pass

class ModelLoader(BaseLoader):
    """
    prambanan:type model_type c(borobudur.model:Model)
    """

    def __init__(self, model_type, schema_name=None, parent=None):
        self.model_type = model_type
        self.parent = parent
        self.schema_name = schema_name

        self.attrs = {}
        self.params = {}

    def attr(self, name, value):
        self.attrs[name] = value
        return self

    def param(self, name, value):
        self.params[name] = value
        return self

    def load(self, callbacks):
        options = {
            "data": self.params,
            "success":callbacks.success,
            "error": callbacks.error
        }
        self.result = self.model_type() if self.model_type.is_collection else self.model_type(self.attrs, self.schema_name, self.parent)
        self.result.fetch(options)

class Loaders(object):
    loaders = []
    model_loaders = {}

    def model(self, name, model_type, schema_name=None, parent=None):
        result = ModelLoader(model_type, schema_name, parent)
        self.loaders.append(result)
        self.model_loaders[name] = result
        if prambanan.is_js:
            self.success = underscore.bind(self.success, self)
        return result

    def apply(self, page, load_flow):
        self.i = 0
        self.len = len(self.loaders)
        self.page = page
        self.load_flow = load_flow

        if self.i < self.len:
            self.next()
        else:
            for name in self.model_loaders:
                page.models[name] = self.model_loaders[name].result
            load_flow.success()

    def success(self):
        self.i += 1
        if self.i < self.len:
            self.next()
        else:
            for name in self.model_loaders:
                self.page.models[name] = self.model_loaders[name].result
            self.load_flow.success()

    def next(self):
        loader = self.loaders[self.i]
        loader.load(self)

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

    def __init__(self, matchdict, document, el_rendered):
        self.matchdict = matchdict
        self.document = document
        self.loaders = Loaders()
        self.models = {}
        self.views = []
        self.el_rendered = el_rendered

    def prepare(self):
        pass

    def will_reload(self, match_dict):
        return False

    def load(self, load_flow):
        self.loaders.apply(self, load_flow)

    def open(self ):
        pass

    def add_view(self, id, view_type, model):
        """
        prambanan:type view_type c(borobudur.view:View)
        """
        el = self.document.el_query("#"+id)[0]
        view = view_type(el, model, self.el_rendered)
        self.views.append((id, view))

    def load_model(self, model_name, model_type, schema_name, **attrs):
        loader = self.loaders.model(model_name, model_type, schema_name, None)
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
