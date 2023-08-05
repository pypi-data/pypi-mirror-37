# -*- coding: utf-8 -*-
"""
Module string.py:
-----------------------
 Flask-Mercury string query parameter type.
"""
from werkzeug.exceptions import BadRequest
from .string import String
from uuid import UUID


class Uuid(String):
    """
    String query parameter type.
    """
    def __new__(cls, name, value):
        """
        String query parameter constructor.
        :param value: a value to be casted to str.
        :return: the value casted to str type
        """
        try:
            value = super().__new__(String, name, value)
            value = UUID(value)
            return value
        except ValueError as e:
            raise BadRequest(
                "Wrong type for the query parameter named '{}'. "
                "It should be an UUID but we got '{}'.".format(name, value)
            )

    @classmethod
    def to_swagger(cls, param, doc):
        """
        Swagger spec query parameter serialization function.
        :param param: function parameter pointer.
        :param doc: the parameter doc_string.
        :return: the parameter spec.
        """
        spec = super().to_swagger(param, doc)
        spec['type'] = 'string'
        return spec

    @classmethod
    def __instancecheck__(cls, instance):
        """
        The magic function called to implement isinstance(..) functionality.
        :param instance: the object being evaluated.
        :return: true if instance should be considered a (direct or indirect) instance of class.
        """
        # builtin int type should be considered a instance of the Integer cls.
        if isinstance(instance, UUID):
            return True

        if type(instance) is cls:
            return True

        if isinstance(instance, str):
            try:
                UUID(instance)
                return True
            except ValueError as e:
                # TODO add parameter name to the message
                raise BadRequest(
                    "Wrong type for the query parameter. "
                    "It should be an string but we got '{}'.".format(instance)
                )
        # TODO add parameter name to the message
        raise BadRequest(
            "Wrong type for the query parameter. "
            "It should be an string but we got '{}'.".format(instance)
        )
