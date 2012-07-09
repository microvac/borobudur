from pyramid.scaffolds import PyramidTemplate
import os

class MongoProjectTemplate(PyramidTemplate):
    _template_dir = 'mongo'
    summary = 'Borobudur with mongo'

    def post(self, command, output_dir, vars): # pragma: no cover
        os.rename(os.path.join(output_dir, "a.gitignore"), os.path.join(output_dir, ".gitignore"))
        os.rename(os.path.join(output_dir, vars["package"], "a.pramignore"), os.path.join(output_dir, vars["package"], ".pramignore"))
        return PyramidTemplate.post(self, command, output_dir, vars)

