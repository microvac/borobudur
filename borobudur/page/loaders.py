from borobudur import query_el, is_server
from borobudur.model import Model
from prambanan import window
from pramjs import underscore

__author__ = 'h'

class BaseLoader(object):
    pass

class ServiceLoader(BaseLoader):

    def __init__(self, resourcer, model, service_id, service_attr):
        self.resourcer = resourcer
        self.service_id = service_id
        self.model = model
        self.service_attr = service_attr

    def load(self, callbacks):

        def prev_success(attrs):
            parsed = self.model.parse(attrs)
            if isinstance(self.model, Model):
                self.model.set(parsed)
            else:
                self.model.reset(parsed)
            callbacks.success()

        def fetch_success(attrs):
            def _success():
                prev_success(attrs)
            if isinstance(self.model, Model):
                self.resourcer.fill_children(self.model.__class__, attrs, _success)
            else:
                self.resourcer.fill_col_children(self.model.model, attrs, _success)

        self.resourcer.service(self.service_id, self.service_attr, fetch_success, None).invoke()

class StorageLoader(BaseLoader):

    def __init__(self, resourcer, model):
        self.resourcer = resourcer
        self.model = model

    def load(self, callbacks):
        self.resourcer.fetch(self.model, callbacks.success, callbacks.error)

class ServiceInvoker(object):

    def __init__(self, service_id, service_attr, on_success, on_error):
        self.service_id = service_id
        self.service_attr = service_attr
        self.on_success = on_success
        self.on_error = on_error

    def invoke(self, *args):
        json = window.JSON
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
        query_el.ajax(settings)

class Loaders(object):

    def __init__(self, request):
        self.loaders = []
        self.request = request
        if not is_server:
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

    def error(self):
        pass

    def next(self):
        loader = self.loaders[self.i]
        loader.load(self)
