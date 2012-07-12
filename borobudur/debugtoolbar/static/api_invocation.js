prambanan.on_bootstrap = function(){
    var app = window.app;
    if(!app){
        return;
    }

    var invocations = new (prambanan.import("borobudur.model").Collection)();

    var $subtitle = $("li#pDebugAPIInvocationPanel a small")
    $subtitle.css({"font-family": "monospace"});
    function updateSubtitle(){
        var total = {"loading": 0, "success": 0, "error": 0}
        invocations.each(function(model){
            total[model.get("status")] += 1;
        });
        $subtitle.html("E:"+total.error+" | S:"+total.success+" | L:"+total.loading)
    }
    updateSubtitle();
    invocations.on("add", updateSubtitle);
    invocations.on("add", function(model){
        model.on("change:status", updateSubtitle)
    });


    prambanan.import("borobudur.dt.api_invocation").bind_ajax_request(app, invocations);
    new (prambanan.import("borobudur.dt.api_invocation").APIInvocationsView)(app, $("#pDebugAPIInvocation")[0], invocations, false);
}