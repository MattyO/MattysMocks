from unittest import TestCase
from datetime import datetime
import mattys_mocks.patch as patch
from mattys_mocks.patch import PatchObject
from mattys_mocks.object import MockObject, MethodMock
from mattys_mocks.tests.mock_these.dumb_class import DumbClass
from mattys_mocks.tests.mock_these.parent_class import ParentClass
import mattys_mocks.tests.mock_these.bunch_of_functions as bof

import warnings
import types
#warnings.warn(str([ name for name, type in locals().items() if  isinstance(type, types.ModuleType) ]))
#warnings.warn(str(id(locals())))

class TestPatchFunction(TestCase):
    @patch.function("mattys_mocks.tests.mock_these.bunch_of_functions.a_function")
    def test_patch_should_replace_function_with_methoond_mock(self, function_mock):
        self.assertIsInstance(bof.a_function, MethodMock)

    @patch.function("mattys_mocks.tests.mock_these.bunch_of_functions.a_function")
    def test_patch_function_returns_non_by_default(self, function_mock):
        self.assertEqual(bof.a_function(), None)

    @patch.function("mattys_mocks.tests.mock_these.bunch_of_functions.a_function", returns="new_value")
    def test_patch_should_replace_function_with_return_value(self, function_mock):
        self.assertEqual(bof.a_function(), "new_value")

class TestPatchObject(TestCase):
    def test_patch_should_not_effect_method_before(self):
        from datetime import datetime
        self.assertIsInstance(datetime.now(), datetime)

    @patch.object('datetime.datetime')
    def test_patched_object_should_return_patch_object(self, patch):
        from datetime import datetime
        self.assertIsInstance(datetime, PatchObject)

    @patch.object('datetime.datetime')
    def test_calling_patched_object_returns_mock_object(self, patch):
        from datetime import datetime
        self.assertIsInstance(datetime(), MockObject)

    @patch.object('datetime.datetime')
    def test_calling_method_of_class_object_returns_method_mock(self, patch):
        from datetime import datetime
        self.assertIsInstance(datetime.now, MethodMock)

    @patch.object('datetime.datetime')
    def test_patched_method_should_have_default_methods_of_mocked_class(self, patch):
        from datetime import datetime
        print dir(datetime)
        self.assertTrue('now' in  dir(datetime))

    @patch.object('datetime.datetime')
    def test_treat_all_methods_found_as_classmethods(self, patch):
        from datetime import datetime
        datetime.now()

    @patch.object('datetime.datetime')
    def test_adds_instances_to_patch_attribute(self, patch):
        from datetime import datetime
        mock_object = datetime()
        self.assertEqual(len(patch.instances), 1)
        self.assertEqual(mock_object, patch.instances[0])

    def test_patch_should_not_effect_method_after(self):
        from datetime import datetime
        self.assertIsInstance(datetime.now(), datetime)

    @patch.object('datetime.datetime')
    @patch.object('mattys_mocks.tests.mock_these.parent_class.DumbClass', methods={"a_method":"test return"})
    def test_patches_are_stackable(self, dumb_patch, datetime_patch,):
        pass

    @patch.object('datetime.datetime')
    @patch.function("mattys_mocks.tests.mock_these.bunch_of_functions.a_function")
    def test_object_and_function_patches_are_stackable(self, dumb_patch, datetime_patch,):
        pass

    @patch.object('mattys_mocks.tests.mock_these.parent_class.DumbClass', methods={"a_method":"test return"})
    def test_patch_with_parent_has_a_relationship(self, dumb_patch):
        pc = ParentClass()
        #print globals()
        #print pc.dumb.a_method
        self.assertEqual(pc.get_method(), "test return")

