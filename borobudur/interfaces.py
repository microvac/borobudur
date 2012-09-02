from zope.interface.interface import Interface

__author__ = 'h'

class IAppContext(Interface):

    def get_storage(self, model):
        pass

    def get_connection(self, connection_name):
        pass


