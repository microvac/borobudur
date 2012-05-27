from prambanan.compiler import *
from prambanan.compiler.provider import PrambananProvider
from os.path import *
from pkg_resources import resource_filename

pylib_dir = resource_filename("borobudur", "pylib/")

class BorobudurPrambananProvider(PrambananProvider):
    modules = {
        "translationstring": JavascriptModule(join(pylib_dir, "translationstring.js")),
        "colander": PythonModule(join(pylib_dir, "colander.py"), "colander", ["datetime", "translationstring"]),
    }
    overridden_types = {}
    validator_types = ["All", "Function", "Range", "Length", "OneOf"]
    for type in validator_types:
        qname = "colander."+type
        overridden_types[qname] = "Function"
    overridden_types["translationstring.TranslationString"] = "Function"

    def get_overridden_types(self):
        return self.overridden_types.copy()

    def get_modules(self):
        return self.modules.copy()
