from unittest import TestCase
from mattys_mocks.patch import PatchObject
from mattys_mocks.object import mock, MockObject, MethodMock, AttributeMock
from datetime import datetime
from mattys_mocks.tests.mock_these.dumb_class import DumbClass


class TestPatchObject(TestCase):
    def setUp(self):
        self.PatchObject = PatchObject(template=DumbClass)

        an_instance = self.PatchObject()
        b_instance = self.PatchObject()

        self.instance = an_instance

        self.PatchObject.a_class_method()
        an_instance.a_method()
        an_instance.b_method()
        an_instance.a_property = "test value"
        b_instance.a_attribute = "test value"
        an_instance.a_attribute = "test value"
        b_instance.a_method()
        an_instance.a_property
        an_instance.a_attribute

    def tearDown(self):
        self.PatchObject = None

    def test_first_instance_is_none_if_none_exsist(self):
        PatchObj2 = PatchObject(template=DumbClass)
        self.assertEqual(PatchObj2.first_instance, None)


    def test_first_instance(self):
        self.assertEqual(self.PatchObject.first_instance, self.instance)

    def test_class_method_calls(self):
        self.assertEqual(len(self.PatchObject.class_method_calls), 1)

    def test_all_calls(self):
        all_call_names = map(lambda c: c.name, self.PatchObject.all_calls)
        self.assertEqual(all_call_names, 
                [   'a_class_method', 
                    'a_method',
                    'b_method',
                    'a_property',
                    'a_attribute',
                    'a_attribute',
                    'a_method',
                    'a_property',
                    'a_attribute'])

    #will produce method dups for different instances
    def test_all_method_calls(self):
        #print len(self.PatchObject.instances)
        all_method_names = map(lambda c: c.name, self.PatchObject.method_calls)
        self.assertEqual(all_method_names,
                ['a_class_method', 'a_method', 'b_method', 'a_method'])

    def test_all_attribute_calls(self):
        all_attribute_names = map(lambda c: c.name, self.PatchObject.attribute_calls)
        self.assertEqual(all_attribute_names,
                [   'a_property',
                    'a_attribute',
                    'a_attribute',
                    'a_property',
                    'a_attribute'])


class TestMockObject(TestCase):

    #these are a little harder because they involve some manual mocking
    #=================================================================================
    #def test_mock_object_should_throw_a_wargning_for_unknow_method(self):
    #    mock_object = MockObject()

    #    mock_object.somemethod()

    #    self.assertTrue(False)

    #def test_mock_object_should_throw_a_wargning_for_unknow_method_only_for_first_time_called(self):
    #    mock_object = MockObject()

    #    mock_object.somemethod()
    #    mock_object.somemethod()

    #    self.assertTrue(False)
    #=================================================================================

    #blocked on adding attributemocks in mock constructor
    #=================================================================================
    #def test_mock_object_should_accpet_methods_in_init(self):
    #    mock_object = MockObject(methods=['amethod'])
    #    self.assertIsInstance(mock_object.amethod, MethodMock)

    #def test_mock_object_should_accept_methods_in_init_in_dict_form(self):
    #    mock_object_two = MockObject(method={'amethod':'somevalue'})
    #    self.assertEqual(mock_object.amethod(), 'somevalue')

    #def test_mock_object_should_accept_attributes_in_init(self):
    #    mock_object = MockObject(attributes=['someattribute'])
    #    mock_object.someattribute = AttributeMock('someattribute', None)

    #    self.assertEqual(mock_object.someattribute, None)

    #def test_mock_object_should_accept_attributes_in_init_in_dict_form(self):
    #    mock_object = MockObject(attributes={'someattribute':'somevalue'})
    #    self.assertEqual(mock_object.someattribute, 'somevalue')
    #=================================================================================

    def test_all_calls(self):
        mock_object = mock(template=DumbClass)()
        mock_object .a_attribute = 1
        mock_object.a_method()
        get_something = mock_object.a_attribute
        mock_object.b_method()
        mock_object.b_attribute = 2


        call_names = map(lambda c: c.name, mock_object.all_calls)
        self.assertEqual(call_names,
                ['a_attribute', 'a_method', 'a_attribute', 'b_method', 'b_attribute'] )

    def test_method_calls(self):
        mock_object = mock(template=DumbClass)()
        mock_object.a_method()
        mock_object.b_method()
        self.assertEqual(len(mock_object.method_calls), 2)
        self.assertEqual(mock_object.method_calls[0].name, 'a_method')
        self.assertEqual(mock_object.method_calls[1].name, 'b_method')

    def test_attribute_calls(self):
        an_instance  = mock(tempalte=DumbClass, attributes=['a_attribute', 'b_attribute'])()

        an_instance.a_attribute = 1
        get_something = an_instance.a_attribute
        an_instance.b_attribute = 2

        attribute_names = map(lambda c: c.name, an_instance.attribute_calls)
        attribute_values = map(lambda c: (c.initial_value, c.final_value), an_instance.attribute_calls)

        self.assertEqual(attribute_names, ['a_attribute', 'a_attribute', 'b_attribute'])
        self.assertEqual(attribute_values, [(None, 1), (1,1), (None,2)])

class TestMock(TestCase):
    def setUp(self):
        self.MockClass = mock(template=DumbClass)

    def test_mock_should_return_a_mock_class(self):
        self.assertIsInstance(mock(), type(MockObject))

    def test_mock_class_should_have_default_methods_of_a_template(self):
        self.assertTrue('a_method' in dir(mock(template=DumbClass)))
        self.assertIsInstance(self.MockClass.a_method, MethodMock)


    #this test should be deleted when attributes can be safely added through the mock constructor
    def test_mock_should_add_the_attribute_attribute_names(self):
        self.assertEqual(sorted(self.MockClass.attribute_names), sorted(['a_property', 'a_attribute', 'b_attribute']))

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

