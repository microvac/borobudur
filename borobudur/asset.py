import os
from webassets.bundle import Bundle
from prambanan.cmd import generate_modules, create_args, translate_parser
from prambanan.output import DirectoryOutputManager

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
            generate_modules(args, self.output_manager, self.manager, self.modules)
            for file in self.output_manager.files:
                l.append((self.dir+file, os.path.join(self.output_manager.dir, file)))
            self._resolved_contents = l
        return self._resolved_contents
