import os

__author__ = 'h'

def npm_i_venv(*args):
    venv = os.environ["VIRTUAL_ENV"]
    if os.name == "nt":
        venv_bin = os.path.join(venv, "Scripts")
    else:
        venv_bin = venv
    prev_npm_prefix = None
    if "NPM_CONFIG_PREFIX" in os.environ:
        prev_npm_prefix = os.environ["NPM_CONFIG_PREFIX"]
    os.environ["NPM_CONFIG_PREFIX"] = venv_bin
    try:
        for arg in args:
            os.system("npm i -g %s" % arg)
    finally:
        if prev_npm_prefix is not None:
            os.environ["NPM_CONFIG_PREFIX"] = prev_npm_prefix

