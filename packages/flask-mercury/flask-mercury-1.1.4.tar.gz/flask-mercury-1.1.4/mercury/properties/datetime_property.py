# -*- coding: utf-8 -*-
"""
Datetime property module - defines datetime attributes.
"""
from simple_mappers import properties
from .base import BaseProperty
from werkzeug import exceptions
import datetime

class DateTimeProperty(properties.DateTimeProperty, BaseProperty):

    def __init__(self, mask=None, **kwargs):
        """
        Datetime property type initialization.
        :param mask: string datetime mask used to parse string dates.
                    or a dict mapping the possible incoming values to its transformed values.

        :param kwargs required: True if the attribute is required.
                         When true and it is not possible to map the attribute from the other object,
                         it raises a value error exception. 
        :param kwargs default: default value or function generator.
        :param kwargs source_name: the name of the attribute in the other object
        """
        if mask is not None:
            self.mask = mask
        else:
            self.mask = "%d/%m/%Y %H:%M"
        
        super(DateTimeProperty, self).__init__(mask, **kwargs)
        
        # default value must be set as string
        if isinstance(self.default,(datetime.datetime, datetime.date,)):
            self.default = self.deflate(self.default)

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
        super(DateTimeProperty,self).to_swagger(schema)
        schema["type"] = "string"
        schema["format"] = self.mask
        return schema