# -*- coding: utf-8 -*-
"""
Package parameters:
-----------------------
 Flask-Mercury integer path parameter type.
"""
from .base import BasePathParameter
from werkzeug.exceptions import BadRequest
import inspect


class Integer(BasePathParameter):
    """
    Integer path parameter type.
    """
    flask_type = "int"

    def __new__(cls, name, value):
        """
        Integer path parameter constructor.
        :param value: a value to be casted to int.
        :return: the value casted to int type
        """
        try:
            value = int(value)
            return value
        except ValueError as e:
            raise BadRequest(
                "Wrong type for the path parameter named '{}'. "
                "It should be an integer but we got '{}'.".format(name, value)
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
        spec['type'] = 'integer'

        return spec

    @classmethod
    def __instancecheck__(cls, instance):
        """
        The magic function called to implement isinstance(..) functionality.
        :param instance: the object being evaluated.
        :return: true if instance should be considered a (direct or indirect) instance of class.
        """
        # builtin int type should be considered a instance of the Integer cls.
        if isinstance(instance, int):
            return True

        if type(instance) is cls:
            return True

        # TODO add parameter name to the message
        raise BadRequest(
            "Wrong type for the path parameter. "
            "It should be an integer but we got '{}'.".format(instance)
        )