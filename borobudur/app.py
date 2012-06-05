import borobudur
import prambanan
import logging
from prambanan.cmd import get_available_modules, walk_import, walk_imports
from prambanan.compiler import RUNTIME_MODULES
from prambanan.template import get_provider

class LoadFlow(object):
    """
    prambanan:type page_types list class borobudur.page:Page
    """

    def __init__(self, request, page_id):
        self.persist_page = True
        self.request = request

        page_types = []

        current = self.load_page(page_id)
        while current is not None:
            page_types.append(current)
            current = current.parent_page_type

        self.page_types = list(reversed(page_types))


    def load_page(self, page_id):
        splitted_page_id = page_id.split(":")
        module_name = splitted_page_id[0]
        class_name = splitted_page_id[1]

        module = __import__(module_name)
        splitted = module_name.split(".")
        for i in range(1, len(splitted)):
            module = getattr(module, splitted[i])

        return getattr(module, class_name)


    def apply(self):
        app_state = self.request.app_state
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
        page.open()

        app_state = self.request.app_state
        app_state.leaf_page = page
        app_state.active_pages.append(page)

        self.i += 1
        if self.i < len(self.page_types):
            self.next()
        else:
            dom_query = self.request.dom_query
            if page.title is not None:
                dom_query("title").html(page.title)
            if page.keywords is not None:
                dom_query("meta[name='keywords']").attr("content", page.keywords)
            if page.description is not None:
                dom_query("meta[name='description']").attr("content", page.description)

    def next(self):
        page_type = self.page_types[self.i]
        page = page_type(self.request)
        page.prepare()
        self.current = page

        page.load(self)

class AppPart(object):

    def __init__(self, name):
        self.name = name
        self.pages = []
        self.module_names = []

    def add_page(self, route, page_id):
        self.pages.append((route, page_id))
        module = page_id.split(":")[0]
        if not module in self.module_names:
            self.module_names.append(module)

    def get_pyramid_views(self, app):
        results = []
        for route, page_id in self.pages:
            name = app.name+"."+self.name+"."+page_id.replace(":", ".")
            results.append((app.root+route, name, self.make_pyramid_view(app, page_id)))
        return results

    def make_pyramid_view(self, app, page_id):

        def callback(request):
            load_flow = LoadFlow(request, page_id)
            load_flow.apply()

        return borobudur.wrap_pyramid_view(callback, app, self)


class AppState(object):
    leaf_page=True
    active_pages = []

class BaseApp(object):
    def __init__(self, name, root, api_root, entry_module, base_template, parts_config):
        self.name = name
        self.root = root
        self.api_root = api_root
        self.entry_module = entry_module
        self.base_template = base_template

        self.parts=[]

        for part_name, part_config  in prambanan.items(parts_config):
            part = AppPart(part_name)
            for route, page_id in part_config:
                part.add_page(route, page_id)
            self.parts.append(part)

        self.setup()

    def setup(self):
        pass

    def get_pyramid_views(self):
        results = []
        for part in self.parts:
            for item in part.get_pyramid_views(self):
                results.append(item)
        return results

def find_templates(modules):
    results = {}
    for name, module in modules.items():
        for type, configs in module.templates.items():
            if type not in results:
                results[type] = []
            for config in configs:
                if config not in results[type]:
                    results[type].append(config)
    return results

def find_templates_dependencies(templates):
    results = []
    for type in templates:
        try:
            provider = get_provider(type)
        except KeyError:
            print "Cannot find template provider '%s' in module '%s' for templates %s" % (type, templates[type])
            continue
        for dependency in provider.template_dependencies():
            if not dependency in results:
                results.append(dependency)
    return results

def find_modules_and_templates(module_names, available_modules):
    modules = walk_imports(module_names, available_modules)
    templates = find_templates(modules)
    results = walk_imports(find_templates_dependencies(templates), available_modules)
    template_position = len(results)
    for name, module in modules.items():
        if name not in results:
            results[name] = module
    return results, templates, template_position

class ServerApp(BaseApp):
    def setup(self):
        from prambanan.compiler.manager import PrambananManager
        from webassets import Environment
        from .asset import PrambananModuleBundle

        self.prambanan_manager = PrambananManager([], "load.conf")

        available_modules = get_available_modules()

        main_modules, main_templates, main_templates_position = find_modules_and_templates([self.entry_module], available_modules)

        common_modules = None
        for part in self.parts:
            part_modules, part_templates, _ = find_modules_and_templates(part.module_names, available_modules)
            part.modules = part_modules
            part.templates = part_templates
            part.templates_position = 0
            #todo, split template and add them to mainmodule
            if common_modules is None:
                common_modules = part_modules.copy()
                for name, module in common_modules.items():
                    has_template = False
                    for type, configs in module.templates.items():
                        if len(configs) > 0:
                            has_template = True
                    if has_template:
                        del common_modules[name]
            else:
                for name, module in common_modules.items():
                    if name not in part_modules:
                        del common_modules[name]

        for part in self.parts:
            for name, module in part.modules.items():
                if name in common_modules:
                    del part.modules[name]
            part.modules = part.modules.values()

        for name, module in common_modules.items():
            if name not in main_modules:
                main_modules[name] = module

        self.modules = RUNTIME_MODULES + main_modules.values()
        self.templates_position = main_templates_position+len(RUNTIME_MODULES)
        self.templates = main_templates


        all_modules = dict([(m.modname, m) for m in self.modules])
        for part in self.parts:
            part_modules = dict([(m.modname, m) for m in part.modules])
            all_modules.update(part_modules)

        for key, module in all_modules.items():
            for dep in module.dependencies:
                if dep not in all_modules:
                    print "cannot find dependency: %s for module %s" % (dep , key)

        self.asset_env = Environment("testapp/static", "/static/")
        self.asset_env.config["UGLIFYJS_BIN"] = "uglifyjs.cmd"
        self.asset_env.debug = True


    def get_state(self):
        return AppState()

class ClientApp(BaseApp):

    def setup(self):
        self.state = AppState()

    def get_state(self):
        return self.state

App = ServerApp if borobudur.is_server else ClientApp