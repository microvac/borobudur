from zope.interface.interface import Interface, Attribute

__author__ = 'h'

class IAppConfigurator(Interface):
    pass

class IAssetCalculator(Interface):
    pass

class IAppRoot(Interface):
    pass

class IAppResources(Interface):

    def get_storage(self, model):
        pass


class IBootstrapSubscriber(Interface):
    pass
