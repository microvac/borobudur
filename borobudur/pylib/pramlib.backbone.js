Backbone.setDomLibrary($);
var backboneClasses = [Backbone.Model, Backbone.Collection, Backbone.View];
_.each(backboneClasses, function(cls){
    cls.prototype.__init__ = function(){
        cls.prototype.constructor.apply(this, arguments);
    }
});
prambanan.exports("borobudur.jslib.backbone", Backbone)

