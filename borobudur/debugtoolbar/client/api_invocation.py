import borobudur
from borobudur.model import Model, Collection
from borobudur.view import View, on_element
from prambanan import get_template, JS
from pramjs.elquery import ElQuery
import pramjs.underscore as underscore

class APIInvocationView(View):
    template = get_template("zpt", ("borobudur", "debugtoolbar/client/api_invocation.pt"))

class APIInvocationsView(View):
    template = get_template("zpt", ("borobudur", "debugtoolbar/client/api_invocations.pt"))
    active_child = None
    q_active_tr = None

    @on_element("tr", "click")
    def show_invocation(self, ev):
        if self.active_child is not None:
            self.q_active_tr.removeClass("pDebugEven")
            self.active_child.remove()
            self.active_child = None
            self.q(".invocation").append(borobudur.query_el("<div></div>"))

        q_el = self.q_active_tr = borobudur.query_el(ev.currentTarget)
        q_el.addClass("pDebugEven")
        cid = q_el.attr("data-key")
        model = self.model.getByCid(cid)
        self.active_child = APIInvocationView(self, self.q(".invocation div")[0], model, False)

def bind_ajax_request(app, col):
    if app:
        return
    jQuery = borobudur.query_el
    prev_ajax = jQuery.ajax
    def ajax(settings):
        if settings.url and settings.url.startswith(app.settings["resource_root"]):
            type = None
            if settings.url.indexOf("/services/") != -1:
                type = "Service"
            elif settings.url.indexOf("/storages/") != -1:
                type = "Storages"
            if type is not None:
                showed_settings = underscore.extend({}, settings)
                del showed_settings["app"]
                model = Model({"status":"loading", "settings":showed_settings, "type": type})
                col.add(model)

                prev_success = settings.success
                def success():
                    model["status"]="success"
                    if prev_success:
                        JS("prev_success.apply(this, arguments)")
                settings.success = success

                prev_error = settings.error
                def error():
                    model["status"]="error"
                    if prev_error:
                        JS("prev_error.apply(this, arguments)")
                settings.error = error
                xhr = prev_ajax(settings)
                model["xhr"] = xhr
                return xhr
            else:
                return prev_ajax(settings)
        else:
            return prev_ajax(settings)
    jQuery.ajax = ajax

def main(app_name, app, assets):
    invocations = Collection()

    q_subtitle = ElQuery("li#pDebugAPIInvocationPanel a small")
    q_subtitle.css({"font-family": "monospace"});
    def updateSubtitle():
        total = {"loading": 0, "success": 0, "error": 0}
        def each_model(model):
            total[model["status"]] += 1;
        invocations.each(each_model)
        q_subtitle.html("E:"+total.error+" | S:"+total.success+" | L:"+total.loading)
    updateSubtitle();

    invocations.on("add", updateSubtitle);
    def on_add(model):
        model.on("change:status", updateSubtitle)
    invocations.on("add", on_add)

    bind_ajax_request(app, invocations)

    parent = {
        "app": app,
        "request": {
            "app": app,
        }
    }

    APIInvocationsView(parent, ElQuery("#pDebugAPIInvocation")[0], invocations, False)

