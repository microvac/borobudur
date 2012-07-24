import colander
import datetime

prev_mapping_serialize = colander.Mapping.serialize
def mapping_serialize(self, node, appstruct):
    if appstruct is None:
        return None
    return prev_mapping_serialize(self, node, appstruct)
colander.Mapping.serialize = mapping_serialize

colander.null = None

