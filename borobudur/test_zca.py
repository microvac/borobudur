from zope.component import getGlobalSiteManager, adapts
from zope.interface import implements
from zope.interface.interface import Attribute, Interface
from zope.component._api import queryAdapter, getAdapter, queryMultiAdapter, getAdapters, getMultiAdapter

class IConnectionSettings(Interface):
    pass

class MongoConnectionSettings(object):
    implements(IConnectionSettings)

class IStorageContext(Interface):
    pass

class StorageContext(object):
    implements(IStorageContext)

class IStorage(Interface):
    """One one"""
    model = Attribute("model name")

    def one(self):
        """Register object's details"""

class BaseStorage(object):
    implements(IStorage)
    adapts(IStorageContext, IConnectionSettings)

    def __init__(self, context, settings):
        self.context = context
        self.settings = settings

    def one(self):
        print self

class UserStorage(BaseStorage):
    model = "user"

class ProjectStorage(UserStorage):
    model = "project"

settings = MongoConnectionSettings()
context = StorageContext()
gsm = getGlobalSiteManager()

gsm.registerUtility(settings, IConnectionSettings)
gsm.registerAdapter(UserStorage, name="a")
gsm.registerAdapter(ProjectStorage, name="b")

a = getMultiAdapter((context, settings), IStorage, "a")
b = getMultiAdapter((context, settings), IStorage, "a")
print a
print b

print a is b

for name, storage in getAdapters((context,settings), IStorage):
    print storage.one()
