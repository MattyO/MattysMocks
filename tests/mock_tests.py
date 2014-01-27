from unittest import TestCase
from object import mock, MockObject, MethodMock, AttributeMock
from datetime import datetime

class DumbClass():
    a_attribute = 'test attribute'

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

class TestMock(TestCase):
    def setUp(self):
        self.MockClass = mock(template=DumbClass)

    def test_mock_should_return_a_mock_class(self):
        self.assertIsInstance(mock(), type(MockObject))

    def test_mock_class_should_have_default_methods_of_a_template(self):
        self.assertTrue('a_method' in dir(mock(template=DumbClass)))
        self.assertIsInstance(self.MockClass.a_method, MethodMock)

    def test_mock_class_default_methods_should_include_class_methods(self):
        self.assertTrue('class_method' in dir(mock(template=DumbClass)))
        self.assertIsInstance(self.MockClass.class_method, MethodMock)

    def test_mock_class_default_methods_should_include_static_methods(self):
        self.assertTrue('static_method' in dir(mock(template=DumbClass)))
        self.assertIsInstance(self.MockClass.static_method, MethodMock)

    def test_mock_attribute_can_get_calls(self):
        test_mock = self.MockClass()
        test_mock.a_attribute
        self.assertEquals(len(test_mock.attribute_calls), 1)

    def test_mock_class_takes_a_list_of_methods(self):
        self.assertFalse('extra' in dir(mock(template=datetime)))
        self.assertTrue('extra' in dir(mock(template=datetime, methods=['extra'])))

    def test_mock_class_should_properties_shoud_behave_like_attributes(self):
        test_mock = self.MockClass()
        test_mock.a_property
        self.assertEqual(test_mock.a_property, None)

    def test_mock_class_undefined_methods_should_return_mock_method(self):
        test_mock = self.MockClass()
        test_mock.notamethod()
        self.assertIsInstance(test_mock.notamethod, MethodMock)

    def test_mock_class_takes_a_list_of_dicts_for_return_methods(self):
        test_mock = mock(template=datetime, methods={'extra':"test value"})()
        self.assertEqual(test_mock.extra(), "test value")

    def test_mock_class_takes_a_list_of_attributes(self):
        self.assertTrue('extra' in dir(mock(template=datetime, attributes=['extra'])))

    def test_default_return_for_method_mock_is_none(self):
        test_mock = self.MockClass()
        self.assertEqual(test_mock.a_method(), None)

    def test_mock_class_takes_a_list_of_attributes_as_dicts_for_default_values(self):
        test_mock = mock(template=datetime, attributes={'extra':"test value"})()
        self.assertEqual(test_mock.extra, "test value" )

