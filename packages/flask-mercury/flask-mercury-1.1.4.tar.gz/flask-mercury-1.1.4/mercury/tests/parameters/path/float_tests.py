# -*- coding: utf-8 -*-
"""
Module base_tests.py
----------------------
A test suite for the float path parameter.
"""
import unittest
from mercury.parameters.path.float_param import Float
from mercury import utils
import inspect
from werkzeug.exceptions import BadRequest


def test_function(parameter:Float="true"):
    """
    A function that defines a base parameter with default value.
    :param parameter: the function parameter with default value.
    """
    return True


class FloatParameterTests(unittest.TestCase):
    """
    A test suite for the base parameter class.
    """

    def test_should_serialize_spec_parameter_correctly(self):
        """
        Tests if the parameter spec is serialized correctly.
        """

        signature = inspect.signature(test_function)
        method_params = list(signature.parameters.values())
        doc_str = utils.parse_docstring(test_function.__doc__)
        par = method_params[0]
        spec = Float.to_swagger(par, doc_str.to_dict().get("params").get("parameter"))

        self.assertEqual(spec['type'], "number")

    def test_should_initialize_float(self):
        """
        test boolean parameter initialization function.
        """
        val = Float("parameter", "1.1")
        self.assertTrue(isinstance(val, float))
        self.assertTrue(val == 1.1)

        val = Float("parameter", 1.1)
        self.assertTrue(isinstance(val, float))
        self.assertTrue(val == 1.1)

    def test_should_not_initialize_float(self):
        """
        test boolean parameter initialization function.
        """
        self.assertRaises(BadRequest, lambda: Float("parameter", "false"))

    def test_should_pass_isinstance(self):
        """
        test if a bool builtin type pass in the isinstance(..) check.
        """
        flag = 11.1
        self.assertTrue(isinstance(flag, Float))
        # flag = "11.1"
        # self.assertTrue(isinstance(flag, Float))

    def test_should_not_pass_instance_check(self):
        flag = "sss"
        self.assertRaises(BadRequest, lambda: isinstance(flag, Float))

    def test_should_call_test_function(self):
        ret = test_function(11.1)
        self.assertTrue(ret)
        ret = test_function(11)
        self.assertTrue(ret)


if __name__ == "__main__":
    unittest.main()