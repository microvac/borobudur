import translationstring
from borobudur.model import Collection, Model
import prambanan
import borobudur
import prambanan.jslib.underscore as underscore
from borobudur.form.form import Form, Button
from borobudur.util.pretty_time import pretty_time

delegate_event_splitter = prambanan.JS("/^(\S+)\s*(.*)$/")

def on_element(selector, event_name, prevent_default=True):
    def decorate(fn):
        if not hasattr(fn, "_on_element"):
            fn._on_element = []
        fn._on_element.append((selector, event_name, prevent_default))
        return fn
    return  decorate

def form_button(name, title, css_class="btn"):
    def decorate(fn):
        button = Button(title=title)
        button.css_class=css_class
        fn._form_button = (name, button)
        return fn
    return decorate

class NullTemplate(object):

    def render(self, el, model, vars):
        print "rendering null template"

translator = translationstring.Translator()

view_utils = {
    "pretty_time": lambda time: pretty_time(time, translator)
}

class View(object):
    """
    todorambanan:type children d(i(str), c(borobudur.view:View))
    """
    events = {}
    children = {}
    forms = {}
    template = NullTemplate()

    def __init__(self, parent, el, model, el_rendered):
        self.parent = parent
        self.app = parent.app
        self.model = model
        self.el = el
        self.el_query = borobudur.create_el_query(el)
        self.q_el = borobudur.query_el(el)

        self.child_views = []
        self.child_forms = {}

        self.render_dict = {}
        self.render_dict["view"] = self
        self.render_dict["app"] = self.app
        self.render_dict["utils"] = view_utils
        self.render_dict["translator"] = translator

        self.delegate_events()

        self.initialize()

        if not el_rendered:
            self.render()

    def initialize(self):
        pass

    def render(self):
        self.template.render(self.el, self.model, self.render_dict)
        return self

    def remove(self):
        for child_view in self.child_views:
            child_view.remove()
        self.child_views = []
        self.q_el.remove()
        return self

    def parent_page(self):
        return self.parent.parent_page() if hasattr(self.parent, "parent_page") else self.parent

    def render_form(self, el, model, name):
        schema = self.forms[name]
        form = Form(schema)

        buttons_config = self.find_decorated_buttons(name)
        buttons = []
        for button, handler in buttons_config:
            handler = underscore.bind(handler, self)
            def make_handler(h):
                return prambanan.wrap_on_error(lambda ev: h(ev, model, form, el))
            button.handler = make_handler(handler)
            buttons.append(button)

        form.buttons = buttons

        #todo hack for new_inquiry
        form.el = el

        self.child_forms[name] = form
        form.render(el, model.attributes)

    def render_child(self, el, model, name):
        child_view_type = self.children[name]
        child_view = prambanan.JS("new child_view_type(self, el, model, false)")
        self.child_views.append(child_view)

    def get_child_model(self, child_name):
        return self.model[child_name]


    def delegate_events(self):
        if borobudur.is_server:
            return

        events = prambanan.items(self.events)
        events.extend(self.find_decorated_events())

        self.undelegate_events()

        def make_handler(method, prevent_default):
            def handler(ev):
                if prevent_default:
                    ev.preventDefault()
                method(ev)
            return handler

        for config, method in events:
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
                for conf in value._on_element:
                    results.append([conf, value])
        return results

    def find_decorated_buttons(self, name):
        if borobudur.is_server:
            return {}

        results = []
        for attr in underscore.functions(self):
            value = self[attr]
            if value._form_button:
                form_name, button = value._form_button
                if name == form_name:
                    results.append([button, value])
        return results

