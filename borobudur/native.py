from pyquery import PyQuery
import colander_patch

def create_el_query(el):
    def dom_query(selector=None):
        if selector is None:
            return PyQuery(el)
        else:
            return PyQuery(el)(selector)
    return dom_query

def query_el(el, selector=None):
    if selector is None:
        return PyQuery(el)
    else:
        return PyQuery(el)(selector)


class Router(object):
    def __init__(self):
        raise Exception()

    def navigate(self, url):
        pass

    def bootstrap(self, env):
        pass

