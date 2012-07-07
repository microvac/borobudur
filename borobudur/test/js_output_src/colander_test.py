import colander
import datetime
from prambanan import JS

v = colander.Range(1, 3)
v(None, 2)
print "ea"
try:
    v(None, 5)
    print "eww"
except colander.Invalid as e:
    print e.msg
    print e.msg.interpolate()
    print "good"


v = colander.Length(max=10)
v(None, "kutumbaba")
print "good"
try:
    v(None, "kutumbabahulahula")
    print "eww"
except colander.Invalid as e:
    print e.msg
    print e.msg.interpolate()
    print "good"

v = colander.Length(min=3,max=10)
v(None, "kutumbaba")
print "good"
try:
    v(None, "ii")
    print "eww"
except colander.Invalid as e:
    print e.msg
    print e.msg.interpolate()
    print "good"

v = colander.OneOf(["kutumbaba", "hulahula"])
v(None, "kutumbaba")
print "good"
try:
    v(None, "ii")
    print "eww"
except colander.Invalid as e:
    print e.msg
    print e.msg.interpolate()
    print "good"

s = colander.SchemaNode(colander.String())
print isinstance(s.deserialize(3), unicode)

s = colander.SchemaNode(colander.Integer())
print isinstance(s.deserialize("3"), int)

s = colander.SchemaNode(colander.DateTime(default_tzinfo=None))

ser = s.serialize(datetime.datetime(2011, 12, 25))
print ser

des = s.deserialize(ser)
print des



