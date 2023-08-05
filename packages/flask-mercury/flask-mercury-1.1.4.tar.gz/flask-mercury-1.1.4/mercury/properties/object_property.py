"""
Object property module - defines Object attributes.
"""
from simple_mappers import properties
from .base import BaseProperty


class ObjectProperty(properties.ObjectProperty, BaseProperty):
    """
    Stores a object property.
    """

    def to_swagger(self, schema:dict):
        """
        Serializes attribute to swagger specification format.
        :param schema: a swagger spec dict.
        :return: the modified swagger spec.
        """
        super(ObjectProperty, self).to_swagger(schema)
        if self.obj_type is not None:
            schema["$ref"] = "#/definitions/{}".format(self.obj_type.__name__)
        else:
            schema["type"] = "object"
            # schema["properties"] = {}
        return schema
