prambanan.load('api_invocation.py', function(prambanan) {
    var APIInvocationView, APIInvocationsView, JS, Model, View, __builtin__, __import__, _class, _m_borobudur, _m_borobudur1, _m_prambanan, _subscript, bind_ajax_request, borobudur, get_template, on_element, print, type;
    __builtin__ = prambanan.import('__builtin__');
    print = __builtin__.print;
    __import__ = __builtin__.__import__;
    type = __builtin__.type;
    _class = prambanan.helpers.class;
    _subscript = prambanan.helpers.subscript;
    borobudur = __import__('borobudur');
    _m_borobudur = __import__('borobudur').model;
    Model = _m_borobudur.Model;
    _m_borobudur1 = __import__('borobudur').view;
    View = _m_borobudur1.View;
    on_element = _m_borobudur1.on_element;
    _m_prambanan = __import__('prambanan');
    get_template = _m_prambanan.get_template;
    JS = _m_prambanan.JS;

    function t_borobudur_dt_api_invocation_APIInvocationView() {
        this.__init__.apply(this, arguments);
    }
    APIInvocationView = _class(t_borobudur_dt_api_invocation_APIInvocationView, [View], function() {
        var template;
        template = get_template("zpt", ["borobudur", "dt/api_invocation.pt"]);
        return [{}, {}, {template: template}]
    });

    function t_borobudur_dt_api_invocation_APIInvocationsView() {
        this.__init__.apply(this, arguments);
    }
    APIInvocationsView = _class(t_borobudur_dt_api_invocation_APIInvocationsView, [View], function() {
        var active_child, show_invocation, template;
        template = get_template("zpt", ["borobudur", "dt/api_invocations.pt"]);
        active_child = null;
        show_invocation = function(ev) {
            var cid, model, q_el, self;
            self = this;
            if (self.active_child != null) {
                self.active_child.remove();
                self.active_child = null;
                self.el_query(".invocation").append(borobudur.query_el("<div></div>"));
            }
            q_el = borobudur.query_el(ev.currentTarget);
            cid = q_el.attr("data-key");
            model = self.model.getByCid(cid);
            self.active_child = new APIInvocationView(self.app, _subscript.l.i(self.el_query(".invocation div"), 0), model, false);
        };
        show_invocation = on_element("click", "tr")(show_invocation);
        return [{show_invocation: show_invocation}, {}, {active_child: active_child,template: template}]
    });
    bind_ajax_request = function(app, col) {
        var ajax, jQuery, prev_ajax;
        jQuery = borobudur.query_el;
        prev_ajax = jQuery.ajax;
        ajax = function(settings) {
            var error, model, prev_error, prev_success, success, type, xhr;
            if (settings.url && settings.url.startswith(app.root + app.api_root)) {
                type = null;
                if (settings.url.indexOf("/services/") !== -1) {
                    type = "Service";
                } else {
                    if (settings.url.indexOf("/storages/") !== -1) {
                        type = "Storages";
                    }
                }
                if (type != null) {
                    model = new Model({status: "loading",settings: settings,type: type});
                    col.add(model);
                    prev_success = settings.success;
                    success = function() {
                        _subscript.s.i(model, "status", "finished");
                        if (prev_success) {
                            prev_success.apply(this, arguments);
                        }
                    };
                    settings.success = success;
                    prev_error = settings.error;
                    error = function() {
                        _subscript.s.i(model, "status", "error");
                        if (prev_error) {
                            prev_error.apply(this, arguments);
                        }
                    };
                    settings.error = error;
                    xhr = prev_ajax(settings);
                    _subscript.s.i(model, "xhr", xhr);
                    print(xhr);
                    return xhr;
                }
            } else {
                return prev_ajax(settings);
            }
        };
        jQuery.ajax = ajax;
    };
    prambanan.exports('borobudur.dt.api_invocation', {APIInvocationView: APIInvocationView,APIInvocationsView: APIInvocationsView,bind_ajax_request: bind_ajax_request});
});