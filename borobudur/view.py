from borobudur.model import Collection, Model
import prambanan
import borobudur
import prambanan.jslib.underscore as underscore

delegate_event_splitter = prambanan.JS("/^(\S+)\s*(.*)$/")

def on_element(key):
    def decorate(fn):
        fn._on_element = key
        return fn
    return  decorate

class View(object):
    """
    prambanan:type children l(t(i(str), c(borobudur.view:View)))
    """
    events = {}
    children = []
    template = None

    def __init__(self, app, el, model, el_rendered):
        self.app = app
        self.model = model
        self.el = el
        self.el_query = borobudur.create_el_query(el)
        self.q_el = borobudur.query_el(el)
        self.child_views = []

        self.delegate_events()

        if not el_rendered:
            self.render()

        self.initialize_children(el_rendered)


    def initialize_children(self, el_rendered):
        return
        for child_name, child_type in self.children:
            child_el = self.el_query("[data-child=%s]" % child_name)[0]
            child_model = self.get_child_model(child_name)
            child_view = child_type(child_el, child_model, el_rendered)
            self.child_views.append(child_view)

    def get_child_model(self, child_name):
        return self.model[child_name]

    def render(self):
        self.template.render(self.el, self.model)
        return self

    def remove(self):
        for child_view in self.child_views:
            child_view.remove()
        self.child_views = []
        self.q_el.remove()
        return self

    def delegate_events(self):
        if borobudur.is_server:
            return

        events = prambanan.items(self.events)
        events.extend(self.find_decorated_events())

        self.undelegate_events()

        for key, method in events:
            if not underscore.isFunction(method):
                method = self[method]

            if not method:
                raise Exception('Method "' + events[key] + '" does not exist');

            __, event_name, selector = key.match(delegate_event_splitter)
            method = underscore.bind(method, self)
            event_name += '.delegateEvents' + self.cid
            if selector == '':
                self.q_el.bind(event_name, method)
            else:
                self.q_el.delegate(selector, event_name, method)

    def undelegate_events(self):
        if borobudur.is_server:
            return

        self.q_el.unbind(".delegateEvents"+self.cid)

    def find_decorated_events(self):
        if borobudur.is_server:
            return {}

        results = []
        for attr in underscore.functions(self):
            value = self[attr]
            if value._on_element:
                results.append([value._on_element, value])
        return results


