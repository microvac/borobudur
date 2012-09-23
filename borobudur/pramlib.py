from prambanan.compiler import *
from prambanan.compiler.library import PrambananLibrary
from os.path import *
from pkg_resources import resource_filename

pylib_dir = resource_filename("borobudur", "pylib/")
debugtoolbar_dir = resource_filename("borobudur", "debugtoolbar/")

class BorobudurPrambananLibrary(PrambananLibrary):
    overridden_types = {}
    validator_types = ["All", "Function", "Range", "Length", "OneOf"]
    overridden_types["translationstring.TranslationString"] = "Function"

    def __init__(self, *args):
        super(BorobudurPrambananLibrary, self).__init__(*args)
        modules = [
            JavascriptModule(join(pylib_dir, "translationstring.js"), "translationstring"),
            PythonModule(join(pylib_dir, "colander.py"), "colander", self.import_cache),
            PythonModule(join(pylib_dir, "peppercorn.py"), "peppercorn", self.import_cache),
            PythonModule(join(pylib_dir, "bson_objectid.py"), "bson.objectid", self.import_cache),
            JavascriptModule(join(debugtoolbar_dir, "client", "borobudur.debugtoolbar.client.asset.js"), "borobudur.debugtoolbar.client.asset")
            ]
        modules.extend(package_to_modules("borobudur", self.import_cache))
        self.modules = modules

    def get_overridden_types(self):
        return self.overridden_types.copy()

    def get_modules(self):
        return self.modules[:]
