import os
import logging
import sys

from StringIO import StringIO
from webassets.bundle import Bundle
from webassets import Environment

from prambanan.cmd import generate_modules, create_args, translate_parser, show_parse_error,walk_imports, get_available_modules
from prambanan.output import DirectoryOutputManager
from prambanan.compiler import RUNTIME_MODULES
from prambanan.compiler.utils import ParseError
from prambanan.compiler.manager import PrambananManager
from prambanan.template import get_provider

logger = logging.getLogger("borobudur")

class PrambananModuleBundle(Bundle):

    def __init__(self, abs_dir, dir, manager, pack, target="", **options):
        self.output_manager = DirectoryOutputManager(abs_dir)
        self.dir = dir
        self.manager = manager
        self.pack = pack
        self.target = target

        Bundle.__init__(self, **options)

    def generate(self, args, modules):
        if len(modules) == 0:
            return
        try:
            generate_modules(args, self.output_manager, self.manager, modules)
        except ParseError as e:
            err_out = StringIO()
            show_parse_error(err_out, e)
            err_message = ("%s:\n%s" % (e.message, err_out.getvalue()))
            trace = sys.exc_info()[2]
            raise Exception(err_message), None, trace

    def resolve_contents(self, env=None, force=False):
        env = self._get_env(env)

        if getattr(self, '_resolved_contents', None) is None or force:
            l = []
            args = create_args(translate_parser, target=self.target)
            self.output_manager.new_job()

            self.generate(args, self.pack.modules[:self.pack.templates_position])
            for type in self.pack.templates:
                get_provider(type).compile(args, self.output_manager, self.manager, self.pack.templates[type])
            self.generate(args, self.pack.modules[self.pack.templates_position:])

            if self.output_manager.current_job_files:
                logger.info("generated files: %s" % ",".join(self.output_manager.current_job_files))

            for file in self.output_manager.files:
                l.append((self.dir+file, os.path.join(self.output_manager.dir, file)))

            self._resolved_contents = l
        return self._resolved_contents

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
    modules=None
    templates=None
    templates_position=0

class AppPacks(object):
    app = Pack()
    parts = {}

class PackCalculator(object):

    def __init__(self, cache_file, entry_module):
        self.manager = PrambananManager([], cache_file)
        self.asset_env = Environment("testapp/static", "/static/")
        self.asset_env.config["UGLIFYJS_BIN"] = "uglifyjs.cmd"
        self.asset_env.debug = True
        self.entry_module = entry_module

    def calculate(self, app):
        result = AppPacks()

        available_modules = get_available_modules()

        main_modules, main_templates, main_templates_position = find_modules_and_templates([self.entry_module], available_modules)

        common_modules = None
        for part in app.parts:
            part_pack = Pack()
            part_modules, part_templates, _ = find_modules_and_templates(part.module_names, available_modules)

            part_pack.modules = part_modules
            part_pack.templates = part_templates
            part_pack.templates_position = 0
            result.parts[part.name] = part_pack

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

        for part in app.parts:
            part_pack = result.parts[part.name]
            for name, module in part_pack.modules.items():
                if name in common_modules:
                    del part_pack.modules[name]
            part_pack.modules = part_pack.modules.values()

        for name, module in common_modules.items():
            if name not in main_modules:
                main_modules[name] = module

        result.app.modules = RUNTIME_MODULES + main_modules.values()
        result.app.templates_position = main_templates_position+len(RUNTIME_MODULES)
        result.app.templates = main_templates


        all_modules = dict([(m.modname, m) for m in result.app.modules])
        for name, part_pack in result.parts.items():
            part_modules = dict([(m.modname, m) for m in part_pack.modules])
            all_modules.update(part_modules)

        for key, module in all_modules.items():
            for dep in module.dependencies:
                if dep not in all_modules:
                    print "cannot find dependency: %s for module %s" % (dep , key)

        return result

    def write_pack(self, q_el, name, pack):
        templates_count = 0
        for configs in pack.templates.values():
            templates_count += len(configs)

        if not pack.modules and not templates_count:
            return

        abs_dir = os.path.join("testapp", "static", "b", name)
        if not os.path.exists(abs_dir):
            os.makedirs(abs_dir)
        dir = "b/"+name+"/"
        bundle = PrambananModuleBundle(abs_dir, dir, self.manager, pack, filters="uglifyjs", output="b/"+name+".js")
        for url in bundle.urls(self.asset_env):
            q_el.append("<script type='text/javascript' src='%s'> </script>\n" % url)
