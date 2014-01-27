import types 
import warnings


def mock(*kargs, **kwargs):
    things = {}
    if 'template' in kwargs.keys():
        template = kwargs['template']
        items = [ method for method in dir(template) if not method.startswith('__')]
        method_types = [types.MethodType, types.FunctionType, types.BuiltinMethodType]
        methods = filter(lambda thing:type(getattr(template, thing)) in method_types , items)
        attributes = list(set(items).difference(methods))
        things = { method_name:MethodMock() for method_name in methods }
        things.update({attribute_name:AttributeMock(attribute_name) for attribute_name in attributes if not attribute_name.startswith('__')})

    if 'methods' in kwargs.keys():
        additional_methods = kwargs['methods']
        if isinstance(additional_methods, types.ListType):
            additional_methods= { method_name: None for method_name in additional_methods }

        things.update({ method_name:MethodMock(return_value) for method_name, return_value in additional_methods.items() })

    if 'attributes' in kwargs.keys():
        additional_attributes= kwargs['attributes']
        if isinstance(additional_attributes, types.ListType):
            additional_attributes= { attr_name: None for attr_name in additional_attributes }
        things.update({attr_name:AttributeMock(attr_name, attr_return) for attr_name, attr_return in additional_attributes.items()})
    return type("MockObject", (MockObject,), things)

class MockObject(object):
    def __init__(self):
        self.attribute_calls = []

    def __getattr__(self,name):
        warnings.warn("creating mock for a method that doesnt exsist", RuntimeWarning)
        return MethodMock()

    @classmethod
    def methods(self):
        return dir(self)

class AttributeMock(object):

    def __init__(self, name, default=None):
        self.name = name
        self.value = default

    def __set__(self, instance, value):

        instance.attribute_calls.append("set: "+ self.name+", value: " + str(value))
        self.value = value

    def __get__(self, instance, owner_class):
        instance.attribute_calls.append("get: "+ self.name+", value: " + str(self.value))
        return self.value

class MethodMock():

    def __init__(self, returns=None):
        self.returns = returns
        self.calls = []

    def __call__(self, *kargs, **kwargs):
        self.calls.append(type('MockCall', (object,), {'args':kargs, "kwargs": kwargs}))
        return self.returns

    @classmethod
    def returns(self, a_value):
        self.returns = a_value

    @classmethod
    def was_called(self):
        return len(self.calls) > 0

