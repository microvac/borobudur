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

    def __init__(self, abs_dir, dir, manager, modules, templates, templates_position, target="", **options):
        self.output_manager = DirectoryOutputManager(abs_dir)
        self.dir = dir
        self.manager = manager
        self.modules = modules
        self.templates = templates
        self.templates_position = templates_position
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

            self.generate(args, self.modules[:self.templates_position])
            for type in self.templates:
                prambanan.template.get_provider(type).compile(args, self.output_manager, self.manager, self.templates[type])
            self.generate(args, self.modules[self.templates_position:])

            if self.output_manager.current_job_files:
                logger.info("generated files: %s" % ",".join(self.output_manager.current_job_files))

            for file in self.output_manager.files:
                l.append((self.dir+file, os.path.join(self.output_manager.dir, file)))

            self._resolved_contents = l
        return self._resolved_contents
