from borobudur.storage import Storage

class SqlStorage(Storage):

    def __init__(self, db, collection_name, embedded_path=None):
        pass


userStorage = SqlStorage(DBSession, SqlAlchemyModelClass)
