import json
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
from borobudur.less_import_parser import get_all_less

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

        if getattr(self, '_resolved_contents', None) is None or force:
            l = []
            args = create_args(translate_parser, target=self.target)
            output_manager.new_job()

            self.generate(args, output_manager, self.pack.modules)

            if output_manager.current_job_files:
                logger.info("generated files: %s" % ",".join(output_manager.current_job_files))

            for file in output_manager.files:
                name = os.path.join(self.target_dir, file).replace("\\", "/")
                child = Bundle(name)
                l.append((child, child))

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

    def needs_rebuild(self, env):
        try:
            resolved_output = self.resolve_output(env)
            o_modified = TimestampVersion.get_timestamp(resolved_output)
        except OSError:
            return SKIP_CACHE
        for content in self.contents:
            all_less = get_all_less(os.path.join(env.directory, content))
            for less in all_less:
                o_less = TimestampVersion.get_timestamp(less)
                if o_less > o_modified:
                    return SKIP_CACHE
        return False

bootstrap_template = """
    console.log("bootstrapper load time", new Date() - start);
    $(function(){
        console.log("document ready time", new Date() - start);
        if (prambanan.has_error)
            return;

        var load = prambanan.import("prambanan").load_module_attr;

        var handler_type_id = %s;

        var app_name = %s;
        var app_root = %s;
        var routes = %s;
        var routing_policy_type = load(%s);

        var settings = %s;
        var subscribers = %s;

        var serialized_state = %s;

        var loaded_assets = %s;

        var routing_policy = new routing_policy_type();
        var app_class = prambanan.import("borobudur").App;
        var app = new app_class(app_root, routing_policy, routes, settings);

        for(var i = 0; i &lt; subscribers.length; i++){
            load(subscribers[i])(app_name, app, loaded_assets, handler_type_id);
        }
        app.router.bootstrap(serialized_state);
    });
"""
class SimplePackCalculator(object):
    def __init__(self, app_config):
        self.app_config = app_config
        self.cached_results = {}
        self.available_modules = get_available_modules(app_config.asset_manager.manager, app_config.asset_manager.manager.libraries)

    def __call__(self, app_name, subscribers, page_type_id):
        if page_type_id in self.cached_results:
            yield self.cached_results[page_type_id]
            return

        result = Pack()
        result.name = app_name

        available_modules = self.available_modules

        default_modules = ["borobudur.app"]
        for subscriber in subscribers:
            module_name = subscriber.split(":")[0]
            if module_name not in default_modules:
                default_modules.append(module_name)

        main_modules = walk_imports(default_modules+self.app_config.module_names, available_modules)

        result.modules = RUNTIME_MODULES + main_modules.values()

        self.cached_results[page_type_id] = result

        yield result

def to_json(obj):
    out = StringIO()
    json.dump(obj, out)
    return out.getvalue()

class AssetManager(object):

    def __init__(self, base_result_dir, base_result_url, is_production=False, result_subdir=None, prambanan_cache_file=None, prambanan_result_subdir=None):

        if prambanan_cache_file is None:
            prambanan_cache_file = ".prambanan.cache"

        if result_subdir is None:
            result_subdir = ".gen"

        if prambanan_result_subdir is None:
            prambanan_result_subdir = ".pram"

        self.env = Environment(base_result_dir, base_result_url)
        self.style_assets = {}

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
        self.style_assets[id] = (type, output, contents)

    def configure_with_npm(self):
        if os.name == "nt":
            self.env.config["UGLIFYJS_BIN"] = "uglifyjs.cmd"
            self.env.config["LESS_BIN"] = "lessc.cmd"
        else:
            self.env.config["UGLIFYJS_BIN"] = "node_modules/.bin/uglifyjs"
            self.env.config["LESS_BIN"] = "node_modules/.bin/lessc"
        self.env.debug = False


    def write_all(self, request, handler_type_id, serialized_state):
        app_name = request.context.app_name
        document = request.document

        calculate = request.app_config.asset_calculator

        subscribers =  request.app_config.get_bootstrap_subscribers(request)
        packs = list(calculate(app_name, subscribers, handler_type_id))
        styles = self.style_assets.keys()

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

        routing_policy_qname = "%s:%s" % (request.app.routing_policy.__class__.__module__, request.app.routing_policy.__class__.__name__)

        bootstrap = bootstrap_template % (
            to_json(handler_type_id),

            to_json(app_name),

            to_json(request.app.root),
            to_json(request.app.routes),
            to_json(routing_policy_qname),

            to_json(request.app_config.settings),
            to_json(subscribers),

            to_json(serialized_state),
            to_json(assets),
        )
        q_bootstrap = PyQuery(etree.Element("script")).html(bootstrap)
        q_body.append(q_bootstrap)

    def get_all_bundles(self, packs, styles):
        for name, bundle in self.packs_to_bundles(packs):
            yield "js", name, bundle

        for name, bundle in self.styles_to_bundles(styles):
            yield "css", name, bundle

    def packs_to_bundles(self, packs):
        for pack in packs:
            if not pack.modules:
                continue

            if self.is_production:
                yield pack.name, PrambananModuleBundle(os.path.join(self.prambanan_result_subdir, pack.name),
                    self.manager, pack, self.overridden_types, output="%s/%s.js"%(self.result_subdir, pack.name), filters="uglifyjs")
            else:
                yield pack.name, PrambananModuleBundle(os.path.join(self.prambanan_result_subdir, pack.name), self.manager, pack, self.overridden_types)

    def styles_to_bundles(self, ids):
        for id in ids:
            type, output, contents = self.style_assets[id]
            output = "%s/%s" % (self.result_subdir, output)
            if type == "less":
                yield id, LessBundle(*contents, filters="less", output=output)
            else:
                yield id, Bundle(*contents, output=output)
