# -*- coding: utf-8 -*-
"""
Module base_tests.py
----------------------
A test suite for the base parameter test.
"""
import unittest
from mercury.parameters.base import BaseParameter
from mercury import utils
import inspect


def test_function_no_default(parameter:BaseParameter):
    """
    A function that defines a base parameter without default value.
    :param parameter: the function parameter.
    """
    pass


def test_function_default(parameter:BaseParameter="test"):
    """
    A function that defines a base parameter with default value.
    :param parameter: the function parameter with default value.
    """
    pass


class BaseParameterTests(unittest.TestCase):
    """
    A test suite for the base parameter class.
    """

    def test_should_serialize_spec_parameter_required_correctly(self):
        """
        Tests if the parameter spec is serialized correctly.
        """

        signature = inspect.signature(test_function_no_default)
        method_params = list(signature.parameters.values())
        doc_str = utils.parse_docstring(test_function_no_default.__doc__)
        par = method_params[0]
        spec = BaseParameter.to_swagger(par, doc_str.to_dict().get("params").get("parameter"))
        expected = {
            "name": "parameter",
            "description": "the function parameter.",
            "required": True
        }
        self.assertEqual(spec, expected)

    def test_should_serialize_spec_parameter_not_required_correctly(self):
        """
        Tests if the parameter spec is serialized correctly.
        """

        signature = inspect.signature(test_function_default)
        method_params = list(signature.parameters.values())
        doc_str = utils.parse_docstring(test_function_default.__doc__)
        par = method_params[0]
        spec = BaseParameter.to_swagger(par, doc_str.to_dict().get("params").get("parameter"))
        expected = {
            "name": "parameter",
            "description": "the function parameter with default value.",
            "required": False
        }
        self.assertEqual(spec, expected)


if __name__ == "__main__":
    unittest.main()