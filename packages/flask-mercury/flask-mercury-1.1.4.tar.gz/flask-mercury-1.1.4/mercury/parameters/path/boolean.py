# -*- coding: utf-8 -*-
"""
Module string.py:
-----------------------
 Flask-Mercury Boolean path parameter type.
"""
from .base import BasePathParameter
from werkzeug.exceptions import BadRequest
import inspect


class Boolean(BasePathParameter):
    """
    Boolean path parameter type.
    """
    flask_type = "string"

    _booleans = ['true', 'false']

    def __new__(cls, name, value):
        """
        Boolean path parameter constructor.
        :param value: a value to be casted to str.
        :return: the value casted to str type
        """
        try:
            value = str(value)
            return value.lower() == 'true'
        except ValueError as e:
            raise BadRequest(
                "Wrong type for the path parameter named '{}'. "
                "It should be a boolean but we got '{}'.".format(name, value)
            )

    @classmethod
    def to_swagger(cls, param, doc):
        """
        Swagger spec path parameter serialization function.
        :param param: function parameter pointer.
        :param doc: the parameter doc_string.
        :return: the parameter spec.
        """
        spec = super().to_swagger(param, doc)
        spec['type'] = 'boolean'

        return spec

    @classmethod
    def __instancecheck__(cls, instance):
        """
        The magic function called to implement isinstance(..) functionality.
        :param instance: the object being evaluated.
        :return: true if instance should be considered a (direct or indirect) instance of class.
        """
        is_bool = str(instance).lower() in cls._booleans
        # builtin int type should be considered a instance of the Integer cls.
        if is_bool:
            return True

        if type(instance) is cls:
            return True

        # TODO add parameter name to the message
        raise BadRequest(
            "Wrong type for the path parameter. "
            "It should be boolean but we got '{}'.".format(instance)
        )