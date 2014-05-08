import types 
import time
import warnings
from collections import namedtuple

def mock(*kargs, **kwargs):
    things = {}
    attributes = []
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
        attributes = list(set(attributes + additional_attributes.keys()))

    things['attribute_names'] = attributes
    return type("MockObject", (MockObject,), things)

class MockObject(object):
    def __init__(self, methods=[], attributes=[]):

        self.attribute_calls = []
        #self.__dict__.update({attribute_name:AttributeMock(attribute_name, None)
        #    for attribute_name in attributes})

    def __getattr__(self,name):
        warnings.warn('creating mock for method "'+name+'" that doesnt exsist', RuntimeWarning)
        mock_created = MethodMock()
        setattr(self, name,  mock_created )
        return mock_created

    @classmethod
    def methods(self):
        return dir(self)

    @property
    def all_calls(self):
        all_calls = self.attribute_calls + self.method_calls
        all_calls = sorted(all_calls, key=lambda c: c.time)
        return all_calls

    @property
    def method_calls(self):
        print 'calling all method calls'

        ignore_these = ['attribute_calls', 'method_calls', 'all_calls'] + self.attribute_names
        method_names = [method_name for method_name in dir(self)
                if method_name not in ignore_these  ]

        mock_methods_names = filter(lambda method_name: isinstance(getattr(self, method_name), MethodMock) , method_names)

        all_mock_calls = []
        for mock_method_name in mock_methods_names:
            local_mock_method = getattr(self, mock_method_name)
            for call in local_mock_method.calls:
                call.name = mock_method_name
            all_mock_calls += local_mock_method.calls

        all_mock_calls = sorted(all_mock_calls,
                key=lambda a_call: a_call.time)

        return all_mock_calls

class AttributeMock(object):

    def __init__(self, name, default=None):
        self.name = name
        self.value = default

    def _call_attributes(self, new_value):
        return {
            'name': self.name,
            'type': 'attribute',
            'time': time.clock(),
            'initial_value': self.value,
            'final_value': new_value,
        }

    def __set__(self, instance, value):
        call_attributes = {
            'name': self.name,
            'type': 'attribute',
            'time': time.clock(),
            'initial_value': self.value,
            'final_value': value,
        }

        instance.attribute_calls.append(type('MockCall', (object,), call_attributes))
        self.value = value

    def __get__(self, instance, owner_class):
        #print 'getting attribute ' + self.name
        call_attributes = {
            'name': self.name,
            'type': 'attribute',
            'time': time.clock(),
            'initial_value': self.value,
            'final_value': self.value,
        }

        instance.attribute_calls.append(type('MockCall', (object,), call_attributes))
        return self.value

class MethodMock():

    def __init__(self, returns=None):
        self.returns = returns
        self.calls = []

    def __call__(self, *args, **kwargs):
        call_attributes = {
            'type': 'method',
            'time': time.clock(),
            'args':args,
            "kwargs": kwargs
        }

        self.calls.append(type('MockCall', (object,), call_attributes))
        return self.returns

    @classmethod
    def returns(self, a_value):
        self.returns = a_value

    @classmethod
    def was_called(self):
        return len(self.calls) > 0

