import borobudur
from borobudur.model import Model, fetch_children
import prambanan
from pramjs import underscore

__author__ = 'h'

class BaseLoader(object):
    pass

class ServiceLoader(BaseLoader):

    def __init__(self, model, service_id, service_attr):
        self.service_id = service_id
        self.model = model
        self.service_attr = service_attr

    def load(self, request, callbacks):

        def prev_success(attrs):
            parsed = self.model.parse(attrs)
            if isinstance(self.model, Model):
                self.model.set(parsed)
            else:
                self.model.reset(parsed)
            callbacks.success()

        def fetch_success(attrs):
            if isinstance(self.model, Model):
                def _success():
                    prev_success(attrs)
                fetch_children(self.model.__class__, attrs, request.app, _success)
            else:
                count = 0
                def col_success():
                    global count
                    count += 1
                    if count == len(attrs):
                        prev_success(attrs)
                for item_attrs in attrs:
                    fetch_children(self.model.model, item_attrs, request.app, col_success)
                if len(attrs) == 0:
                    prev_success(attrs)

        url = "%s/%s/%s" % (request.app.settings["service_root"], self.service_id, self.service_attr)
        borobudur.query_el.getJSON(url, fetch_success)

class StorageLoader(BaseLoader):

    def __init__(self, model):
        self.model = model

    def load(self, request, callbacks):
        options = {
            "data": self.params,
            }
        self.model.fetch(request.app, callbacks.success, callbacks.error, options)

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

    def __init__(self, request):
        self.loaders = []
        self.request = request
        if prambanan.is_js:
            self.success = underscore.bind(self.success, self)

    def append(self, loader):
        self.loaders.append(loader)

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
        loader.load(self.request, self)
