# -*- coding: utf-8 -*-
"""
Package parameters:
-----------------------
 Flask-Mercury base parameter type definition.
"""
from werkzeug.exceptions import BadRequest
from flask import request
from .base import BaseParameter
import io


class FileParameter(BaseParameter):
    """
    A File parameter definition.
    """
    flask_type = "file"

    def __new__(cls, name, value):
        """
        A file parameter constructor.
        :param value: a value to be casted to int.
        :return: the value casted to int type
        """

        if isinstance(value, io.IOBase):
            return value
        else:
            raise BadRequest(
                "Bad file received '{}'. "
                "We could not get the file stream, instead we got '{}'."
                "".format(name, value)
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
        spec['type'] = 'file'
        spec['format'] = 'binary'

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