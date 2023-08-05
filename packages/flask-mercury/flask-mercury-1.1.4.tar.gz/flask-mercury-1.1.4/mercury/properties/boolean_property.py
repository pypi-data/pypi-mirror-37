# -*- coding: utf-8 -*-
"""
boolean property module - defines boolean attributes.
"""
from simple_mappers import properties
from .base import BaseProperty


class BooleanProperty(properties.BooleanProperty, BaseProperty):
    """
    Stores a boolean value
    """
    def to_swagger(self, schema:dict):
        """
        Serializes attribute to swagger specification format.
        :param schema: a swagger spec dict.
        :return: the modified swagger spec.
        """
        super(BooleanProperty, self).to_swagger(schema)
        schema["type"] = "boolean"
        return schema
