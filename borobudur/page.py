import borobudur

class BaseLoader(object):
    pass

class ModelLoader(BaseLoader):

    def __init__(self, model_type):
        self.model_type = model_type
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
        self.result = self.model_type() if self.model_type.is_collection else self.model_type(self.attrs)
        self.result.fetch(options)

class Loaders(object):
    loaders = []
    model_loaders = {}

    def model(self, name, model_type):
        result = ModelLoader(model_type)
        self.loaders.append(result)
        self.model_loaders[name] = result
        return result

    def apply(self, load_flow):
        self.i = 0
        self.len = len(self.loaders)
        self.load_flow = load_flow

        if self.i < self.len:
            self.next()
        else:
            load_flow.success()

    def success(self):
        self.i += 1
        if self.i < self.len:
            self.next()
        else:
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

    parent_page_type = None
    parent_page = None

    def __init__(self, request):
        self.dom_query = request.dom_query
        self.document = request.document
        self.loaders = Loaders()
        self.models = {}
        self.views = []

    def prepare(self, *args):
        pass

    def load(self, load_flow):
        self.loaders.apply(load_flow)

    def open(self):
        pass

    def add_view(self, id, view_type, model):
        el = self.dom_query("#"+id)[0]
        view = view_type(el, model)
        view.render()
        self.views.append((id, view))

    def get_view(self, id):
        for view_id, view in self.views:
            if id == view_id:
                return view
        return None

    def destroy(self):
        reversed_views = reversed(self.views)
        for id, view in reversed_views:
            view.el_query.replaceWidth("<div id='"+id+"'/>")
            view.remove()

class PagesGroup(object):
    def get_pages(self):
        pass
