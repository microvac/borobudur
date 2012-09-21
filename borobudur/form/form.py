import borobudur
import borobudur.form.widget as widget
import borobudur.form.field as field

from borobudur.form.compat import (
    string_types,
    text_type,
)
from borobudur.model import Model, ModelRefNode, CollectionRefNode, Collection
from borobudur.schema import MappingNode
import pramjs.underscore as underscore
from prambanan import get_template

button_template = get_template('zpt', ('borobudur', 'form/templates/button.pt'))

class Form(field.Field):
    """
    Field representing an entire form.

    Arguments:

    schema
        A :class:`colander.SchemaNode` object representing a
        schema to be rendered.  Required.

    action
        The form action (inserted into the ``action`` attribute of
        the form's form tag when rendered).  Default: the empty string.

    method
        The form method (inserted into the ``method`` attribute of
        the form's form tag when rendered).  Default: ``POST``.

    buttons
        A sequence of strings or :class:`deform.form.Button`
        objects representing submit buttons that will be placed at
        the bottom of the form.  If any string is passed in the
        sequence, it is converted to
        :class:`deform.form.Button` objects.

    formid
        The identifier for this form.  This value will be used as the
        HTML ``id`` attribute of the rendered HTML form.  It will also
        be used as the value of a hidden form input control
        (``__formid__``) which will be placed in this form's
        rendering.  You should pass a string value for ``formid`` when
        more than one Deform form is placed into a single page and
        both share the same action.  When one of the forms on the page
        is posted, your code will to be able to decide which of those
        forms was posted based on the differing values of
        ``__formid__``.  By default, ``formid`` is ``deform``.

    use_ajax
       If this option is ``True``, the form will use AJAX (actually
       AJAH); when any submit button is clicked, the DOM node related
       to this form will be replaced with the result of the form post
       caused by the submission.  The page will not be reloaded.  This
       feature uses the ``jquery.form`` library ``ajaxForm`` feature
       as per `http://jquery.malsup.com/form/
       <http://jquery.malsup.com/form/>`_.  Default: ``False``.  If
       this option is ``True``, the ``jquery.form.js`` library must be
       loaded in the HTML page which embeds the form.  A copy of it
       exists in the ``static`` directory of the ``deform`` package.

    ajax_options
       A *string* which must represent a JavaScript obejct
       (dictionary) of extra AJAX options as per
       `http://jquery.malsup.com/form/#options-object
       <http://jquery.malsup.com/form/#options-object>`_.  For
       example:

       .. code-block:: python

           '{"success": function (rText, sText, xhr, form) {alert(sText)};}'

       Default options exist even if ``ajax_options`` is not provided.
       By default, ``target`` points at the DOM node representing the
       form and and ``replaceTarget`` is ``true``.

       A successhandler calls the ``deform.processCallbacks`` method
       that will ajaxify the newly written form again.  If you pass
       these values in ``ajax_options``, the defaults will be
       overridden.  If you want to override the success handler, don't
       forget to call ``deform.processCallbacks``, otherwise
       subsequent form submissions won't be submitted via AJAX.

       This option has no effect when ``use_ajax`` is False.

       The default value of ``ajax_options`` is a string
       representation of the empty object.

    The :class:`deform.Form` constructor also accepts all the keyword
    arguments accepted by the :class:`deform.Field` class.  These
    keywords mean the same thing in the context of a Form as they do
    in the context of a Field (a Form is just another kind of Field).
    """
    css_class = 'deform'
    element = None
    buttons = []
    fields = None
    removed_fields = None

    def __init__(self, action='', method='POST',
                 formid='deform', use_ajax=False, ajax_options='{}', **kw):

        schema = self.schema

        if self.fields is not None:
            new_schema = MappingNode()
            for child in schema.children:
                if child.name in self.fields:
                    new_schema.children.append(child)
            schema = new_schema
        elif self.removed_fields is not None:
            new_schema = MappingNode()
            for child in schema.children:
                if child.name not in self.removed_fields:
                    new_schema.children.append(child)
            schema = new_schema

        super(Form, self).__init__(schema, **kw)

        self.action = action
        self.method = method
        self.formid = formid
        self.use_ajax = use_ajax
        self.widget = widget.FormWidget()
        self.event = Model()
        self.initialize()

    def initialize(self):
        pass

    def render(self, model, readonly=False):
        """ Render the field (or form) to HTML using ``appstruct`` as
        a set of default values.  ``appstruct`` is typically a
        dictionary of application values matching the schema used by
        this form, or ``None``.

        Calling this method is the same as calling::

           cstruct = form.schema.serialize(appstruct)
           form.widget.serialize(field, cstruct)

        The ``readonly`` argument causes the rendering to be entirely
        read-only (no input elements at all).

        See the documentation for
        :meth:`colander.SchemaNode.serialize` and
        :meth:`deform.widget.Widget.serialize` .
        """
        self.m = model

        cstruct = self.schema.serialize(model.attributes)

        element = self.serialize(cstruct, readonly=readonly)
        if self.element is not None:
            borobudur.query_el(self.element).replaceWith(element)
        self.element = element

        return element

    def fill_model(self):
        appstruct = self.validate(self.element)
        self.m.set(appstruct)


    def add_button_handler(self, name, handler):
        self.event.on(name, handler)

class Button(object):
    """
    A class representing a form submit button.  A sequence of
    :class:`deform.widget.Button` objects may be passed to the
    constructor of a :class:`deform.form.Form` class when it is
    created to represent the buttons renderered at the bottom of the
    form.

    Arguments:

    name
        The string or unicode value used as the ``name`` of the button
        when rendered (the ``name`` attribute of the button or input
        tag resulting from a form rendering).  Default: ``submit``.

    title
        The value used as the title of the button when rendered (shows
        up in the button inner text).  Default: capitalization of
        whatever is passed as ``name``.  E.g. if ``name`` is passed as
        ``submit``, ``title`` will be ``Submit``.

    type
        The value used as the type of button. The HTML spec supports 
        ``submit``, ``reset`` and ``button``. Default: ``submit``. 

    value
        The value used as the value of the button when rendered (the
        ``value`` attribute of the button or input tag resulting from
        a form rendering).  Default: same as ``name`` passed.

    disabled
        Render the button as disabled if True.
    """
    def __init__(self, name='submit', title=None, type='submit', value=None,
                 css_class="btn",disabled=False):
        if title is None:
            title = name.capitalize()
        if value is None:
            value = name

        self.name = name
        self.css_class = css_class
        self.title = title
        self.type = type
        self.value = value
        self.disabled = disabled

    def render(self, form):
        q_el = borobudur.query_el("<div></div>")
        element = q_el[0]
        button_template.render(element, form.model, {"field":form, "button":self})
        result = q_el.children()[0]
        borobudur.query_el(result).bind("click", self.make_handler(form))
        return result

    def make_handler(self, form):
        def handler(ev):
            form.event.trigger(self.name, ev)
        return handler

