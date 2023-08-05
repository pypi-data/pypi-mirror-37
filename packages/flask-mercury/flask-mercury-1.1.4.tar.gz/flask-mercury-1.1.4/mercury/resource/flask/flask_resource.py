# -*- coding: utf-8 -*-
"""
Module flask_resource.py
---------------------
    The base flask Api resource implementation.
    Provides the base end point functionality such as route register request auto serialization
    and method dispatch.
"""
from ..meta_resource import BaseResource
from mercury.parameters.path import BasePathParameter
from flask import request, jsonify
from mercury.api_model import ApiModel
from flask import Flask
import inspect
import json
from mercury import exceptions
from io import StringIO
from werkzeug import exceptions as http_exceptions
from mercury.resource import _verbs
from . import path_utils
from flask.globals import current_app


class FlaskResource(BaseResource):
    """
    A Base API endpoint class implementation.
    """
    ROUTE = None
    __model__ = None

    def __init__(self):
        """
        Resource initialization function.
        """
        super().__init__()
        # request object shortcut
        self.request = request

    def dispatch_request(self, *args, **kwargs):
        """
        Parses the body of an post request into a Mapping definition object before
        dispatching the request to the endpoint implementation.
        """
        # identify the http request verb
        args = list(args)

        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        # sanity check on verb implementation
        if meth is None:
            raise http_exceptions.MethodNotAllowed(
                None,
                "The api endpoint {}, does not support the {} http/https verb.".format(
                    request.path, request.method
                )
            )

        args_ = list()
        kwargs_ = dict()
        model = None
        for param in meth.__params__:
            # TODO: save this information on somewhere to not have perform issubclass check every time
            if issubclass(param.annotation, (ApiModel,)):
                model = param.annotation
            if param.name != "self":
                if param.default is inspect._empty:
                    default = None
                else:
                    default = param.default
                p = param.annotation.from_request(param.name, default)
                if default is None:
                    args_.append(p)
                else:
                    kwargs_[param.name] = p

        if model is None and len(request.data) > 0:
            raise http_exceptions.InternalServerError(
                "There is an error on the resource definition. "
                "Could not parse the request body."
            )

        response = super().dispatch_request(*args_, **kwargs_)
        if isinstance(response, (ApiModel,)):
            response = response.to_dict()

        response = json.dumps(response, allow_nan=False, ensure_ascii=False)
        response = current_app.response_class(
            response,
            mimetype=current_app.config['JSONIFY_MIMETYPE']
        )
        return response

    @classmethod
    def register(cls, app:Flask, api_title):
        """
        Register the resource endpoint route and initialize its path parameters.
        :param app: a reference to the 'flask.Flask' app.
        :param api_title: the api title.
        """
        base_path = cls.get_base_path()
        # get the resource base path
        # checks for route meta data
        base_parameters = path_utils.get_route_parameters(base_path)

        # for each http verb performs a sanity check on the path parameters
        for verb in _verbs:
            if hasattr(cls, verb):
                impl = getattr(cls, verb)
                # checks path parameters definition
                cls.check_base_param_equality(base_parameters, impl)

                # builds final paths
                # for each additional parameter
                # appends to the path
                cls.add_url_rules(app, impl, verb, api_title)

    @classmethod
    def get_base_path(cls):
        """
        Returns the resource base route path.
        If no cls.ROUTE was provided it uses the class dotted path to build a base route for the resource.
        :return: the resource base route path
        """
        base_path = cls.ROUTE
        if base_path is None:
            # otherwise uses the module dotted path as path
            mod = cls.__module__.split('.')
            # remove file name from path
            mod.pop()
            if cls.__name__.lower() != mod[-1]:
                mod = "/".join(mod)
                base_path = "/{}/{}".format(mod, cls.__name__.lower())
            else:
                mod = "/".join(mod)
                base_path = "/{}".format(mod)

        return base_path

    @classmethod
    def add_url_rules(cls, app, impl, verb_name, api_title):
        """
        Builds a complete route path and adds the route rule to the impl verb.
        :param app: A flask application object;
        :param impl: the verb implementation.
        :param verb_name: the verb name e.g. get, post, put .....
        :param api_title: the api title.
        """
        base_path = cls.get_base_path()
        # builds final paths
        # for each additional parameter
        # appends to the path
        str_builder = StringIO()
        first_default_flag = False
        # base_path must start with the api_title
        if not base_path.startswith(api_title):
            str_builder.write("/" + api_title)
        str_builder.write(base_path)
        for parameter in impl.__params__:
            if parameter.default is not inspect._empty and not first_default_flag:
                app.add_url_rule(
                    str_builder.getvalue(),
                    view_func=cls.as_view("{}_{}".format(verb_name,cls.__name__)),
                    methods=[verb_name.upper(), ]
                )
                first_default_flag = True

            # adds path_param to the base_path
            if issubclass(parameter.annotation, BasePathParameter):
                if parameter.name not in base_path:
                    path_param = "/<{}:{}>".format(parameter.annotation.flask_type, parameter.name)
                    str_builder.write(path_param)

        view_name = "{}_{}_full".format(verb_name, cls.__name__)
        app.add_url_rule(
            str_builder.getvalue(),
            view_func=cls.as_view(view_name),
            methods=[verb_name.upper(), ]
        )

    @staticmethod
    def check_base_param_equality(base_params, impl):
        """
        checks whether all items in both list of parameters are equals.
        :param base_params: list of base path parameters
        :param impl: a reference to a verb method implementation.
        :return: true if all items in the sequence of both lists are equals.
        :raises: mercury.exceptions.ResourceSpecError
        """
        if base_params is not None:
            # removes args, kwargs and self from the list of impl_params
            params = [
                p.name for p in impl.__params__
                if p.name not in ["args", "kwargs", "self"]
                and not issubclass(p.annotation, (ApiModel,))
            ]
            if len(params) == 0:
                return True
            # check list equality
            for i in range(len(base_params)):
                if params[i] != base_params[i]:
                    # if some divergence is found,
                    # then returns false
                    raise exceptions.ResourceSpecError(
                        "Wrong method parameter definition on '{impl}'. "
                        "The all base_path parameters must be defined in the method signature,"
                        " in the ordering that they appear on the base path. "
                        "Additional parameters may be declared after the ones defined on the base_path."
                        "For more information please refers to the mercury documentation."
                        "Method name: {impl}."
                        "Method declared parameters: {meth_params}."
                        "Base path parameters: {base_params}".format(
                            impl=impl.__qualname__,
                            meth_params=params,
                            base_params=base_params
                        )
                    )
        # return true if every thing is ok
        return True