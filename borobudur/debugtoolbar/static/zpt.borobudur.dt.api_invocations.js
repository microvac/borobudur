prambanan.load('dt/api_invocations.pt', function(prambanan) {
    var __builtin__, __filename, __import__, __marker, _convert_str, _iter, _lookup_attr, _m_prambanan, _m_prambanan1, _m_prambanan2, _remove_el, object, render;
    __builtin__ = prambanan.import('__builtin__');
    __import__ = __builtin__.__import__;
    object = __builtin__.object;
    _iter = prambanan.helpers.iter;
    _m_prambanan = __import__('prambanan').zpt;
    _remove_el = _m_prambanan.remove_el;
    _m_prambanan1 = __import__('prambanan').zpt;
    _lookup_attr = _m_prambanan1.lookup_attr;
    _m_prambanan2 = __import__('prambanan').zpt;
    _convert_str = _m_prambanan2.convert_str;
    __marker = new object();
    __filename = "g:\\workspace\\python\\virtualenvs\\cashweb\\borobudur\\borobudur\\dt\\api_invocations.pt";
    render = function(__stack_174471768, __model_174471768, econtext, rcontext) {
        var __collection, __el_map_178805392, __i18n_domain, __on_add_178805392, __on_remove_178805392, __on_reset_178805392, __stack_178805392, _i, _len, _list, model;
        __i18n_domain = null;
        __stack_174471768.u("div");
        __stack_174471768.a("class", "container-fluid");
        __stack_174471768.t("\n    ");
        __stack_174471768.u("div");
        __stack_174471768.a("class", "row-fluid");
        __stack_174471768.t("\n        ");
        __stack_174471768.u("div");
        __stack_174471768.a("class", "span4");
        __stack_174471768.t("\n            ");
        __stack_174471768.u("h2");
        __stack_174471768.t("API Invocations");
        __stack_174471768.o();
        __stack_174471768.t("\n            ");
        __stack_174471768.u("table");
        __stack_174471768.a("class", "table table-condensed table-bordered table-striped");
        __stack_174471768.t("\n                ");
        __stack_174471768.u("thead");
        __stack_174471768.t("\n                    ");
        __stack_174471768.u("th");
        __stack_174471768.t("Type");
        __stack_174471768.o();
        __stack_174471768.t("\n                    ");
        __stack_174471768.u("th");
        __stack_174471768.t("URL");
        __stack_174471768.o();
        __stack_174471768.t("\n                    ");
        __stack_174471768.u("th");
        __stack_174471768.t("Status");
        __stack_174471768.o();
        __stack_174471768.t("\n                ");
        __stack_174471768.o();
        __stack_174471768.t("\n                ");
        __stack_174471768.u("tbody");
        __stack_174471768.t("\n                    ");
        __stack_178805392 = __stack_174471768.capture_for_repeat();
        __el_map_178805392 = {};
        __on_add_178805392 = function(__model_invocation_178805392) {
            var __on_change_178806400, __stack_178806400;
            __stack_178805392.t("\n                        ");
            __stack_178806400 = __stack_178805392.capture();
            __on_change_178806400 = function() {
                var __attr_data_key, __content_37156944;
                __stack_178806400.replay("tr");
                __attr_data_key = _convert_str(_lookup_attr(__model_invocation_178805392, "cid", "__model_invocation.cid", __filename));
                __stack_178806400.a("data-key", __attr_data_key);
                __stack_178806400.t("\n                            ");
                __stack_178806400.u("td");
                __content_37156944 = _convert_str(_lookup_attr(__model_invocation_178805392, "type", "__model_invocation.type", __filename));
                __stack_178806400.t(__content_37156944);
                __stack_178806400.o();
                __stack_178806400.t("\n                            ");
                __stack_178806400.u("td");
                __content_37156944 = _convert_str(_lookup_attr(_lookup_attr(__model_invocation_178805392, "settings", "__model_invocation.settings", __filename), "url", "__model_invocation.settings.url", __filename));
                __stack_178806400.t(__content_37156944);
                __stack_178806400.o();
                __stack_178806400.t("\n                            ");
                __stack_178806400.u("td");
                __content_37156944 = _convert_str(_lookup_attr(__model_invocation_178805392, "status", "__model_invocation.status", __filename));
                __stack_178806400.t(__content_37156944);
                __stack_178806400.o();
                __stack_178806400.t("\n                        ");
                __stack_178806400.o();
            };
            __model_174471768.on("change", __on_change_178806400);
            __on_change_178806400();
            __stack_178805392.t("\n                    ");
            __el_map_178805392[__model_invocation_178805392.cid] = __stack_178805392.repeat_el;
        };
        __on_remove_178805392 = function(__model_invocation_178805392) {
            _remove_el(__el_map_178805392[__model_invocation_178805392.cid]);
            delete __el_map_178805392[__model_invocation_178805392.cid];
        };
        __on_reset_178805392 = function(models) {
            var _i, _i1, _len, _len1, _list, _list1, cid, model;
            _list = _iter(__el_map_178805392);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                cid = _list[_i];
                _remove_el(__el_map_178805392[cid]);
            }
            __el_map_178805392 = {};
            if (models) {
                _list1 = _iter(models);
                for (_i1 = 0, _len1 = _list1.length; _i1 < _len1; _i1++) {
                    model = _list1[_i1];
                    __on_add_178805392(model);
                }
            }
        };
        __collection = __model_174471768;
        _list = _iter(__collection);
        for (_i = 0, _len = _list.length; _i < _len; _i++) {
            model = _list[_i];
            __on_add_178805392(model);
        }
        __collection.on("add", __on_add_178805392);
        __collection.on("remove", __on_remove_178805392);
        __collection.on("reset", __on_reset_178805392);
        __stack_174471768.t("\n                ");
        __stack_174471768.o();
        __stack_174471768.t("\n            ");
        __stack_174471768.o();
        __stack_174471768.t("\n        ");
        __stack_174471768.o();
        __stack_174471768.t("\n        ");
        __stack_174471768.u("div");
        __stack_174471768.a("class", "span8 invocation");
        __stack_174471768.t("\n            ");
        __stack_174471768.u("div");
        __stack_174471768.o();
        __stack_174471768.t("\n        ");
        __stack_174471768.o();
        __stack_174471768.t("\n    ");
        __stack_174471768.o();
        __stack_174471768.t("\n");
        __stack_174471768.o();
        __stack_174471768.t("\n");
    };
    prambanan.templates.zpt.export('borobudur', 'dt/api_invocations.pt', render);
});