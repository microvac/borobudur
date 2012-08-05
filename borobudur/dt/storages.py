import borobudur
from borobudur.model import Model
from borobudur.view import View, on_element
from prambanan import get_template
import prambanan

class StorageView(View):
    """
    prambanan:type model_type c(borobudur.model:Model)
    """

    template = get_template("zpt", ("borobudur", "dt/storage.pt"))

    def __init__(self, app, el, model_type_name):
        self.model_type_name = model_type_name
        self.model_type = prambanan.load_module_attr(model_type_name)

        model = Model({"model_type": self.model_type, "model_type_name": model_type_name})
        super(StorageView, self).__init__(self, el, model, False)
        self.show_form()

    @on_element("change", "select.schema-chooser")
    def show_form(self):
        schema_name = self.el_query("select.schema-chooser").val()
        model = self.model_type(schema_name=schema_name)

        q_form_el = self.el_query(".schema-form")
        self.el_query(".schema-form").html("")
        self.render_form(q_form_el[0], model, schema_name)

class StoragesView(View):
    template = None
    active_child = None
    q_active_tr = None

    @on_element("tr", "click")
    def show_storage(self, ev):
        if self.active_child is not None:
            self.q_active_tr.removeClass("pDebugEven")
            self.active_child.remove()
            self.active_child = None
            self.el_query(".storage").append(borobudur.query_el("<div></div>"))

        q_el = self.q_active_tr = borobudur.query_el(ev.currentTarget)
        q_el.addClass("pDebugEven")
        model_type_name = borobudur.query_el("td", q_el).first().html()
        self.active_child = StorageView(self.app, self.el_query(".storage div")[0], model_type_name)

