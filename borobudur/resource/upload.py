import StringIO
import datetime
from bson.objectid import ObjectId
import os
from pyramid.response import FileResponse
from pyramid.security import authenticated_userid

__author__ = 'h'

def make_file_storage_view(storage_type):

    model = storage_type.model

    class View(object):

        def __init__(self, request):
            self.storage = request.resources.get_storage(model)
            self.request = request
            self.schema = model.schema

        def upload(self):
            user_id = authenticated_userid(self.request)
            file = self.request.body_file
            params = self.request.params
            result = self.storage.upload(file, user_id, params, self.schema)
            return {"success":True, "file": result.toJSON()}

        def download(self):
            id = self.request.matchdict["id"]
            type = self.request.matchdict.get("type", self.storage.default_type)

            path = os.path.join(self.storage.directory, id, type)
            response = FileResponse(path, request=self.request)

            item = self.storage.model.with_id(id)
            self.storage.one(item)
            response.content_disposition = 'attachment; filename="%s"' % item["filename"]

            return response

    return View

class FileStorageExposer(object):

    def __call__(self, config, resource_root, factory, storage_type):
        model = storage_type.model
        name = model.__name__
        storage_url = model.model_url

        storage_view = make_file_storage_view(storage_type)

        config.add_route("upload_"+name, resource_root+"uploads/"+storage_url, factory=factory)
        config.add_route("download_"+name, resource_root+"files/"+storage_url+"/{id}", factory=factory)
        config.add_route("typed_download_"+name, resource_root+"files/"+storage_url+"/{id}/{type}", factory=factory)

        config.add_view(storage_view, route_name="upload_"+name, attr="upload", request_method="POST", renderer="json")
        config.add_view(storage_view, route_name="download_"+name, attr="download", request_method="GET")
        config.add_view(storage_view, route_name="typed_download_"+name, attr="download", request_method="GET")

class FileStorage(object):

    model=None
    directory=None
    default_type = "index"

    def __init__(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def upload(self, file, user_id, params, schema):
        file_id = ObjectId()

        os.mkdir(os.path.join(self.directory, str(file_id)))

        file = StringIO.StringIO(file.read())

        for type, sub_file in self.make_sub_files(file):
            self.save_file(sub_file, file_id, type)

        attrs = self.extract_upload_params(file_id, user_id, params)
        model = self.model(attrs)
        self.insert(model)

        return model

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
