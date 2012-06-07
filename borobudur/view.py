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
    events = {}
    def __init__(self, el, model):
        self.model = model
        self.el = el
        self.el_query = borobudur.create_el_query(el)
        self.q_el = borobudur.query_el(el)

        self.delegate_events()

    def render(self):
        cls = str(self.__class__)
        renderer = "server" if borobudur.is_server else "client"
        print "%s rendered in %s" % (cls, renderer)
        self.template.render(self.el, model=self.model)
        return self

    def remove(self):
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

