import translationstring

_ = translationstring.TranslationStringFactory("tstring")

tstring = _("${name} is ${adjective}")
print tstring
tstring = tstring % {'name':'egoz', 'adjective': 'cool'}
print tstring.interpolate()