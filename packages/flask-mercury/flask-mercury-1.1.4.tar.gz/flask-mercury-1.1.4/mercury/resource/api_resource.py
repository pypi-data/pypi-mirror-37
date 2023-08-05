# -*- coding: utf-8 -*-
"""
Module api_resource.py
---------------------
    The base Api resource implementation.
"""
from .flask import FlaskResource
from .swagger import SwaggerResource


class Resource(FlaskResource, SwaggerResource):
    """
    A Base API endpoint class implementation.
    """
    pass
