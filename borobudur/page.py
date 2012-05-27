__author__ = 'h'

class Page(object):
    """
        a page manage models and views
    """
    title=None
    keywords=None
    description=None
    parent_page_type = None
    parent_page = None
    loaders = []

    def __init__(self, request):
        self.dom_query = request.dom_query

    def prepare(self, *args):
        print "prepare"
        pass

    def load(self, callbacks):
        print "load"
        callbacks["success"]()

    def open(self):
        print "open"
        pass

    def add_view(self, name, view, model):
        pass

class PagesGroup(object):
    def get_pages(self):
        pass

