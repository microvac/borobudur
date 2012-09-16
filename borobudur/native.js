var $lib = this.prambanan;

if (console && console.error){
    var prevAjax = $.ajax;
    $.ajax = function(settings){
        if(settings && settings.success){
            settings.success = $lib.helpers.wrap_on_error(settings.success);
            return  prevAjax(settings);
        }
        else {
            return prevAjax.call(this, arguments);
        }
    }
}

function create_el_query(el){
    return function(selector){
        if (!_.isUndefined(selector))
            return $(selector, el);
        else
            return $(el);
    }
}

var Router = (function(){

    // Make backbone history inheritable
    Backbone.History.extend = Backbone.Model.extend;


    var History = Backbone.History.extend({
        loadUrl: function(fragmentOverride) {
            var fragment = this.fragment = this.getFragment(fragmentOverride);
            var matched = _.any(this.handlers, function(handler) {
                if (handler.route.regexp.test(fragment)) {
                    handler.callback(fragment);
                    return true;
                }
            });
            return matched;
        }
    });

    var namedParam    = /{(\w+)}/g;
    var splatParam    = /\*\w+/g;
    var escapeRegExp  = /[-[\]()+?.,\\^$|#\s]/g;

    var history = null;

    function t_borobudur_router(){
        this.__init__.apply(this, arguments)
    }

    return Backbone.Router.extend({

        constructor: t_borobudur_router,

        __init__: function(app, options){
            this.app = app
            this.options = {};
            var leafPages = app.get_leaf_pages();
            _.each(leafPages, function(current){
                var route = current[0];
                var page_id = current[1];
                var callback = current[2];
                var name = page_id.replace(":", ".");
                this.route(route, name, callback);
            }, this);
        },

        bootstrap: function(server_state){
            if($lib.on_bootstrap){
                $lib.on_bootstrap();
            }
            this.app_state = {
                leaf_page: null,
                active_pages:  [],
                load_info: server_state.load_info
            };
            history.start({pushState: true, root:this.app.root});
        },

        route: function(route, name, callback) {
            history || (history = new History);
            route = this._routeToRegExp(route);
            if (!callback) callback = this[name];
            history.route(route, _.bind(function(fragment) {
                var document = {
                    el: document,
                    el_query: create_el_query(document),
                    q_el: $(document)
                }
                var callbacks = {"success": function(){}};
                var request = {
                    document: document,
                    matchdict: this._extractParameters(route, fragment),
                    app: this.app
                }

                //save last route, used on refresh
                this.last_route = {
                    request: request,
                    callback: callback,
                    callbacks: callbacks
                }

                callback && callback(request, this.app_state, callbacks);
                this.trigger.call(this, ['route:' + name], request);
                history.trigger('route', this, name, request);
            }, this));
            return this;
        },

        refresh: function(){
            if (this.last_route){
                var last_route = this.last_route;
                var callback = last_route.callback;
                callback && callback(last_route.request, this.app_state, last_route.callbacks);
            }
        },

        navigate: function(fragment, options) {
            if (fragment == "#"){
                return;
            }
            options = options || {trigger: true}
            this.app_state.load_info = false;
            history.navigate(fragment, options);
        },

        _routeToRegExp: function(route) {
            var regexp = new RegExp('^'+route.replace(escapeRegExp, '\\$&')
                .replace(namedParam, '([^\/]+)')
                .replace(splatParam, '(.*?)')+'$');
            var names = [];
            var name;
            while(name = namedParam.exec(route)){
                names.push(name[1])
            }
            return {regexp: regexp, names: names}
        },

        _extractParameters: function(route, fragment) {
            var params =  route.regexp.exec(fragment).slice(1);
            var names = route.names;
            var results = {};
            for (var i = 0; i < params.length; i++){
                results[names[i]] = params[i];
            }
            return results;
        }

    });

})();

