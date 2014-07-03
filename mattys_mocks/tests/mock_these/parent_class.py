#import mock_these.dumb_class
from mattys_mocks.tests.mock_these.dumb_class import DumbClass
import warnings
import types
#warnings.warn(str([ name for name, type in locals().items() if  isinstance(type, types.ModuleType) ]))
#warnings.warn(str(id(locals())))
class ParentClass():
    def __init__(self):
        self.dumb = DumbClass()

    def get_attribute(self):
        return dumb.a_attribute

    def get_method(self):
        return self.dumb.a_method()

    def get_property(self):
        return self.dumb.a_property

    def get_class_method(self):
        return self.dumb.class_method()

    def get_staticmethod(self):
        return self.dumb.static_method()


