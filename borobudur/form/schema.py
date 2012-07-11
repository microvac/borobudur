import colander
import borobudur.schema

from borobudur.form import widget

def get_widget(typ):
    if typ == colander.Mapping:
        return widget.MappingWidget
    elif typ == colander.Sequence:
        return widget.SequenceWidget
    elif typ == colander.String:
        return widget.TextInputWidget
    elif typ == colander.Integer:
        return widget.TextInputWidget
    elif typ == colander.Float:
        return widget.TextInputWidget
    elif typ == colander.Decimal:
        return widget.TextInputWidget
    elif typ == colander.Boolean:
        return widget.CheckboxWidget
    elif typ == colander.Date:
        return widget.DateInputWidget
    elif typ == colander.DateTime:
        return widget.DateTimeInputWidget
    elif typ == borobudur.schema.ObjectId:
        return widget.TextInputWidget
    else:
        raise Exception("cannot find widget")

