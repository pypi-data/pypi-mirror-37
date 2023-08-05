# -*- coding: utf-8 -*-
"""
Module base_tests.py
----------------------
A test suite for the base query parameter.
"""
import unittest
from mercury.parameters.query.boolean import Boolean
from mercury import utils
import inspect
from werkzeug.exceptions import BadRequest


def test_function(parameter:Boolean="true"):
    """
    A function that defines a base parameter with default value.
    :param parameter: the function parameter with default value.
    """
    return True


class BooleanParameterTests(unittest.TestCase):
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
        spec = Boolean.to_swagger(par, doc_str.to_dict().get("params").get("parameter"))

        self.assertEqual(spec['type'], "boolean")

    def test_should_initialize_boolean_as_true(self):
        """
        test boolean parameter initialization function.
        """
        val = Boolean("parameter", "true")
        self.assertTrue(isinstance(val, bool))
        self.assertTrue(val)

        val = Boolean("parameter", True)
        self.assertTrue(isinstance(val, bool))
        self.assertTrue(val)

    def test_should_initialize_boolean_as_false(self):
        """
        test boolean parameter initialization function.
        """
        val = Boolean("parameter", "false")
        self.assertTrue(isinstance(val, bool))
        self.assertTrue(not val)

        val = Boolean("parameter", False)
        self.assertTrue(isinstance(val, bool))
        self.assertTrue(not val)

    def test_should_pass_isinstance(self):
        """
        test if a bool builtin type pass in the isinstance(..) check.
        """
        flag = True

        self.assertTrue(isinstance(flag, Boolean))
        flag = False

        self.assertTrue(isinstance(flag, Boolean))

        flag = "true"

        self.assertTrue(isinstance(flag, Boolean))

        flag = "false"

        self.assertTrue(isinstance(flag, Boolean))

    def test_should_not_pass_instance_check(self):
        try:
            flag = 21
            isinstance(flag, Boolean)
        except BadRequest as ex:
            self.assertTrue(isinstance(ex, BadRequest))

        try:
            flag = "not a flag"
            isinstance(flag, Boolean)
        except BadRequest as ex:
            self.assertTrue(isinstance(ex, BadRequest))

    def test_should_call_test_function(self):
        ret = test_function("true")
        self.assertTrue(ret)
        ret = test_function(True)
        self.assertTrue(ret)
        ret = test_function("False")
        self.assertTrue(ret)
        ret = test_function(False)
        self.assertTrue(ret)


if __name__ == "__main__":
    unittest.main()