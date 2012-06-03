from webassets.bundle import Bundle
from webassets.env import Environment
import pkg_resources
from borobudur.asset import PrambananModuleBundle
from prambanan.compiler import RUNTIME_MODULES, package_to_modules
from prambanan.compiler.manager import PrambananManager

"""
manager = PrambananManager([], "load.conf")
dir = "asset_gen"
abs_dir = "asset_gen"
bundle = PrambananModuleBundle(abs_dir, dir, manager, RUNTIME_MODULES, filters="uglifyjs", output="base.js")

env = Environment("asset_gen", "static/")
env.config["UGLIFYJS_BIN"] = "uglifyjs.cmd"
for url in bundle.urls(env):
    print url
for url in bundle.urls(env):
    print url
"""

for module in package_to_modules("borobudur"):
    for a,b,c in module.files():
        print a
        print b
        print c
        print "----------------"
