import os
import sys
import shutil

from pyramid.paster import (
    setup_logging,
    bootstrap)
from borobudur.interfaces import IApp


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini clean|build")' % (cmd, cmd))
    sys.exit(1)

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
    env = bootstrap(config_uri)
    for app_name, app in env["app"].registry.getUtilitiesFor(IApp):
        manager = app.asset_manager
        if argv[2] == "clean":
            rm_all(manager.full_result_dir)
            rm_all(manager.env.cache.directory)
        elif argv[2] == "build":
            page = app.pages[0][1]
            packs = app.asset_calculator(app_name, page)
            for _, __, bundle in manager.get_all_bundles(packs, manager.style_assets.keys()):
                print "generating %s" % bundle.output
                for url in bundle.urls(manager.env):
                    print "%s generated" % url
        else:
            usage(argv)

