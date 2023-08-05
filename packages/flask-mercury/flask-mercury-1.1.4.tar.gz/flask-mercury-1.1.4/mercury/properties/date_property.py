# -*- coding: utf-8 -*-
"""
Date property module - defines date attributes.
"""
from simple_mappers import properties
from .base import BaseProperty
from werkzeug import exceptions


class DateProperty(properties.DateProperty, BaseProperty):
    """
    Stores a date
    """

    def inflate(self, value):
        """Returns the value that should be used to fill the object being mapped."""
        try:
            value = super().inflate(value)
            return value
        except TypeError as e:
            raise exceptions.BadRequest(str(e))
        except ValueError as e:
            name = self.mapping_from or self.property_name
            raise exceptions.BadRequest(
                "On Property: {}\n"
                "Value: {}\n"
                "Error: Date property '{}' does not match format '{}'.".format(name, value, name, self.mask)
            )

    def to_swagger(self, schema:dict):
        """
        Serializes attribute to swagger specification format.
        :param schema: a swagger spec dict.
        :return: the modified swagger spec.
        """
        super(DateProperty, self).to_swagger(schema)
        schema["type"] = "string"
        schema["format"] = self.mask
        return schema