# -*- coding: utf-8 -*-
"""
Module integer_tests.py
----------------------
A test suite for the Uuid path parameter.
"""
import unittest
from mercury.parameters.path.uuid import Uuid
from mercury import utils
import inspect
from werkzeug.exceptions import BadRequest
import uuid


def test_function(parameter:Uuid="true"):
    """
    A function that defines a base parameter with default value.
    :param parameter: the function parameter with default value.
    """
    return True


class UuidParameterTests(unittest.TestCase):
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
        spec = Uuid.to_swagger(par, doc_str.to_dict().get("params").get("parameter"))

        self.assertEqual(spec['type'], "string")

    def test_should_initialize_str(self):
        """
        test boolean parameter initialization function.
        """
        val_str = str(uuid.uuid4())
        val = Uuid("parameter", val_str)
        self.assertTrue(isinstance(val, uuid.UUID))
        self.assertTrue(val == uuid.UUID(val_str))

    def test_should_pass_isinstance(self):
        """
        test if a bool builtin type pass in the isinstance(..) check.
        """
        val = uuid.uuid4()

        self.assertTrue(isinstance(val, Uuid))
        self.assertTrue(isinstance(str(val), Uuid))
        # flag = "11.1"
        # self.assertTrue(isinstance(flag, Float))

    def test_should_not_pass_instance_check(self):
        flag = 11
        self.assertRaises(BadRequest, lambda: isinstance(flag, Uuid))

    def test_should_call_test_function(self):
        val = uuid.uuid4()
        ret = test_function(str(val))
        self.assertTrue(ret)


if __name__ == "__main__":
    unittest.main()