from prambanan.compiler import *
from prambanan.compiler.provider import PrambananProvider
from os.path import *
from pkg_resources import resource_filename

pylib_dir = resource_filename("borobudur", "pylib/")

class BorobudurPrambananLibrary(PrambananProvider):
    overridden_types = {}
    validator_types = ["All", "Function", "Range", "Length", "OneOf"]
    overridden_types["translationstring.TranslationString"] = "Function"
    modules = [
        JavascriptModule(join(pylib_dir, "translationstring.js"), "translationstring"),
        PythonModule(join(pylib_dir, "colander.py"), "colander"),
        JavascriptModule([join(pylib_dir, "backbone.js"), join(pylib_dir, "pramlib.backbone.js")], "borobudur.jslib.backbone"),
    ]
    modules.extend(package_to_modules("borobudur"))
    for m in modules:
        if m.modname == "borobudur":
            m.js_deps.append(join(pylib_dir, "zepto.js"))
            break

    def get_overridden_types(self):
        return self.overridden_types.copy()

    def get_modules(self):
        return self.modules[:]
