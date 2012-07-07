class ObjectId(object):
    def __init__(self, _id):
        self._id = _id

    def __str__(self):
        return self._id