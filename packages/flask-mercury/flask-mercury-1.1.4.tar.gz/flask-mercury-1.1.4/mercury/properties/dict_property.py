"""
Dict property module - defines dictionary attributes.
"""
from simple_mappers import properties
from .base import BaseProperty
from werkzeug import exceptions


class DictProperty(properties.DictProperty, BaseProperty):
    """
    Stores a dict of items
    """

    def inflate(self, value):
        """Returns the value that should be used to fill the object being mapped."""
        try:
            value = super().inflate(value)
            return value
        except TypeError as e:
            raise exceptions.BadRequest(str(e))

    def to_swagger(self, schema: dict):
        """
        Serializes attribute to swagger specification format.
        :param schema: a swagger spec dict.
        :return: the modified swagger spec.
        """
        super(DictProperty, self).to_swagger(schema)
        schema["type"] = "object"
        return schema
