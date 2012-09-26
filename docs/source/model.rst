Models and Collections - Working with data
**************************
Borobudur models and collections based on Backbone's `Model <http://documentcloud.github.com/backbone/#Model>`_ and `Collection <http://documentcloud.github.com/backbone/#Collection>`_
read those links!.

The difference is almost camelCase backbone's method and attributes is overridden by underscore_casing

Borobudur model also has schema, this is some example Model

    .. pycco:: python

        from borobudur.model import Model

        class Portrait(Model):
            #what attribute should act as id
            #so a model with "_id" as its `id_attribute` will have `model.id == model["_id"]`
            id_attribute = "_id"

            schema = MappingNode(
                _id=ObjectIdNode(),
                date_uploaded=DateTimeNode(),
                filename=StringNode(),

                crop_x=IntegerNode(),
                crop_y=IntegerNode(),
                crop_scale=IntegerNode(),
            )
            model_url = "portraits"

Schemas
=======
Todo


