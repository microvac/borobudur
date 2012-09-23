from pyquery import PyQuery
import colander_patch
import pramjs.elquery

def create_el_query(el):
    def dom_query(selector=None):
        if selector is None:
            return PyQuery(el)
        else:
            return PyQuery(selector, el)
    return dom_query


class Router(object):
    def __init__(self, *args, **kwargs):
        pass

    def navigate(self, url):
        raise Exception()

    def bootstrap(self, env):
        raise Exception()

