import borobudur

class View(object):
    """
        Comot dari backbone view bukan pyramid view
    """
    def __init__(self, el, model):
        self.model = model
        self.el = el
        self.el_query = borobudur.create_dom_query(el)
        self.q_el = self.el_query()

    def render(self):
        cls = str(self.__class__)
        renderer = "server" if borobudur.is_server else "client"
        print "%s rendered in %s" % (cls, renderer)
        self.template.render(self.el, model=self.model)
        return self

    def remove(self):
        self.q_el.remove()
