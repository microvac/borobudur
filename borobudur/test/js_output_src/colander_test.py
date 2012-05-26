import colander

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
