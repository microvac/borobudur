import datetime
from bson.objectid import ObjectId
import os
from borobudur.storage import Storage

__author__ = 'h'

class FileStorage(Storage):

    model=None
    directory=None
    default_type = "index"

    def __init__(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def upload(self, file, user_id, params, schema):
        file_id = ObjectId()

        os.mkdir(os.path.join(self.directory, str(file_id)))

        for type, sub_file in self.make_sub_files(file):
            self.save_file(sub_file, file_id, type)

        result = self.extract_upload_params(file_id, user_id, params)
        return self.insert(result, schema)

    def make_sub_files(self, file):
        yield self.default_type, file

    def save_file(self, file, file_id, type):
        file_path = os.path.join(self.directory, str(file_id), type)
        with  open(file_path, 'wb') as output_file:
            while 1:
                data = file.read(2<<16)
                if not data:
                    break
                output_file.write(data)
            output_file.close()

    def extract_upload_params(self, file_id, user_id, params):
        result = {}
        result["_id"] = file_id
        result["filename"] = params["qqfile"]
        result["date_uploaded"] = datetime.datetime.now()
        return result
