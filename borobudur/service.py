def service(return_model, return_schema_name):
    def decorate(fn):
        return fn
    return decorate

class Service(object):
    id = None

    def __init__(self, app, callbacks):
        self.app = app
        self.callbacks = callbacks

    def invoke(self, method_name, **kwargs):
        pass
