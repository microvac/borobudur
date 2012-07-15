import prambanan.jslib.underscore as underscore

import borobudur
import prambanan

class BaseLoader(object):
    pass

class ServiceModelLoader(BaseLoader):

    def __init__(self, service_id, service_attr):
        self.service_id = service_id
        self.service_attr = service_attr

    def load(self, model, callbacks):
        def success(attrs):
            model.set(attrs)
            callbacks.success()

        url = "/app/services/%s/%s" % (self.service_id, self.service_attr)
        borobudur.query_el.getJSON(url, success)

class StorageModelLoader(BaseLoader):
    def load(self, model, callbacks):
        options = {
            "data": self.params,
            "success":callbacks.success,
            "error": callbacks.error
        }
        model.fetch(options)

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

class StopLoadException(Exception):
    pass

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
        model.storage_root = self.page.storage_root
        loader.load(model, self)


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


class LoadFlow(object):
    """
    prambanan:type page_types l(c(borobudur.page:Page))
    """

    def __init__(self, app, page_type_id, app_state, matchdict):
        page_type = prambanan.load_module_attr(page_type_id)

        self.app = app
        self.page_type_id = page_type_id
        self.app_state = app_state
        self.matchdict = matchdict

        loaded_index = -1 if not app_state.load_info else app_state.load_info["index"]
        self.load_from = loaded_index + 1

        page_types = []

        persist_page = find_LCA(app_state.leaf_page, page_type)

        current = persist_page
        while current is not None:
            if current.will_reload(matchdict):
                persist_page = current.parent_page
            current = current.parent_page

        current = page_type
        while current is not None and (persist_page is None or current != persist_page.__class__):
            page_types.append(current)
            current = current.parent_page_type

        self.persist_page = persist_page
        self.page_types = list(reversed(page_types))

    def apply(self, document, callbacks):
        self.document = document
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
            page = page_type(self.app, self.matchdict, self.document, page_el_rendered)
            page.parent_page = self.app_state.leaf_page

            self.current = page

            loaders = Loaders(page)
            page.prepare(loaders)
            loaders.apply(self)

    def finish(self):
        page = self.current
        el_query = self.document.el_query
        if page is not None:
            if page.title is not None:
                el_query("title").html(page.title)
            if page.keywords is not None:
                el_query("meta[name='keywords']").attr("content", page.keywords)
            if page.description is not None:
                el_query("meta[name='description']").attr("content", page.description)
        self.callbacks["success"](self)

class AppPart(object):

    def __init__(self, name):
        self.name = name

class App(object):
    def __init__(self, settings):
        self.name = settings["name"];
        self.root = settings["root"];
        self.api_root = settings["api_root"];
        self.pages = []
        self.module_names = []

        for route, page_type_id  in settings["pages"]:
            self.add_page(route, page_type_id)

    def add_page(self, route, page_type_id):
        self.pages.append((route, page_type_id))
        module = page_type_id.split(":")[0]
        if not module in self.module_names:
            self.module_names.append(module)

    def get_leaf_pages(self):
        results = []
        for route, page_type_id in self.pages:
            results.append((route, page_type_id, self.make_callback(page_type_id)))
        return results

    def make_callback(self, page_type_id):

        def callback(app_state, matchdict, document, callbacks):
            load_flow = LoadFlow(self, page_type_id, app_state, matchdict)
            load_flow.apply(document, callbacks)

        return callback
