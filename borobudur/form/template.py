import borobudur
from prambanan import get_template

class ZPTRenderer(object):
    """
    Construct a Chameleon ZPT :term:`renderer`.

    The resulting renderer callable accepts a template name *without*
    the ``.pt`` file extension and a set of keyword` values.

    **Arguments**

    search_path
      A sequence of strings representing fully qualified filesystem
      directories containing Deform Chameleon template sources.  The
      order in which the directories are listed within ``search_path``
      is the order in which they are checked for the template provided
      to the renderer.

    auto_reload
       If true, automatically reload templates when they change (slows
       rendering).  Default: ``True``.

    debug
       If true, show nicer tracebacks during Chameleon template rendering
       errors (slows rendering).  Default: ``True``.

    encoding
       The encoding that the on-disk representation of the templates
       and all non-ASCII values passed to the template should be
       expected to adhere to.  Default: ``utf-8``.

    translator
       A translation function used for internationalization when the
       ``i18n:translate`` attribute syntax is used in the Chameleon
       template is active or a
       :class:`translationstring.TranslationString` is encountered
       during output.  It must accept a translation string and return
       an interpolated translation.  Default: ``None`` (no translation
       performed).
    """
    def __init__(self, template_map):
        self.template_map = template_map

    def render(self, template_name, field, **kw):
        if template_name not in self.template_map:
            raise ValueError("there is no template for '%s' in template_map map " % template_name)

        template = self.template_map[template_name]

        q_el = borobudur.query_el("<div></div>")
        element = q_el[0]

        vars = dict(kw)
        vars["field"] = field
        template.render(element, field.event, vars)
        return q_el.children()[0]

    def set_templates(self, d):
        for key in d:
            self.template_map[key] = d[key]
        return self

    def clone(self):
        template_map_copy = {}
        for key in self.template_map:
            template_map_copy[key] = self.template_map[key]
        return self.__class__(template_map_copy)


default_template_map = {
    "form": get_template("zpt", ("borobudur", "form/templates/form.pt")),
    "mapping": get_template("zpt", ("borobudur", "form/templates/mapping.pt")),
    "mapping_item": get_template("zpt", ("borobudur", "form/templates/mapping_item.pt")),
    "sequence": get_template("zpt", ("borobudur", "form/templates/sequence.pt")),
    "sequence_item": get_template("zpt", ("borobudur", "form/templates/sequence_item.pt")),
    "textinput": get_template("zpt", ("borobudur", "form/templates/textinput.pt")),
    "password": get_template("zpt", ("borobudur", "form/templates/password.pt")),
    "checked_password": get_template("zpt", ("borobudur", "form/templates/checked_password.pt")),
    "hidden": get_template("zpt", ("borobudur", "form/templates/hidden.pt")),
    "checkbox": get_template("zpt", ("borobudur", "form/templates/checkbox.pt")),
    "dateinput": get_template("zpt", ("borobudur", "form/templates/dateinput.pt")),
    "datetimeinput": get_template("zpt", ("borobudur", "form/templates/datetimeinput.pt")),
}

default_renderer = ZPTRenderer(default_template_map)