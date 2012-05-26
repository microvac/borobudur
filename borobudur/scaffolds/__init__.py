from pyramid.scaffolds import PyramidTemplate
import os

__author__ = 'h'

class MongoProjectTemplate(PyramidTemplate):
    _template_dir = 'mongo'
    summary = 'Borobudur with mongo'

    def post(self, command, output_dir, vars): # pragma: no cover
        os.rename(os.path.join(output_dir, "a.gitignore"), os.path.join(output_dir, ".gitignore"))
        return PyramidTemplate.post(self, command, output_dir, vars)

