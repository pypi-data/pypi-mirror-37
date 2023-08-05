# -*- coding: utf-8 -*-
"""
Flask-Mercury
-----------------
Flask-Mercury is a simple lightweight framework to build flask apis
and swagger documentation.
It is empowered by simple_mappers to delivers auto-mapping capabilities.
"""
from .resource import Resource
from .api_model import ApiModel
from . import parameters
from .mercury_app import load

