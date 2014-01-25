from unittest import TestCase
from object import mock, MockObject
from datetime import datetime

class DumbClass():
    def a_method(self):
        pass

    @property
    def a_property(self):
        pass

    @classmethod
    def class_method(self):
        pass
    @staticmethod
    def static_method():
        pass


class TestMockFunction(TestCase):
    def test_mock_should_return_a_mock_class(self):
        self.assertIsInstance(mock(), type(MockObject))

    def test_mock_class_should_have_default_methods_of_a_template(self):
        self.assertTrue('a_method' in dir(mock(template=DumbClass)))

    def test_mock_class_default_methods_should_include_class_methods(self):
        self.assertTrue('class_method' in dir(mock(template=DumbClass)))

    def test_mock_class_default_methods_should_include_static_methods(self):
        self.assertTrue('static_method' in dir(mock(template=DumbClass)))

    def test_mock_class_should_have_default_method_of_a_templated_builtin(self):
        self.assertTrue('now' in dir(mock(template=datetime)))
