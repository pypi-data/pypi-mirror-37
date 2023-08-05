# -*- coding: utf-8 -*-
"""
Package resource
---------------------
Api resource provides api resource definition and implementation
for flask-mercury.
"""

_verbs = ["get", "post", "put", "delete", "head", "patch"]

from .meta_resource import BaseResource
from .api_resource import Resource
