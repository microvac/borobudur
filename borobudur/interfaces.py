from zope.interface.interface import Interface, Attribute

__author__ = 'h'

class IApp(Interface):
    pass

class IAppConfigurator(Interface):
    pass

class IAppResources(Interface):

    def get_storage(self, model):
        pass


class IBootstrapSubscriber(Interface):
    pass
