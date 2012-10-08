try: import simplejson as json
except ImportError: import json

from lxml import etree
import os
import logging
import sys

from StringIO import StringIO
from pyquery.pyquery import PyQuery
from webassets.bundle import Bundle
from webassets import Environment
from webassets.updater import SKIP_CACHE
from webassets.version import TimestampVersion
from borobudur.asset import magic
from borobudur.asset.less_import_parser import is_any_modified_after
from borobudur.interfaces import IAssetCalculator

from prambanan.cmd import generate_modules, create_args, translate_parser, show_parse_error,walk_imports, get_available_modules, modules_changed, get_overridden_types
from prambanan.output import DirectoryOutputManager
from prambanan.compiler import RUNTIME_MODULES
from prambanan.compiler.utils import ParseError
from prambanan.compiler.manager import PrambananManager
from pramjs.elquery import ElQuery

logger = logging.getLogger("borobudur")

class SelfCheckingBundle(Bundle):

    def needs_rebuild(self, env):
        raise NotImplementedError()

class PrambananModuleBundle(SelfCheckingBundle):

    def __init__(self, target_dir, manager, pack, overridden_types, target="", **options):
        self.target_dir = target_dir
        self.manager = manager
        self.pack = pack
        self.target = target
        self.overridden_types = overridden_types

        Bundle.__init__(self, **options)


    @property
    def is_container(self):
        return False

    def generate(self, args, output_manager, modules):
        if len(modules) == 0:
            return
        try:
            generate_modules(args, output_manager, self.manager, modules, self.overridden_types)
        except ParseError as e:
            err_out = StringIO()
            show_parse_error(err_out, e)
            err_message = ("%s:\n%s" % (e.message, err_out.getvalue()))
            trace = sys.exc_info()[2]
            raise Exception(err_message), None, trace

    def resolve_contents(self, env=None, force=False):
        env = self._get_env(env)

        abs_dir = os.path.join(env.directory, self.target_dir)
        output_manager = DirectoryOutputManager(abs_dir)

        if not os.path.exists(abs_dir):
            os.makedirs(abs_dir)

        l = []
        args = create_args(translate_parser, target=self.target)
        output_manager.new_job()

        self.generate(args, output_manager, self.pack.modules)

        if output_manager.current_job_files:
            logger.info("generated files: %s" % ",".join(output_manager.current_job_files))

        for file in output_manager.files:
            name = os.path.join(self.target_dir, file).replace("\\", "/")
            result = env.resolver.resolve_source(name)
            l.append((name, result))

        self._resolved_contents = l
        return self._resolved_contents

    def needs_rebuild(self, env):
        abs_dir = os.path.join(env.directory, self.target_dir)
        output_manager = DirectoryOutputManager(abs_dir)
        if modules_changed(output_manager, self.manager, self.pack.modules):
            return SKIP_CACHE
        return False

    """
    def urls(self, env=None, *args, **kwargs):
        results = super(PrambananModuleBundle, self).urls(env, *args, **kwargs)
        for result in results:
            if env.debug:
            """



class Pack(object):
    name=None
    modules=None

class LessBundle(SelfCheckingBundle):

    def __init__(self, *args, **kwargs):
        self._less_cache = {}
        super(LessBundle, self).__init__(*args, **kwargs)

    def needs_rebuild(self, env):
        try:
            resolved_output = self.resolve_output(env)
            o_modified = TimestampVersion.get_timestamp(resolved_output)
        except OSError:
            return SKIP_CACHE
        for content in self.contents:
            if is_any_modified_after(os.path.join(env.directory, content), self._less_cache, o_modified):
                return SKIP_CACHE
        return False

class SimplePackCalculator(object):

    def __init__(self, app_config, app_name, registry):
        available_modules = get_available_modules(app_config.asset_manager.manager, app_config.asset_manager.manager.libraries)
        subscribers =  app_config.get_bootstrap_subscribers(registry)

        module_names = []

        for route, route_handler_id in app_config.routes:
            module = route_handler_id.split(":")[0]
            if not module in module_names:
                module_names.append(module)

        result = Pack()
        result.name = app_name
        available_modules = available_modules

        default_modules = []
        for subscriber in subscribers:
            module_name = subscriber.split(":")[0]
            if module_name not in default_modules:
                default_modules.append(module_name)

        main_modules = walk_imports(default_modules+module_names, available_modules)

        result.modules = RUNTIME_MODULES + main_modules.values()
        self.result = result

        self.pack_map = {}
        for route, route_handler_id in app_config.routes:
            self.pack_map[route_handler_id] = app_name

    def calculate_one(self, page_type_id):
        yield self.result

    def calculate_all(self):
        yield self.result

class MagicPackCalculator(object):
    def __init__(self, splitter, app_config, app_name, registry):
        subscribers =  app_config.get_bootstrap_subscribers(registry)

        default_modules = []
        for subscriber in subscribers:
            module_name = subscriber.split(":")[0]
            if module_name not in default_modules:
                default_modules.append(module_name)

        self.handler_splits = {}

        targets = {}

        for route, route_handler_id in app_config.routes:
            module = route_handler_id.split(":")[0]

            target_name = splitter(module)
            if target_name not in targets:
                targets[target_name] = set(default_modules)

            self.handler_splits[route_handler_id] = target_name
            targets[target_name].add(module)

        available_modules = get_available_modules(app_config.asset_manager.manager, app_config.asset_manager.manager.libraries)

        runtime_pack = Pack()
        runtime_pack.name = "%s.runtime" % app_name
        runtime_pack.modules = RUNTIME_MODULES[:]

        count_result = magic.count(targets, available_modules)

        all_packs = {}
        self.all_results = [runtime_pack]

        for count_pack in count_result.all_packs:
            pack = Pack()
            pack.name = "%s.%d" % (app_name, count_pack.id)
            modules = []
            for module_name in count_pack.items:
                modules.append(available_modules[module_name])
            pack.modules = modules
            all_packs[count_pack.id] = pack
            self.all_results.append(pack)

        self.results = {}
        for split in targets:
            split_results = [runtime_pack]
            for count_pack in count_result.packs[split]:
                split_results.append(all_packs[count_pack.id])
            self.results[split] = split_results

        self.pack_map = {}
        for route, route_handler_id in app_config.routes:
            name = self.handler_splits[route_handler_id]
            self.pack_map[route_handler_id] = [pack.name for pack in self.results[name]]

    def calculate_one(self, page_type_id):
        return self.results[self.handler_splits[page_type_id]]

    def calculate_all(self):
        return self.all_results


class MagicPackCalculatorFactory(object):

    def __init__(self, splitter):
        self.splitter = splitter

    def __call__(self, app_config, app_name, registry):
        return MagicPackCalculator(self.splitter, app_config, app_name, registry)

bootstrap_template = """
    console.log("bootstrapper load time", new Date() - start);
    (function(){
        if (prambanan.has_error)
            return;

        var handler_type_id = %s;

        var app_name = %s;
        var app_root = %s;
        var routes = %s;

        var serialized = %s;

        var loaded_packs = %s;
        var pack_map = %s;
        var pack_urls = %s;

        var settings = %s;
        var subscribers = %s;

        var loaded_assets = %s;

        var load = prambanan.import("prambanan").load_module_attr;

        var app_class = prambanan.import("borobudur").App;
        var app = new app_class(app_root, null, routes, settings);
        app.deserialize(serialized);

        $(function(){
            console.log("document ready time", new Date() - start);

            for(var i = 0; i < subscribers.length; i++){
                load(subscribers[i])(app_name, app, loaded_assets, handler_type_id);
            }
            app.router.bootstrap(loaded_packs, pack_map, pack_urls);
        });
    })();
"""

def to_json(obj):
    return json.dumps(obj)

class AssetManager(object):

    def __init__(self, base_result_dir, base_result_url, is_production=False, result_subdir=None, prambanan_cache_file=None, prambanan_result_subdir=None):

        if prambanan_cache_file is None:
            prambanan_cache_file = ".prambanan.cache"

        if result_subdir is None:
            result_subdir = ".gen"

        if prambanan_result_subdir is None:
            prambanan_result_subdir = ".pram"

        self.env = Environment(base_result_dir, base_result_url)

        self.styles_bundles = {}
        self.packs_bundles = {}

        self.result_subdir = result_subdir
        self.prambanan_result_subdir = prambanan_result_subdir

        self.manager = PrambananManager([], prambanan_cache_file)
        self.overridden_types = get_overridden_types(self.manager, self.manager.libraries)
        self.is_production = is_production

        updater = self.env.updater
        prev_needs_rebuild = updater.needs_rebuild
        def needs_rebuild(bundle, env):
            if isinstance(bundle, SelfCheckingBundle):
                return bundle.needs_rebuild(env)
            return prev_needs_rebuild(bundle, env)
        updater.needs_rebuild = needs_rebuild


    def define_style(self, id, type, output, *contents):
        if type not in ["less", "css"]:
            raise ValueError("type %s is not supported" % type)

        if type == "less":
             self.styles_bundles[id] = LessBundle(*contents, filters="less", output=output)
        else:
             self.styles_bundles[id] = Bundle(*contents, output=output)

    def configure_with_npm(self):
        if os.name == "nt":
            self.env.config["UGLIFYJS_BIN"] = "uglifyjs.cmd"
            self.env.config["LESS_BIN"] = "lessc.cmd"
        else:
            self.env.config["UGLIFYJS_BIN"] = "node_modules/.bin/uglifyjs"
            self.env.config["LESS_BIN"] = "node_modules/.bin/lessc"
        self.env.debug = False


    def write_all(self, request, handler_type_id):
        app_name = request.context.app_name
        document = request.document

        calculator = request.registry.queryUtility(IAssetCalculator, name=app_name)

        subscribers =  request.app_config.get_bootstrap_subscribers(request.registry)
        packs = list(calculator.calculate_one(handler_type_id))
        styles = self.styles_bundles.keys()

        assets = {"js":{}, "css":{}}

        q_body = ElQuery("body", document)
        q_head = ElQuery("head", document)

        q_start = PyQuery(etree.Element("script")).html("start = new Date();")
        q_body.append(q_start)

        for type, name, bundle in self.get_all_bundles(packs, styles):
            if type == "js":
                format = "<script type='text/javascript' src='%s'> </script>\n"
                q_el = q_body
            else:
                format ="<link rel='stylesheet' href='%s' />\n"
                q_el = q_head
            urls = []
            for url in bundle.urls(self.env):
                q_el.append(format % url)
                urls.append(url)
            assets[type][name] = urls

        loaded_packs = [pack.name for pack in packs]
        all_packs = calculator.calculate_all()
        pack_urls = {}
        for name, bundle in self.packs_to_bundles(all_packs):
            pack_urls[name] = []
            for url in bundle.urls(self.env):
                pack_urls[name].append(url)

        bootstrap = bootstrap_template % (
            to_json(handler_type_id),

            to_json(app_name),

            to_json(request.app.root),
            to_json(request.app.routes),
            to_json(request.app.serialize()),

            to_json(loaded_packs),
            to_json(calculator.pack_map),
            to_json(pack_urls),

            to_json(request.app_config.settings),
            to_json(subscribers),

            to_json(assets),
        )
        script = etree.Element("script")
        script.text = etree.CDATA(bootstrap)
        q_body.append(script)

    def get_all_bundles(self, packs, styles):
        for name, bundle in self.packs_to_bundles(packs):
            yield "js", name, bundle

        for name, bundle in self.styles_to_bundles(styles):
            yield "css", name, bundle

    def packs_to_bundles(self, packs):
        for pack in packs:
            if not pack.modules:
                continue

            if pack.name in self.packs_bundles:
                bundle = self.packs_bundles[pack.name]
            else:
                if self.is_production:
                    bundle = PrambananModuleBundle(os.path.join(self.prambanan_result_subdir, pack.name),
                        self.manager, pack, self.overridden_types, output="%s/%s.js"%(self.result_subdir, pack.name), filters="uglifyjs")
                else:
                    bundle = PrambananModuleBundle(os.path.join(self.prambanan_result_subdir, pack.name), self.manager, pack, self.overridden_types)
                self.packs_bundles[pack.name] = bundle
            yield pack.name, bundle

    def styles_to_bundles(self, ids):
        for id in ids:
            yield id, self.styles_bundles[id]
