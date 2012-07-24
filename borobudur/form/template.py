import borobudur

def ZPTRendererFactory():
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
    def __call__(template, element, field, **kw):
        vars = dict(kw)
        vars["field"] = field
        return template.render(element, field.model, vars)
    return __call__


default_renderer = ZPTRendererFactory()
