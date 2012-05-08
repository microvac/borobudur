"""
unused see Model in borobudur/__init__.py
"""

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
