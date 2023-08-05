# -*- coding: utf-8 -*-
"""
Module mercury_app.py
---------------------
  MercuryApp provides swagger endpoints and initialization functions to the Flask-Mercury framework.
"""
import json
import flask
from simple_mappers import JsonObject
import inspect
import importlib
import pkgutil
from .resource import Resource
from .api_model import ApiModel
from flask import Flask


class MercuryApp(object):
    """
    Swagger ui endpoints.
    """
    def __init__(self, app: Flask, api_title, schemes, api_doc):
        self.app = app
        # swagger specification object initialization
        swagger_spec = dict(
            definitions=dict(),
            # initialize the paths part
            paths=dict(),
            tags=list(),
            swagger="2.0",
            info=JsonObject(),
            basePath='/' + api_title,
            schemes=schemes
        )
        self.spec = JsonObject(**swagger_spec)
        self.spec.info.description = api_doc.summary
        self.spec.info.version = api_doc.version
        # self.spec.info.version = "1.0.0"
        self.spec.info.title = api_title
        # TODO
        # swagger_spec.info.termsOfService = ""
        # swagger_spec.info.contact = {"email":""}
        # swagger_spec.info.license = {"name": doc.license, "url":""}

        self.index_path = "index.html"
        self.api_title = api_title

    def auto_discover_spec(self, api_module):
        def selector(member):
            """Filters members that are either an ApiModel implementation or a Resource implementation"""
            if inspect.isclass(member):
                if issubclass(member, ApiModel) and member is not ApiModel:
                    return True
                elif issubclass(member, Resource) and member is not Resource:
                    return True
            return False

        # searches for 'mercury.Resource' implementation recursively on the API_ROOT package
        for finder, name, is_pack in pkgutil.walk_packages(api_module.__path__, api_module.__name__ + "."):
            if is_pack:
                # skip packages
                continue
            # import the module if it has not been imported yet
            mod = importlib.import_module(name)
            # filter mercury members
            mod_members = inspect.getmembers(
                mod,
                predicate=selector
            )
            # for each member
            for member_name, member_obj in mod_members:
                if issubclass(member_obj, Resource):
                    spec = member_obj.to_swagger()
                    self.add_resource_spec(spec)
                    member_obj.register(self.app, self.api_title)
                elif issubclass(member_obj, ApiModel):
                    member_obj.to_swagger(self.spec)

    def add_resource_spec(self, resource_spec):
        for path, path_spec in resource_spec.paths.items():
            if path in self.spec.paths:
                for verb, verb_spec in path_spec.items():
                    if verb not in self.spec.paths[path]:
                        self.spec.paths[path][verb] = verb_spec
            else:
                self.spec.paths[path] = dict()
                for verb, verb_spec in path_spec.items():
                    self.spec.paths[path][verb] = verb_spec

        for tag in resource_spec.tags:
            if tag not in self.spec.tags:
                self.spec.tags.append(tag)

    def swagger_json(self):
        """
        endpoint that returns the swagger.json specification.
        """
        return json.dumps(self.spec.to_dict())

    def index(self):
        """
        returns the swagger index.html page.
        """
        spec_name = "{}.swagger_json".format(self.api_title)
        temp = flask.render_template(self.index_path, spec=spec_name, api_title=self.api_title)
        return temp


def load(app:Flask, api_title, schemes, api_package="."):
    """ Flask-Mercury loader function.
    An autodiscover function used to load the framework on the current project.
    It will scan the current project looking for mercury Resources and Models
    :param app: The flask app reference.
    :param api_title: the api title.
    :param schemes: a list containing two possible values [http, https].
    :param api_package: a dotted path to the api root package.
    """
    # some imports needed to load the module
    # we are importing them here because it is required only on the first run
    import importlib
    from . import utils

    # builds api info part of the specification
    api_module = importlib.import_module(api_package)
    api_doc = api_module.__doc__
    doc = utils.parse_docstring(api_doc)
    s = MercuryApp(app, api_title, schemes, doc)
    s.auto_discover_spec(api_module)

    # finally register swagger routes
    # Setting CORS due to swagger-ui
    from flask_cors import CORS
    from flask import Blueprint
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__))

    # Blueprint initialization
    blueprint = Blueprint(
        api_title,
        __name__,
        static_folder="{}/static".format(current_dir),
        template_folder="{}/static/templates".format(current_dir),
        url_prefix=api_title
    )
    CORS(blueprint)

    blueprint.add_url_rule('/swagger', view_func=s.index)
    blueprint.add_url_rule('/swagger/swagger.json', endpoint="swagger_json", view_func=s.swagger_json)
    app.register_blueprint(blueprint, url_prefix="/"+blueprint.name, static_folder="{}/static".format(current_dir))
