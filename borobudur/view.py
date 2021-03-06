from prambanan import ctor, load_qname, to_qname, JS, wrap_on_error
from borobudur import is_server, create_el_query
from pramjs.elquery import ElQuery
import pramjs.underscore as underscore

delegate_event_splitter = JS("/^(\S+)\s*(.*)$/")

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

    def __init__(self, parent, el, model):
        self.parent = parent
        self.request = parent.request
        self.app = parent.app
        self.id = self.app.next_count()

        self.model = model
        self.el = el
        self.q = create_el_query(el)
        self.q_el = ElQuery(el)

        self.child_views = []
        self.child_forms = []

        self.renderdict = self.create_renderdict()

        self.delegate_element_events()

        self.initialize()

    def create_renderdict(self):
        renderdict = {"view": self, "request": self.request, "app": self.app}
        return renderdict

    def initialize(self):
        pass

    def render(self):
        self.template.render(self.el, self.model, self.renderdict)
        return self

    def remove(self):
        for name, child_view in self.child_views:
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

        form = ctor(form_type)(self.app)
        self._bind_form(form, name)


        el = form.render(model)
        self.child_forms.append((name, form, model))

        return el

    def _bind_form(self, form, name):
        form_handlers = self.find_decorated_form_handlers(name)
        for config, handler in form_handlers:
            _, event_name, prevent_default = config
            handler = underscore.bind(handler, self)
            def make_handler(h):
                def wrapped(ev):
                    if prevent_default:
                        ev.preventDefault()
                        h(form, form.model, ev)
                return wrap_on_error(wrapped)
            form.add_event_handler(event_name, make_handler(handler))

    def render_child(self, name, model, tag="div"):
        child_view_type = self.children[name]
        if not child_view_type:
            raise KeyError("form with name '%s' doesn't registered to view" % name)

        el = ElQuery("<%s></%s>"% (tag, tag))[0]
        child_view = ctor(child_view_type)(self, el, model)
        child_view.render()
        self.child_views.append((name, child_view))
        return el

    def get_child_model(self, child_name):
        return self.model[child_name]

    def delegate_element_events(self):
        if is_server:
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
            method = wrap_on_error(method)

            event_name += '.delegateEvents' + self.cid

            handler = make_handler(method, prevent_default)

            if selector is None:
                self.q_el.bind(event_name, handler)
            else:
                self.q_el.delegate(selector, event_name, handler)

    def undelegate_element_events(self):
        if is_server:
            return

        self.q_el.unbind(".delegateEvents"+self.cid)

    def find_decorated_element_handlers(self):
        if is_server:
            return {}

        results = []
        for attr in underscore.functions(self):
            value = self[attr]
            if value._on_element:
                for conf in value._on_element:
                    results.append([conf, value])
        return results

    def find_decorated_form_handlers(self, name):
        if is_server:
            return {}

        results = []
        for attr in underscore.functions(self):
            value = self[attr]
            if value._on_form:
                for conf in value._on_form:
                    if conf[0] == name:
                        results.append([conf, value])
        return results

    def deserialize(self, serialized):
        for name, id, qname, model_cid, value in serialized["child_views"]:
            view_el = self.q("[data-view-id='%s']" % id)[0]
            view_type = load_qname(qname)
            view_model = self.app.model_dumper.load(model_cid)
            view = ctor(view_type)(self, view_el, view_model)

            view.deserialize(value)
            view.id = id
            self.child_views.append((name, view))

        for name, formid, qname, model_cid, value in serialized["child_forms"]:
            form_el = self.q("#%s" % formid)[0]
            form_type = load_qname(qname)
            form_model = self.app.model_dumper.load(model_cid)
            form = ctor(form_type)(self.app)

            self._bind_form(form, name)
            form.attach(form_el, form_model, value)
            self.child_forms.append((name, form, form_model))

    def serialize(self):
        results = {"child_views": [], "child_forms": []}

        for name, child_view in self.child_views:
            child_view.q_el.attr("data-view-id", str(child_view.id))
            model_cid = self.app.model_dumper.dump(child_view.model)
            results["child_views"].append((name, child_view.id, to_qname(child_view.__class__), model_cid, child_view.serialize()))

        for name, child_form, model in self.child_forms:
            model_cid = self.app.model_dumper.dump(child_form.model)
            results["child_forms"].append((name, child_form.formid, to_qname(child_form.__class__), model_cid, child_form.dump()))

        return results

