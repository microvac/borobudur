import prambanan
import borobudur
import pramjs.underscore as underscore

delegate_event_splitter = prambanan.JS("/^(\S+)\s*(.*)$/")

def on_element(selector, event_name, prevent_default=True):
    def decorate(fn):
        if not hasattr(fn, "_on_element"):
            fn._on_element = []
        fn._on_element.append((selector, event_name, prevent_default))
        return fn
    return  decorate

def on_form(selector, button_name, prevent_default=True):
    def decorate(fn):
        if not hasattr(fn, "_on_form"):
            fn._on_form = []
        fn._on_form.append((selector, button_name, prevent_default))
        return fn
    return  decorate


class Form(object):
    """
    Interface for form
    """

    def __init__(self):
        pass

    def render(self, model):
        pass

    def add_event_handler(self, event_name, event_handler):
        pass

class NullTemplate(object):

    def render(self, el, model, vars):
        print "rendering null template"

class View(object):
    """
    todorambanan:type children d(i(str), c(borobudur.view:View))
    """
    children = {}
    forms = {}
    template = NullTemplate()

    def __init__(self, parent, el, model, el_rendered):
        self.parent = parent
        self.request = parent.request
        self.app = parent.app

        self.model = model
        self.el = el
        self.el_query = borobudur.create_el_query(el)
        self.q_el = borobudur.query_el(el)

        self.child_views = []
        self.child_forms = {}

        self.renderdict = self.create_renderdict()

        self.delegate_element_events()

        self.initialize()

        if not el_rendered:
            self.render()

    def create_renderdict(self):
        renderdict = {}
        renderdict["view"] = self
        renderdict["request"] = self.request
        renderdict["app"] = self.app
        return renderdict

    def initialize(self):
        pass

    def render(self):
        self.template.render(self.el, self.model, self.renderdict)
        return self

    def remove(self):
        for child_view in self.child_views:
            child_view.remove()
        self.child_views = []
        self.q_el.remove()
        return self

    def parent_page(self):
        return self.parent.parent_page() if hasattr(self.parent, "parent_page") else self.parent

    def render_form(self, name, model):
        form_type = self.forms[name]
        if not form_type:
            raise KeyError("form with name '%s' doesn't registered to view" % name)

        if borobudur.is_server:
            form = form_type()
        else:
            form = prambanan.JS("new form_type()")

        form_handlers = self.find_decorated_form_handlers(name)
        for config, handler in form_handlers:
            _, event_name, prevent_default = config
            handler = underscore.bind(handler, self)
            def make_handler(h):
                def wrapped(ev):
                    if prevent_default:
                        ev.preventDefault()
                        h(ev, form.model, form, form.element)
                return prambanan.wrap_on_error(wrapped)
            form.add_event_handler(event_name, make_handler(handler))

        el = form.render(model)
        self.child_forms[name] = form

        form.el = el

        return el

    def render_child(self, name, model, tag="div"):
        child_view_type = self.children[name]
        if not child_view_type:
            raise KeyError("form with name '%s' doesn't registered to view" % name)

        el = borobudur.query_el("<%s></%s>"% (tag, tag))[0]
        child_view = prambanan.JS("new child_view_type(self, el, model, false)")
        self.child_views.append(child_view)
        return el

    def get_child_model(self, child_name):
        return self.model[child_name]

    def delegate_element_events(self):
        if borobudur.is_server:
            return

        self.undelegate_element_events()

        element_handlers = self.find_decorated_element_handlers()

        def make_handler(method, prevent_default):
            def handler(ev):
                if prevent_default:
                    ev.preventDefault()
                method(ev)
            return handler

        for config, method in element_handlers:
            selector, event_name, prevent_default = config

            if not underscore.isFunction(method):
                if not self[method]:
                    raise Exception('Method "' + method + '" does not exist');
                method = self[method]

            method = underscore.bind(method, self)
            method = prambanan.wrap_on_error(method)

            event_name += '.delegateEvents' + self.cid

            handler = make_handler(method, prevent_default)

            if selector is None:
                self.q_el.bind(event_name, handler)
            else:
                self.q_el.delegate(selector, event_name, handler)

    def undelegate_element_events(self):
        if borobudur.is_server:
            return

        self.q_el.unbind(".delegateEvents"+self.cid)

    def find_decorated_element_handlers(self):
        if borobudur.is_server:
            return {}

        results = []
        for attr in underscore.functions(self):
            value = self[attr]
            if value._on_element:
                for conf in value._on_element:
                    results.append([conf, value])
        return results

    def find_decorated_form_handlers(self, name):
        if borobudur.is_server:
            return {}

        results = []
        for attr in underscore.functions(self):
            value = self[attr]
            if value._on_form:
                for conf in value._on_form:
                    if conf[0] == name:
                        results.append([conf, value])
        return results

