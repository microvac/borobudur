from lxml import etree
from pyramid.response import Response
from pyquery import PyQuery
from borobudur.asset import PrambananModuleBundle
import os

def create_dom_query(el):
    def dom_query(selector=None):
        if selector is None:
            return PyQuery(el)
        else:
            return PyQuery(el)(selector)
    return dom_query


class Router(object):
    def __init__(self):
        raise Exception()

    def navigate(self, url):
        pass

    def bootstrap(self, env):
        pass

