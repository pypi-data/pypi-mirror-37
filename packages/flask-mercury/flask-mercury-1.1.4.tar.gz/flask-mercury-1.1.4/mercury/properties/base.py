# -*- coding: utf-8 -*-
"""
Module base.py
----------------- 
    Defines a base class property.
    Properties are used to give meta-data to class attributes.
"""
from simple_mappers import properties
from simple_mappers.properties import mapping_error
from werkzeug import exceptions


class BaseProperty(properties.BaseProperty):
    """
    Base class for object properties
    """

    def __init__(
            self, required=False, default=None,
            mapping_name=None, cascade=True, validate_func=None,
            description=None, example=None, **kwargs
    ):
        """
        A Base class property definition. 
        :param required: True if the attribute is required.
                         When true and it is not possible to map the attribute from the other object,
                         it raises a value error exception. 
        :param default: default value or function generator.
        :param mapping_name: the name of the attribute in the other object
        :param cascade: when true mappers try to map the the property from the other object properties.
        :param validate_func: a function used to validate attribute values.
        :param description: a property description sting.
        :param example: a value example for the attribute.
        :param kwargs:
        """
        super().__init__(
            required=required,
            default=default,
            mapping_name=mapping_name,
            cascade=cascade,
            validade_func=validate_func,
            **kwargs
        )

        self.description = None
        if description is not None:
            self.description = description
        self.example = example

    def inflate(self, value):
        """
        returns default or value. 
        """
        # applies the validation function
        try:
            return super().inflate(value)
        except mapping_error.InvalidAttributeValueError as e:
            raise exceptions.BadRequest(str(e))
        except mapping_error.RequiredPropertyError as e:
            raise exceptions.BadRequest(str(e))

    def to_swagger(self, schema:dict):
        """
        Serializes attribute to swagger specification format.
        :param schema: a swagger spec dict.
        :return: the modified swagger spec.
        """
        if self.required:
            if "required" not in schema:
                schema["required"] = list()
            name = self.property_name if not self.mapping_from else self.mapping_from
            schema["required"].append(name)
        if self.default is not None:
            schema["default"] = self.default

        if self.description is not None:
            schema["description"] = self.description
        return schema


class ChoiceProperty(properties.ChoiceProperty, BaseProperty):
    """
    Defines a base choosable base property.
    """

    def inflate(self, value):
        """Returns the value that should be used to fill the object being mapped."""
        try:
            value = super().inflate(value)
            return value
        except mapping_error.InvalidAttributeValueError as e:
            raise exceptions.BadRequest(str(e))

    def deflate(self, value, **kwargs):
        """Returns the value that should be used to send to the object being mapped."""
        try:
            value = super().deflate(value, **kwargs)
            return value
        except ValueError as e:
            raise exceptions.BadRequest(str(e))

    def to_swagger(self, schema:dict):
        """
        Serializes attribute to swagger specification format.
        :param schema: a swagger spec dict.
        :return: the modified swagger spec.
        """
        super(ChoiceProperty, self).to_swagger(schema)
        schema["type"] = "string"
        if self.choices is not None:
            schema["enum"] = self.choices
        return schema


class NormalProperty(properties.NormalProperty, BaseProperty):
    """
    Base class for normalized properties.
    """
    def to_swagger(self, schema:dict):
        """
        Serializes attribute to swagger specification format.
        :param schema: a swagger spec dict.
        :return: the modified swagger spec.
        """
        super(NormalProperty, self).to_swagger(schema)
        schema["type"] = "string"
        return schema
