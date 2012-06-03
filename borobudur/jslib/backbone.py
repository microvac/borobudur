from prambanan.jslib.underscore import *

class Event(object):
    _callbacks = {}

    def on(self, name, callback):
        if not name in self._callbacks:
            self._callbacks[name] = []
        self._callbacks[name].append(callback)
        return self

    def off(self, name, callback):
        if not name in self._callbacks:
            self._callbacks[name] = []
        callbacks = self._callbacks[name]
        for i in xrange(len(callbacks) - 1, -1, -1):
            if callbacks[i] == callback:
                del callbacks[i]
        return self

    def trigger(self, name, *args):
        if name in self._callbacks:
            for callbacks in self._callbacks[name]:
                callbacks(*args)
        return self

class Model(Event):
    """
    """
    idAttribute = "id"

    def __init__(self, attributes=None, options=None):
        if attributes is None:
            attributes = {}

        self.cid = ""
        self.id = None
        self.attributes = {}
        self.set(attributes, {"silent":True})

    def validate(self, attributes=None):
        pass

    def isValid(self):
        return self.validate(self.toJSON()) is None

    def isNew(self):
        return self.id is None

    def get(self, name):
        if name in self.attributes:
            return self.attributes[name]
        return None

    def set(self, attrs, options=None):
        if options is None:
            options = {}

        changes = {}
        for key in iter(attrs):
            value = attrs[key]
            if value != self.get(key):
                changes[key] = value
                self.attributes[key] = value
                if not options.get("silent"):
                    self.trigger("change:"+key, self, value)

        if len(changes) > 0:
            if not options.get("silent"):
                self.trigger("change", self, changes)

    def clear(self, options=None):
        if options is None:
            options = {}
        self.attributes.clear()
        if "silent" not in options or not options.get("silent"):
            self.trigger("change")

    def clone(self):
        return self.__class__(self.attributes)

    def toJSON(self):
        return self.attributes.copy()

    def fetch(self, options=None):
        raise NotImplementedError()

    def save(self, value=None, options=None):
        raise NotImplementedError()

    def destroy(self, options=None):
        raise NotImplementedError()

    def changedAttributes(self, diff=None):
        raise NotImplementedError()

    def hasChanged(self, attr=None):
        raise NotImplementedError()

    def __eq__(self, other):
        try:
            other_attrs = other.attributes
        except AttributeError:
            return False

        return other_attrs == self.attributes

class Collection(Event):

    def __init__(self, models, options=None)
        if options is None:
            options = {}

        self.model = Model
        if options.get("model") is not None:
            self.model = options.get("model")

        self.models = []
        self.add(models, {"silent": True})

    def add(self, models, options=None):

        if options is None:
            options = {}

        models = list(models) if type(models) is list else [models]

        #not checking for duplicates
        at = options.get("at") if options.get("at") is not None else len(self.models)
        self.models = self.models[:at] + models + self.models[at:] #not quite readable?

        #append all first then trigger
        if options.get("silent"):
            return self

        #Hmm mungkin ada bug? salah baca behaviour?
        index = 0
        for position, model in enumerate(self.models):
            if model.id == models[index].id:
                options["index"] = position
                self.trigger("add", model, self, options)
                index += 1

        return self

    #The comments are mostly from annotated source code in backbonejs.org
    def remove(self, models, options=None):

        if options is None:
            options = {}

        models = list(models) if type(models) is list else [models]

        '''
        for model in models:
            for i in range(len(self.models)):
                if model.id == self.models[i].id:
                    self.models.pop(i)
                    options["index"] = i #index always changing because of pop?
                    if not options.get("silent"):
                        self.trigger("remove", model, self, options)
        '''

        #Bener kek gini ga ya behaviournya? Kekekeke
        indexes = []
        for model in models:
            for i in xrange(len(self.models)):
                if model.id == self.models[i].id:
                    indexes.append(i)

        index = 0
        for model in models:
            for i in xrange(len(self.models)):
                if model.id == self.models[i].id:
                    self.models.pop(i)
                    options["index"] = indexes[index]
                    index += 1
                    if not options.get("silent"):
                        self.trigger("remove", model, self, options)

        return self

    #The JSON representation of a Collection is an array of the models' attributes.
    def toJSON(self):
        return map(lambda model: model.toJSON(), self.models)
        #return map(self.models, lambda model: model.toJSON())
        #raise NotImplementedError()

    #Add a model to the end of the collection.
    def push(self, model, options=None):
        #model = self._prepareModel(model, options)
        self.add(model, options)
        return model

    #Remove a model from the end of the collection.
    def pop(self, options=None):
        model = self.at(len(self.models)-1)
        self.remove(model, options)
        return model

    #Add a model to the beginning of the collection.
    def unshift(self, model, options=None):
        #model = self._prepareModel(model, options)
        if options is None:
            options = {}
        options["at"] = 0
        self.add(model, options)
        return model

    #Remove a model from the beginning of the collection.
    def shift(self):
        model = self.at(0)
        self.remove(model, options)
        return model

    #Get a model from the set by id.
    def get(self, id):
        for model in self.models:
            if model.id == id:
                return model

    #Get the model at the given index.
    def at(self, index):
        return self.models[index]

    #Return models with matching attributes.
    def where(self, attrs):
        if not attrs:
            return []

        def condition(model):
            for key in attrs.keys():
                if attrs[key] != model.get(key):
                    return False
            return True

        return filter(condition, self.models)
        #return filter(self.models, condition)

    #Pluck an attribute from each model in the collection.
    def pluck(self, attr):
        return map(lambda model: model.get(attr), self.models)
        #return map(self.models, lambda model: model.get(attr))

    #No comparator no sort!
    def sort(self):
        raise NotImplementedError()

    def _prepareModel(self, model, options=None):
        raise NotImplementedError()













