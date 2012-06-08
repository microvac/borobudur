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

from prambanan.cmd import generate_modules, create_args, translate_parser, show_parse_error,walk_imports, get_available_modules, modules_changed
from prambanan.output import DirectoryOutputManager
from prambanan.compiler import RUNTIME_MODULES
from prambanan.compiler.utils import ParseError
from prambanan.compiler.manager import PrambananManager
from prambanan.template import get_provider

logger = logging.getLogger("borobudur")

class SelfCheckingBundle(Bundle):

    def needs_rebuild(self, env):
        raise NotImplementedError()


class PrambananModuleBundle(SelfCheckingBundle):

    def __init__(self, target_dir, manager, pack, target="", **options):
        self.target_dir = target_dir
        self.manager = manager
        self.pack = pack
        self.target = target

        Bundle.__init__(self, **options)

    def generate(self, args, output_manager, modules):
        if len(modules) == 0:
            return
        try:
            generate_modules(args, output_manager, self.manager, modules)
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

            self.generate(args, output_manager, self.pack.modules[:self.pack.templates_position])
            for type in self.pack.templates:
                get_provider(type).compile(args, output_manager, self.manager, self.pack.templates[type])
            self.generate(args, output_manager, self.pack.modules[self.pack.templates_position:])

            if output_manager.current_job_files:
                logger.info("generated files: %s" % ",".join(output_manager.current_job_files))

            for file in output_manager.files:
                child = Bundle(os.path.join(self.target_dir, file).replace("\\", "/"))
                l.append((child, child))

            self._resolved_contents = l
        return self._resolved_contents

    def needs_rebuild(self, env):
        abs_dir = os.path.join(env.directory, self.target_dir)
        output_manager = DirectoryOutputManager(abs_dir)
        if modules_changed(output_manager, self.manager, self.pack.modules):
            return SKIP_CACHE
        for type in self.pack.templates:
            if get_provider(type).changed(output_manager, self.manager, self.pack.templates[type]):
                return SKIP_CACHE
        return False


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

class Pack(object):
    name=None
    modules=None
    templates=None
    templates_position=0

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
    $(function(){
        prambanan.import("prambanan").load_module_attr(%s)(%s);
    });
"""
class SimplePackCalculator(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, page_type_id, entry_point):
        entry_module = entry_point.split(":")[0]
        result = Pack()
        result.name = self.app.name

        available_modules = get_available_modules()

        main_modules, main_templates, main_templates_position = find_modules_and_templates([entry_module]+self.app.module_names, available_modules)

        result.modules = RUNTIME_MODULES + main_modules.values()
        result.templates_position = main_templates_position+len(RUNTIME_MODULES)
        result.templates = main_templates

        yield result

class AssetManager(object):

    def __init__(self, base_dir, static_dir, prambanan_dir, prambanan_cache_file):

        self.env = Environment(os.path.join(base_dir, static_dir), "/"+static_dir+"/")
        self.style_assets = {}

        self.target_dir = prambanan_dir
        self.manager = PrambananManager([], prambanan_cache_file)

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

    def write_all(self, load_flow, calculate, entry_point):
        page_type_id = load_flow.page_type_id

        packs = list(calculate(page_type_id, entry_point))
        styles = ["bootstrap"]

        assets = {"js":{}, "css":{}}

        q_body = load_flow.document.el_query("body")
        q_head = load_flow.document.el_query("head")

        for type, name, bundle in self.get_all_bundles(packs, styles):
            if type == "js":
                format = "<script type='text/javascript' src='%s'> </script>\n"
                q_el = q_head
            else:
                format =" <link rel='stylesheet' href='%s' />"
                q_el = q_body
            urls = []
            for url in bundle.urls(self.env):
                q_el.append(format % url)
                urls.append(url)
            assets[type][name] = urls


        state = {
            "current_page": page_type_id,
            "loaded_assets": assets,
            "load_info": {"index": load_flow.i}
        }

        state_out = StringIO()
        entry_point_out = StringIO()
        json.dump(state, state_out)
        json.dump(entry_point, entry_point_out)

        bootstrap = bootstrap_template % (entry_point_out.getvalue(), state_out.getvalue())
        q_bootstrap = PyQuery(etree.Element("script")).html(bootstrap)
        q_body.append(q_bootstrap)

    def get_all_bundles(self, packs, styles):
        for name, bundle in self.packs_to_bundles(packs):
            yield "js", name, bundle

        for name, bundle in self.styles_to_bundles(styles):
            yield "css", name, bundle

    def packs_to_bundles(self, packs):
        for pack in packs:
            templates_count = 0
            for configs in pack.templates.values():
                templates_count += len(configs)

            if not pack.modules and not templates_count:
                continue

            yield pack.name, PrambananModuleBundle(os.path.join(self.target_dir, pack.name), self.manager, pack)

    def styles_to_bundles(self, ids):
        for id in ids:
            type, output, contents = self.style_assets[id]
            if type == "less":
                yield id, LessBundle(*contents, filters="less", output=output)
            else:
                yield id, Bundle(*contents, output=output)
