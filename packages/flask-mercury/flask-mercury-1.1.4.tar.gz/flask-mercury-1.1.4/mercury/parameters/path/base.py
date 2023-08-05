# -*- coding: utf-8 -*-
"""
Package parameters:
-----------------------
 Flask-Mercury path and Query parameter type definitions.
"""
import inspect
from ..base import BaseParameter
from flask import request


class BasePathParameter(BaseParameter):
    """
    Base path parameter class
    """
    flask_type = ""

    @classmethod
    def to_swagger(cls, param, doc):
        """
        Base path parameter spec serialization function.
        """
        spec = super().to_swagger(param, doc)
        spec["in"] = "path"

        return spec

    @classmethod
    def from_request(cls, name, default=None):
        value = request.view_args.get(name, default)
        if value is not None:
            return cls(name, value)
        else:
            return None
