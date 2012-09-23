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

            _.each(app.routes, function(current){
                var route = current[0];
                var page_id = current[1];
                var name = page_id.replace(":", ".");
                this.route(route, name, page_id);
            }, this);
        },

        bootstrap: function(serialized_state){
            if($lib.on_bootstrap){
                $lib.on_bootstrap();
            }
            this.app_state = this.app.routing_policy.create_state();
            this.app_state.load(serialized_state);

            this.request = {app: this.app, document: document};
            history.start({pushState: true, root:this.app.root});
        },

        route: function(route, name, handler_id) {
            history || (history = new History);
            route = this._routeToRegExp(route);
            var routing_policy = this.app.routing_policy;

            history.route(route, _.bind(function(fragment) {
                this.app.model_caches = {}
                var callbacks = {"success": function(){}};
                this.request.matchdict = this._extractParameters(route, fragment);

                //save last route, used on refresh
                this.last_route = {
                    request: this.request,
                    handler_id: handler_id,
                    callbacks: callbacks
                }

                routing_policy.apply(this.request, handler_id, this.app_state, callbacks);
                this.trigger.call(this, ['route:' + name], this.request);
                history.trigger('route', this, name, this.request);
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

