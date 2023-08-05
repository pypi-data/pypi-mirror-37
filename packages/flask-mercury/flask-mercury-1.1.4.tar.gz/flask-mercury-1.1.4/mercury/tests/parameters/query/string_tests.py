# -*- coding: utf-8 -*-
"""
Module integer_tests.py
----------------------
A test suite for the string query parameter.
"""
import unittest
from mercury.parameters.query.string import String
from mercury import utils
import inspect
from werkzeug.exceptions import BadRequest


def test_function(parameter:String="true"):
    """
    A function that defines a base parameter with default value.
    :param parameter: the function parameter with default value.
    """
    return True


class IntegerParameterTests(unittest.TestCase):
    """
    A test suite for the String parameter class.
    """

    def test_should_serialize_spec_parameter_correctly(self):
        """
        Tests if the parameter spec is serialized correctly.
        """

        signature = inspect.signature(test_function)
        method_params = list(signature.parameters.values())
        doc_str = utils.parse_docstring(test_function.__doc__)
        par = method_params[0]
        spec = String.to_swagger(par, doc_str.to_dict().get("params").get("parameter"))

        self.assertEqual(spec['type'], "string")

    def test_should_initialize_str(self):
        """
        test boolean parameter initialization function.
        """
        val = String("parameter", "1")
        self.assertTrue(isinstance(val, str))
        self.assertTrue(val == "1")

        val = String("parameter", 1)
        self.assertTrue(isinstance(val, str))
        self.assertTrue(val == "1")

    def test_should_pass_isinstance(self):
        """
        test if a bool builtin type pass in the isinstance(..) check.
        """
        flag = "11"
        self.assertTrue(isinstance(flag, String))
        # flag = "11.1"
        # self.assertTrue(isinstance(flag, Float))

    def test_should_not_pass_instance_check(self):
        flag = 11
        self.assertRaises(BadRequest, lambda: isinstance(flag, String))

    def test_should_call_test_function(self):
        ret = test_function("11")
        self.assertTrue(ret)


if __name__ == "__main__":
    unittest.main()