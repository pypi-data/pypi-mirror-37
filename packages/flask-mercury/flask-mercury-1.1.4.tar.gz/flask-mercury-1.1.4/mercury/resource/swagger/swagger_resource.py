# -*- coding: utf-8 -*-
"""
Module resource.py
---------------------
    The base Api swagger resource implementation.
    Provides the base functionality to serialize the resource meta information
    to the swagger spec.
"""
from mercury.resource import BaseResource
from mercury.api_model import ApiModel
import inspect
from simple_mappers.object_mapper import JsonObject
from mercury import utils
from mercury.resource import _verbs
from . import path_utils
from mercury.parameters.base import BaseParameter
from mercury.parameters.path import BasePathParameter
from mercury.parameters.query import BaseQueryParameter


class SwaggerResource(BaseResource):
    """
    A Base Swagger resource that adds metadata serialization to the swagger spec format.
    """
    ROUTE = None
    TAGS = None

    @classmethod
    def to_swagger(cls):
        """
        Swagger spec serialization function.
        :param cls: The class to be serialized.
        """
        # each verb builds a swagger path list
        resource_spec = JsonObject()
        resource_spec.paths = dict()
        resource_spec.tags = [{"name": tag} for tag in cls.get_tags()]
        for verb in _verbs:
            verb_specs = cls.get_verb_spec(verb)
            # now adds the verb to the resource spec
            for path, verb_spec in verb_specs.items():
                if path in resource_spec.paths:
                    resource_spec.paths[path][verb] = verb_spec[verb]
                else:
                    resource_spec.paths[path] = {
                        verb: verb_spec[verb]
                    }
        return resource_spec

    @classmethod
    def get_tags(cls):
        """
        Returns the resource tags.
        :param cls: the resource class being serialized to the swagger spec json.
        """
        # checks for Meta data
        if cls.TAGS is not None:
            # checks whether a tag meta data is provided
            return cls.TAGS
        else:
            # if no tag was provided then it will use the resource root __module__
            # path as tag
            return [cls.__module__.split('.')[1]]

    @classmethod
    def get_verb_spec(cls, verb):
        """
        Builds and returns the api spec for the resource verb.
        :return: The swagger Resource verb specification.
        """
        paths_spec = dict()
        paths = cls.get_paths(verb)
        # for each path in the paths list
        #  we build the swagger paths part of the schema
        for path, impl in paths:  # impl: reference to the resource method that implements the verb
            spec = cls.build_verb_spec(path, impl)
            # now adds the verb to path spec
            if path in paths_spec:
                paths_spec[path][verb] = spec
            else:
                paths_spec[path] = {
                    verb: spec
                }
        return paths_spec

    @classmethod
    def get_paths(cls, verb):
        """
        returns a list of paths for the verb received as parameter.
        :param verb: a verb name. Allowed values are "get", "post", "put", "delete", "head", "patch".
        :return: a list of tuples (path, impl),
        where *path* is the string path to the endpoint
        and *impl* is a reference for the class resource method that implements the endpoint.
        """
        # initializes the paths list
        paths = list()
        base_path = path_utils.format_base_path_swagger(cls)
        if hasattr(cls, verb):
            # sanity checks whether all base path parameters are defined on the resource function
            path_utils.check_route_and_verb_path_parameter_specifications(cls, verb)

            method = getattr(cls, verb, None)

            additional_params = path_utils.find_additional_params(cls, method)
            # no additional parameter was found
            if len(additional_params) == 0:
                paths = [(base_path, method)]
            else:  # verb defines more parameters than the base path
                required_params = path_utils.filter_required_params(additional_params)
                if len(required_params) > 0:
                    path = "{}/{}".format(
                        base_path,
                        "/".join(required_params)
                    )
                    # appends the parameter to the path list
                    paths.append((path, method))

                not_required_params = path_utils.filter_not_required_params(additional_params)
                if len(not_required_params) > 0:
                    # then appends one additional path to the paths list
                    # with the paths definition
                    path = "{}/{}".format(
                        base_path,
                        "/".join(not_required_params)
                    )
                    paths.append((path, method))

        return paths

    @classmethod
    def build_verb_spec(cls, path, verb):
        """
        Builds the swagger spec for the pair pair (path, verb)
        :param path: a resource endpoint path
        :param verb: a function that implements the verb.
        :return: the verb swagger specification.
        """
        verb_spec = JsonObject()
        verb_spec.tags = cls.get_tags()
        verb_spec.summary = verb.__pdoc__.summary
        verb_spec.description = verb.__pdoc__.description
        verb_spec.consumes = verb.__pdoc__.consumes
        verb_spec.produces = verb.__pdoc__.produces
        verb_spec.parameters = cls.get_verb_parameters_spec(path, verb)

        # finally builds the responses specification
        verb_spec.responses = cls.get_verb_responses_spec(verb)
        return verb_spec

    @classmethod
    def get_verb_parameters_spec(cls, path, verb):
        """
        Returns the swagger parameters spec for the verb implementation and path pair.
        :param path: a resource path.
        :param verb: a verb implementation.
        :return: swagger parameters specification.
        """
        spec = list()
        # foreach parameter defined in the verb implementation
        for par in verb.__params__:
            path_param = '{'+par.name+'}'
            if path_param in path:
                if issubclass(par.annotation, BasePathParameter):
                    param_spec = par.annotation.to_swagger(
                        par,
                        verb.__pdoc__.params.get(par.name)
                    )
                    spec.append(param_spec)
            elif issubclass(par.annotation, ApiModel):
                param_spec = par.annotation.to_swagger_as_parameter(
                    par,
                    verb.__pdoc__.params.get(par.name)
                )
                spec.append(param_spec)
            elif issubclass(par.annotation, BaseQueryParameter):
                param_spec = par.annotation.to_swagger(
                    par,
                    verb.__pdoc__.params.get(par.name)
                )
                spec.append(param_spec)

        return spec

    @classmethod
    def get_verb_responses_spec(cls, verb):
        """
        Returns the verb swagger responses spec for the given verb.
        :param verb: a verb implementation.
        :return: the verb swagger reponses specification.
        """
        spec = dict()
        # if it was declared the return type
        if issubclass(verb.__returns__, ApiModel):
            spec["200"] = verb.__returns__.to_swagger_as_response(verb.__pdoc__.returns)
        else:
            spec["200"] = {
                "description": verb.__pdoc__.returns,
                # 'type': self.TYPE_MAP.get(impl.__returns__.__name__)
            }

        for ex, description in verb.__pdoc__.raises.items():
            # ex is a string containing or the error code
            # or the dotted path to the exception
            if not utils.is_integer(ex):  # is it is a dotted path
                _ex = utils.import_string(ex)
                # sanity check exception type
                if not hasattr(_ex, "code"):
                    raise TypeError(
                        "The exception {} specified on the doc sting is no an http exception"
                        "and does not defines a error code."
                        "Exceptions specified on the docstring must by an http exception.".format(ex)
                    )
                spec[str(_ex.code)] = {"description": description}
            else:  # otherwise it is just a error code
                spec[ex] = {"description": description}

        return spec