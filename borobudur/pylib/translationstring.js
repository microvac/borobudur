(function(prambanan) {
    var TranslationString, Translator, TranslationStringFactory,  __keyword_default, _get_arg, _init_args, _make_kwargs;

    _init_args = prambanan.helpers.init_args;
    _make_kwargs = prambanan.helpers.make_kwargs;
    _get_arg = prambanan.helpers.get_arg;

    var i_regex =  /\$\{([\s\S]+?)\}/g;
    /**
     * The constructor for a :term:`translation string`.  A translation
     * string is a Unicode-like object that has some extra metadata.
     * * This constructor accepts one required argument named ``msgid``.
     * ``msgid`` must be the :term:`message identifier` for the
     * translation string.  It must be a ``unicode`` object or a ``str``
     * object encoded in the default system encoding.
     * * Optional keyword arguments to this object's constructor include
     * ``domain``, ``default``, and ``mapping``.
     * * ``domain`` represents the :term:`translation domain`.  By default,
     * the translation domain is ``None``, indicating that this
     * translation string is associated with the default translation
     * domain (usually ``messages``).
     * * ``default`` represents an explicit *default text* for this
     * translation string.  Default text appears when the translation
     * string cannot be translated.  Usually, the ``msgid`` of a
     * translation string serves double duty as as its default text.
     * However, using this option you can provide a different default
     * text for this translation string.  This feature is useful when the
     * default of a translation string is too complicated or too long to
     * be used as a message identifier. If ``default`` is provided, it
     * must be a ``unicode`` object or a ``str`` object encoded in the
     * default system encoding (usually means ASCII).  If ``default`` is
     * ``None`` (its default value), the ``msgid`` value used by this
     * translation string will be assumed to be the value of ``default``.
     * * ``mapping``, if supplied, must be a dictionary-like object which
     * represents the replacement values for any :term:`translation
     * string` *replacement marker* instances found within the ``msgid``
     * (or ``default``) value of this translation string.
     * * After a translation string is constructed, it behaves like most
     * other ``unicode`` objects; its ``msgid`` value will be displayed
     * when it is treated like a ``unicode`` object.  Only when its
     * ``ugettext`` method is called will it be translated.
     * * Its default value is available as the ``default`` attribute of the
     * object, its :term:`translation domain` is available as the
     * ``domain`` attribute, and the ``mapping`` is available as the
     * ``mapping`` attribute.  The object otherwise behaves much like a
     * Unicode string.
     */

    function t_translationstring_TranslationString() {}
    TranslationString = function(msgid, domain, __keyword_default, mapping) {
        var _args, self;
        _args = _init_args(arguments);
        __keyword_default = _get_arg(3, "default", _args, null);
        mapping = _get_arg(4, "mapping", _args, null);
        self = new String(msgid);
        if (msgid.constructor === t_translationstring_TranslationString){
            mapping = mapping || msgid.mapping && _.clone(msgid.mapping);
            msgid = msgid.toString();
        }
        self.mapping = mapping;
        self.__mod__ = __mod__;
        self.template = _.template(msgid, undefined, {interpolate: i_regex});
        self.interpolate = interpolate;
        self.constructor = t_translationstring_TranslationString;
        return self;
    };
    /**
     * Create a new TranslationString instance with an updated mapping.
     * This makes it possible to use the standard python %-style string
     * formatting with translatable strings. Only dictionary
     * arguments are supported.
     */
    function __mod__(options) {
        var mapping, self;
        self = this;
        if (self.mapping) {
            mapping = _.clone(self.mapping);
            _.extend(mapping, options);
        } else{
            mapping = _.clone(options);
        }
        return TranslationString(self, _make_kwargs({mapping: mapping}));
    };
    /**
     * Interpolate the value ``translated`` which is assumed to
     * be a Unicode object containing zero or more *replacement
     * markers* (``${foo}`` or ``${bar}``) using the ``mapping``
     * dictionary attached to this instance.  If the ``mapping``
     * dictionary is empty or ``None``, no interpolation is
     * performed.
     * * If ``translated`` is ``None``, interpolation will be performed
     * against the ``default`` value.
     */
    function interpolate (translated) {
        var self = this;
        try{
            return self.template(self.mapping);
        }
        catch($e){
            return self.toString();
        }
    };
    /**
     * Create a factory which will generate translation strings
     * without requiring that each call to the factory be passed a
     * ``domain`` value.  A single argument is passed to this class'
     * constructor: ``domain``.  This value will be used as the
     * ``domain`` values of :class:`translationstring.TranslationString`
     * objects generated by the ``__call__`` of this class.  The
     * ``msgid``, ``mapping``, and ``default`` values provided to the
     * ``__call__`` method of an instance of this class have the meaning
     * as described by the constructor of the
     * :class:`translationstring.TranslationString`
     */
    TranslationStringFactory = function(domain) {
        var create;
        /**
         * Provided a msgid (Unicode object or :term:`translation
         * string`) and optionally a mapping object, and a *default
         * value*, return a :term:`translation string` object.
         */
        create = function(msgid, mapping, __keyword_default) {
            var _args;
            _args = _init_args(arguments);
            mapping = _get_arg(1, "mapping", _args, null);
            __keyword_default = _get_arg(2, "default", _args, null);
            return TranslationString(msgid, _make_kwargs({domain: domain,default:__keyword_default,mapping: mapping}));
        };
        return create;
    };

    Translator = function(){
        var translator = function(tstring){
            return tstring.interpolate();
        }
        return translator;
    }


    prambanan.exports('translationstring', {TranslationString: TranslationString,TranslationStringFactory: TranslationStringFactory, Translator: Translator});
})(prambanan);
