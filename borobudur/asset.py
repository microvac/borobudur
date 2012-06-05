from StringIO import StringIO
import os
import logging
import sys
from webassets.bundle import Bundle
from prambanan.compiler.utils import ParseError

import prambanan.template
from prambanan.cmd import generate_modules, create_args, translate_parser, show_parse_error
from prambanan.output import DirectoryOutputManager

logger = logging.getLogger("borobudur")

class PrambananModuleBundle(Bundle):

    def __init__(self, abs_dir, dir, manager, modules, target="", **options):
        self.output_manager = DirectoryOutputManager(abs_dir)
        self.dir = dir
        self.manager = manager
        self.modules = modules
        self.target = target

        Bundle.__init__(self, **options)

    def resolve_contents(self, env=None, force=False):
        env = self._get_env(env)

        if getattr(self, '_resolved_contents', None) is None or force:
            l = []
            args = create_args(translate_parser, target=self.target)
            self.output_manager.new_job()
            try:
                generate_modules(args, self.output_manager, self.manager, self.modules)
            except ParseError as e:
                err_out = StringIO()
                show_parse_error(err_out, e)
                err_message = ("%s:\n%s" % (e.message, err_out.getvalue()))
                trace = sys.exc_info()[2]
                raise Exception(err_message), None, trace


            templates = {}
            for module in self.modules:
                for type in module.templates:
                    if type not in templates:
                        templates[type] = []
                    for config in module.templates[type]:
                        if config not in templates[type]:
                            templates[type].append(config)

            for type in templates:
                prambanan.template.get_provider(type).compile(args, self.output_manager, self.manager, templates[type])

            if self.output_manager.current_job_files:
                logger.info("generated files: %s" % ",".join(self.output_manager.current_job_files))


            for file in self.output_manager.files:
                if file.startswith("zpt"):
                    l.insert(15, (self.dir+file, os.path.join(self.output_manager.dir, file)))
                else:
                    l.append((self.dir+file, os.path.join(self.output_manager.dir, file)))

            self._resolved_contents = l
        return self._resolved_contents
