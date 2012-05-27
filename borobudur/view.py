from pyquery import PyQuery as DomQuery

class View(object):
    """
        Comot dari backbone view bukan pyramid view
    """
    def __init__(self, el, model):
        self.model = model
        self.el = el
        self.dom_query = DomQuery(el)

    def render(self):
        self.template.render(self.el, model=self.model)
        return self
