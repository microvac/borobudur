import os
import sys
import pyramid.settings
import shutil

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )
from borobudur.app import App
from borobudur.asset import AssetManager, SimplePackCalculator
from roma.common import app_settings


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini clean|build")' % (cmd, cmd))
    sys.exit(1)

def create_app(settings):
    return App(app_settings)

def get_manager(settings):
    asset_manager = AssetManager(
        base_dir="roma",
        static_dir="static",
        result_dir="gen",
        prambanan_dir=".p",
        prambanan_cache_file=".prambanan.cache",
        is_production=pyramid.settings.asbool(settings.get("borobudur.asset.is_production")),
    )
    if os.name == "nt":
        asset_manager.env.config["UGLIFYJS_BIN"] = "uglifyjs.cmd"
        asset_manager.env.config["LESS_BIN"] = "lessc.cmd"
    else:
        asset_manager.env.config["UGLIFYJS_BIN"] = "node_modules/.bin/uglifyjs"
        asset_manager.env.config["LESS_BIN"] = "node_modules/.bin/lessc"
    asset_manager.env.debug = False

    asset_manager.define_style("bootstrap", "less", "bootstrap.css", "less/bootstrap.less")
    asset_manager.define_style("fileuploader", "css", "fileuploader.css", "css/fileuploader.css")
    asset_manager.define_style("bootstrap-responsive", "less", "gen/bootstrap-responsive.css", "less/responsive.less")
    return asset_manager

def rm_all(folder):
    print "cleaning %s" % folder
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        else:
            shutil.rmtree(file_path)

def main(argv=sys.argv):
    if len(argv) != 3:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    manager = get_manager(settings)
    entry_point = "roma.client:main"
    if argv[2] == "clean":
        rm_all(manager.full_result_dir)
        rm_all(manager.env.cache.directory)
    elif argv[2] == "build":
        app = create_app(settings)
        calculator = SimplePackCalculator(app, manager.manager)
        page = app_settings["pages"][0][1]
        packs = calculator(page, entry_point)
        for _, __, bundle in manager.get_all_bundles(packs, manager.style_assets.keys()):
            print "generating %s" % bundle.output
            for url in bundle.urls(manager.env):
                print "%s generated" % url
    else:
        usage(argv)

