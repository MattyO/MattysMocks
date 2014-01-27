from unittest import TestCase
from datetime import datetime
import patch
from patch import PatchObject
from object import MockObject, MethodMock

class TestPatch(TestCase):
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
        print 'calling dir directly on mock class'
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

