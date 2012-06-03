import borobudur

class View(object):
    """
        Comot dari backbone view bukan pyramid view
    """
    def __init__(self, el, model):
        self.model = model
        self.el = el
        self.el_query = borobudur.create_dom_query(el)

    def render(self):
        self.template.render(self.el, model=self.model)
        return self
