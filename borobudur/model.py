class Event():
    def on(self):
        pass
    def trigger(self):
        pass
    def off(self):
        pass

class Model(Event):
    """
    """

    schema = None
    storage = None

    def __init__(self):
        self._attributes = {}

    def save(self):
        pass

    def load(self, appstruct):
        self._attributes.update(appstruct)

    def validate(self):
        self.schema.validate(self._attributes)

    def get(self, name):
        return self._attributes[name]

    def set(self, attrs):
        for attr, value in enumerate(attrs):
            self._attributes[attr] = value
            self.trigger("change:"+attr, self, value)

    def to_appstruct(self):
        return self.toJSON()

    def save(self):
        if self.is_new():
            storage.insert(self.to_appstruct(), self.schema)
        else:
            storage.update(self.to_appstruct(), self.schema)


class Collection(object):
    pass


class UserModel(Model):

    def hash_password(self):
        plain_password = self.get("plain_password")
        salt = util.generate_salt()
        hashed_password = util.hash(plain_password, salt)
        self.set({
            "salt": salt,
            "hash": hashed_password
        })

anu = UserModel()
anu.set({"plain_password": "kakaka"})
anu.hash_password()

class UserModel2(Model):

    def __init__(self):
        self.on("change:plain_password", self.hash_password)

    def hash_password(self):
        plain_password = self.get("plain_password")
        salt = util.generate_salt()
        hashed_password = util.hash(plain_password, salt)
        self.set({
            "salt": salt,
            "hash": hashed_password
        })


anu = UserModel2()
anu.set({"plain_password": "kakaka"})


appstruct_list = storage.list(query, schema)
userColl = UserCollection()
userColl.model_schema = schema
user_collection = UserCollection.load(appstruct_list)
for user in user_collection:
    user.hash_password()
