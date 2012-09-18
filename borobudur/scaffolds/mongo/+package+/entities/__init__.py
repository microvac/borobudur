import borobudur.schema
import borobudur.model.Model

from borobudur.schema import (\
    SchemaNode,SchemaDelete,
    Mapping,Sequence,
    String,Integer,Float,Boolean,Date,DateTime,
    Range,Length,OneOf,All
)

schemas = borobudur.schema.SchemaRepository()

@schemas.root("Phone")
class Phone(Mapping):
    phone = SchemaNode(String(), validator=Length(100))

@schemas.root("User")
class Friend(Mapping):
    name = SchemaNode(String(), validator=Length(100))
    age = SchemaNode(Integer(), validator=Range(1, 100))
    phone = Phone()

@schemas.child("name_only")
class NameOnlyFriend(Friend):
    age=SchemaDelete()
