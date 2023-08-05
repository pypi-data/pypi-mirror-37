# -*- coding: utf-8 -*-
"""
Module base_tests.py
----------------------
A test suite for the base path parameter.
"""
import unittest
from mercury.parameters.path.base import BasePathParameter
from mercury import utils
import inspect


def test_function(parameter:BasePathParameter="test"):
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

        signature = inspect.signature(test_function)
        method_params = list(signature.parameters.values())
        doc_str = utils.parse_docstring(test_function.__doc__)
        par = method_params[0]
        spec = BasePathParameter.to_swagger(par, doc_str.to_dict().get("params").get("parameter"))

        self.assertEqual(spec['in'], "path")


if __name__ == "__main__":
    unittest.main()