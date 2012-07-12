$(function(){
    var app = window.app;
    if(!app){
        return;
    }

    var model = new (prambanan.import("borobudur.model").Model)({});
    new (prambanan.import("borobudur.dt.storages").StoragesView)(app, $("#pDebugStorages")[0], model, true);
});