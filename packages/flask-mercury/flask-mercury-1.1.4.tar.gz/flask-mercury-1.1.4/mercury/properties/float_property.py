"""
float property module - defines float attributes.
"""
from simple_mappers import properties
from .base import BaseProperty
from werkzeug import exceptions

class FloatProperty(properties.FloatProperty, BaseProperty):
    """
    Store a floating point value
    """

    def inflate(self, value):
        """Returns the value that should be used to fill the object being mapped."""
        try:
            value = super().inflate(value)
            return value
        except ValueError:
            name = self.mapping_from or self.property_name
            raise exceptions.BadRequest(
                "On property: '{}'.\n"
                "Value: '{}'.\n"
                "Error: Expected float type.".format(name, value)
            )

    def to_swagger(self, schema:dict):
        """
        Serializes attribute to swagger specification format.
        :param schema: a swagger spec dict.
        :return: the modified swagger spec.
        """
        super(FloatProperty, self).to_swagger(schema)
        schema["type"] = "float"
        return schema
