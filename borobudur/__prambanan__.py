from prambanan.compiler import *
from prambanan.compiler.provider import PrambananProvider
from os.path import *
from pkg_resources import resource_filename

pylib_dir = resource_filename("borobudur", "pylib/")

class BorobudurPrambananProvider(PrambananProvider):
    overridden_types = {}
    validator_types = ["All", "Function", "Range", "Length", "OneOf"]
    overridden_types["translationstring.TranslationString"] = "Function"
    modules = [
        JavascriptModule(join(pylib_dir, "translationstring.js"), "translationstring"),
        PythonModule(join(pylib_dir, "colander.py"), "colander")
    ]
    modules.extend(package_to_modules("borobudur"))

    def get_overridden_types(self):
        return self.overridden_types.copy()

    def get_modules(self):
        return self.modules[:]
