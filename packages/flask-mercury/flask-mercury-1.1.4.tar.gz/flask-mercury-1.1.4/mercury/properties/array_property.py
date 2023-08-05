# -*- coding: utf-8 -*-
"""
Module array_property.py
----------------------------
    Defines array attributes.
"""
from simple_mappers import properties
import collections
from .base import BaseProperty
from .object_property import ObjectProperty
from werkzeug import exceptions
from ..api_model import ApiModel


class ArrayProperty(properties.ArrayProperty, BaseProperty):
    """
    Stores a list of items.
    """
    def inflate(self, value):
        """Returns the value that should be used to fill the object being mapped."""
        try:
            return super().inflate(value)
        except TypeError as e:
            raise exceptions.BadRequest(str(e))

    def deflate(self, value, **kwargs):
        """Returns the value that should be used to send to the object being mapped."""
        try:
            return super().deflate(value, **kwargs)
        except TypeError as e:
            raise exceptions.BadRequest(str(e))

    def to_swagger(self, schema:dict):
        """
        Swagger serialization function.
        :param schema: a dictionary used to represent and store the schema.
        """
        super(ArrayProperty, self).to_swagger(schema)
        schema["type"] = "array"
        if self.itens_type is not None:
            if isinstance(self.itens_type, type) and issubclass(self.itens_type, (ApiModel,)):
                schema["items"] = {
                    "$ref": "#/definitions/{}".format(self.itens_type.__name__)
                }
            else:
                schema["items"] = self.itens_type.to_swagger(dict())
        return schema