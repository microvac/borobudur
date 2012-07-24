import colander
import datetime

prev_mapping_serialize = colander.Mapping.serialize
def mapping_serialize(self, node, appstruct):
    if appstruct is None:
        return None
    return prev_mapping_serialize(self, node, appstruct)
colander.Mapping.serialize = mapping_serialize

prev_datetime_deserialize = colander.DateTime.deserialize
def datetime_deserialize(self, node, cstruct):
    if isinstance(cstruct, datetime.datetime):
        return cstruct
    return prev_datetime_deserialize(self, node, cstruct)
colander.DateTime.deserialize = datetime_deserialize

colander.null = None

