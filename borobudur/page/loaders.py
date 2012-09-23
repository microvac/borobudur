import borobudur
from borobudur.model import Model, fetch_children
import prambanan
from pramjs import underscore

__author__ = 'h'

class BaseLoader(object):
    pass

class ServiceModelLoader(BaseLoader):

    def __init__(self, service_id, service_attr):
        self.service_id = service_id

        self.service_attr = service_attr

    def load(self, app, model, callbacks):

        def prev_success(attrs):
            parsed = model.parse(attrs)
            if isinstance(model, Model):
                model.set(parsed)
            else:
                model.reset(parsed)
            callbacks.success()

        def fetch_success(attrs):
            if isinstance(model, Model):
                def _success():
                    prev_success(attrs)
                fetch_children(model.__class__, attrs, app, _success)
            else:
                count = 0
                def col_success():
                    global count
                    count += 1
                    if count == len(attrs):
                        prev_success(attrs)
                for item_attrs in attrs:
                    fetch_children(model.model, item_attrs, app, col_success)
                if len(attrs) == 0:
                    prev_success(attrs)

        url = "%s/%s/%s" % (app.settings["service_root"], self.service_id, self.service_attr)
        borobudur.query_el.getJSON(url, fetch_success)

class StorageModelLoader(BaseLoader):

    def load(self, app, model, callbacks):
        options = {
            "data": self.params,
            }
        model.fetch(app, callbacks.success, callbacks.error, options)

class ServiceInvoker(object):

    def __init__(self, service_id, service_attr, on_success, on_error):
        self.service_id = service_id
        self.service_attr = service_attr
        self.on_success = on_success
        self.on_error = on_error

    def invoke(self, *args):
        json = prambanan.window.JSON
        url = "/app/services/%s/%s" % (self.service_id, self.service_attr)
        settings = {
            "data": json.stringify(args),
            "type": "POST",
            "contentType": "application/json; charset=utf-8",
            "dataType": "json",
            "success": self.on_success,
            "error": self.on_error,
            "url": url,
            }
        borobudur.query_el.ajax(settings)

class Loaders(object):

    def __init__(self, page):
        self.loaders = []
        self.page = page
        self.models = page.models
        if prambanan.is_js:
            self.success = underscore.bind(self.success, self)

    def add(self, name, loader):
        self.loaders.append((name, loader))

    def fetch_models(self, *names):
        for name in names:
            self.loaders.append((name, StorageModelLoader()))

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
        name, loader = self.loaders[self.i]
        model = self.models[name]
        loader.load(self.page.app, model, self)



