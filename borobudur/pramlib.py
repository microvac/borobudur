from prambanan.compiler import *
from prambanan.compiler.library import PrambananLibrary
from os.path import *
from pkg_resources import resource_filename

pylib_dir = resource_filename("borobudur", "pylib/")
jslib_dir = resource_filename("borobudur", "jslib/")

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
            JavascriptModule([join(pylib_dir, "pramlib.backbone.js")], "borobudur.jslib.backbone"),
            JavascriptModule([join(pylib_dir, "fileuploader.js"), join(pylib_dir, "pramlib.qq.js")], "borobudur.jslib.qq"),
            PythonModule(join(jslib_dir, "bootstrap", "modal.py"), "borobudur.jslib.bootstrap.modal", self.import_cache, [join(pylib_dir, "bootstrap", "bootstrap-modal.js"), join(pylib_dir, "bootstrap", "bootstrap-modal-gallery.js")]),
            PythonModule(join(jslib_dir, "bootstrap", "datepicker.py"), "borobudur.jslib.bootstrap.datepicker", self.import_cache, [join(pylib_dir, "bootstrap", "bootstrap-datepicker.js")]),
            ]
        modules.extend(package_to_modules("borobudur", self.import_cache))
        for m in modules:
            if m.modname == "borobudur":
                m.js_deps.append(join(pylib_dir, "jquery.min.js"))
                break
        self.modules = modules

    def get_overridden_types(self):
        return self.overridden_types.copy()

    def get_modules(self):
        return self.modules[:]
