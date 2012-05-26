class TranslationString(text_type):
    """
    The constructor for a :term:`translation string`.  A translation
    string is a Unicode-like object that has some extra metadata.

    This constructor accepts one required argument named ``msgid``.
    ``msgid`` must be the :term:`message identifier` for the
    translation string.  It must be a ``unicode`` object or a ``str``
    object encoded in the default system encoding.

    Optional keyword arguments to this object's constructor include
    ``domain``, ``default``, and ``mapping``.

    ``domain`` represents the :term:`translation domain`.  By default,
    the translation domain is ``None``, indicating that this
    translation string is associated with the default translation
    domain (usually ``messages``).

    ``default`` represents an explicit *default text* for this
    translation string.  Default text appears when the translation
    string cannot be translated.  Usually, the ``msgid`` of a
    translation string serves double duty as as its default text.
    However, using this option you can provide a different default
    text for this translation string.  This feature is useful when the
    default of a translation string is too complicated or too long to
    be used as a message identifier. If ``default`` is provided, it
    must be a ``unicode`` object or a ``str`` object encoded in the
    default system encoding (usually means ASCII).  If ``default`` is
    ``None`` (its default value), the ``msgid`` value used by this
    translation string will be assumed to be the value of ``default``.

    ``mapping``, if supplied, must be a dictionary-like object which
    represents the replacement values for any :term:`translation
    string` *replacement marker* instances found within the ``msgid``
    (or ``default``) value of this translation string.

    After a translation string is constructed, it behaves like most
    other ``unicode`` objects; its ``msgid`` value will be displayed
    when it is treated like a ``unicode`` object.  Only when its
    ``ugettext`` method is called will it be translated.

    Its default value is available as the ``default`` attribute of the
    object, its :term:`translation domain` is available as the
    ``domain`` attribute, and the ``mapping`` is available as the
    ``mapping`` attribute.  The object otherwise behaves much like a
    Unicode string.
    """
    __slots__ = ('domain', 'default', 'mapping')

    def __new__(self, msgid, domain=None, default=None, mapping=None):

        # NB: this function should never never lose the *original
        # identity* of a non-``None`` but empty ``default`` value
        # provided to it.  See the comment in ChameleonTranslate.

        self = text_type.__new__(self, msgid)
        if isinstance(msgid, self.__class__):
            domain = domain or msgid.domain and msgid.domain[:]
            default = default or msgid.default and msgid.default[:]
            mapping = mapping or msgid.mapping and msgid.mapping.copy()
            msgid = text_type(msgid)
        self.domain = domain
        if default is None:
            default = text_type(msgid)
        self.default = default
        self.mapping = mapping
        return self

    def __mod__(self, options):
        """Create a new TranslationString instance with an updated mapping.
        This makes it possible to use the standard python %-style string
        formatting with translatable strings. Only dictionary
        arguments are supported.
        """
        if not isinstance(options, dict):
            raise ValueError(
                    'Can only interpolate translationstring '
                    'with dictionaries.')
        if self.mapping:
            mapping = self.mapping.copy()
            mapping.update(options)
        else:
            mapping = options.copy()
        return TranslationString(self, mapping=mapping)

    def interpolate(self, translated=None):
        """ Interpolate the value ``translated`` which is assumed to
        be a Unicode object containing zero or more *replacement
        markers* (``${foo}`` or ``${bar}``) using the ``mapping``
        dictionary attached to this instance.  If the ``mapping``
        dictionary is empty or ``None``, no interpolation is
        performed.

        If ``translated`` is ``None``, interpolation will be performed
        against the ``default`` value.
        """
        if translated is None:
            translated = self.default

        # NB: this function should never never lose the *original
        # identity* of a non-``None`` but empty ``default`` value it
        # is provided.  If (translated == default) , it should return the
        # *orignal* default, not a derivation.  See the comment below in
        # ChameleonTranslate.

        if self.mapping and translated:
            def replace(match):
                whole, param1, param2 = match.groups()
                return text_type(self.mapping.get(param1 or param2, whole))
            translated = _interp_regex.sub(replace, translated)

        return translated

    def __reduce__(self):
        return self.__class__, self.__getstate__()

    def __getstate__(self):
        return text_type(self), self.domain, self.default, self.mapping

def TranslationStringFactory(domain):
    """ Create a factory which will generate translation strings
    without requiring that each call to the factory be passed a
    ``domain`` value.  A single argument is passed to this class'
    constructor: ``domain``.  This value will be used as the
    ``domain`` values of :class:`translationstring.TranslationString`
    objects generated by the ``__call__`` of this class.  The
    ``msgid``, ``mapping``, and ``default`` values provided to the
    ``__call__`` method of an instance of this class have the meaning
    as described by the constructor of the
    :class:`translationstring.TranslationString`"""
    def create(msgid, mapping=None, default=None):
        """ Provided a msgid (Unicode object or :term:`translation
        string`) and optionally a mapping object, and a *default
        value*, return a :term:`translation string` object."""
        return TranslationString(msgid, domain=domain, default=default,
                                 mapping=mapping)
    return create
