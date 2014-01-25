import types 

def mock(*kargs, **kwargs):
    things = {}
    if 'template' in kwargs.keys():
        template = kwargs['template']
        items = [ method for method in dir(template) if not method.startswith('__')]
        methods = filter(lambda thing:
                    type(getattr(template, thing)) is types.MethodType or
                    type(getattr(template, thing)) is types.FunctionType or
                    type(getattr(template, thing)) is types.BuiltinMethodType,
                items)
        attributes = list(set(items).difference(methods))
        things = { method_name:MethodMock() for method_name in methods }
        things.update({attribute_name:AttributeMock() for attribute_name in attributes if not attribute_name.startswith('__')})

    #if 'attributes' in kwargs.keys():
    #    things.update({attribute_name:AttributeMock() for attribute_name in kwargs['attributes']})

    return type("MockObject", (MockObject,), things)

class MockObject(object):
    def __init__(self):
        print 'making a mock object one'
    def __getattr__(self, name):
        if name.startswith("__"):
            return super(MockObject, self).__getattribute__(name)
        print 'warning returning mock method for unknown method ' + name
        self.__dict__[name] = MethodMock
        return self.__dict__[name]

    @classmethod
    def methods(self):
        return dir(self)

class AttributeMock(object):

    def __init__(self, default=None):
        self.value = default
        self.call_stack = []
        self.set_values = []
        self.get_count = 0

    def __set__(self, instance, value):
        self.value = value
        self.set_values.append(value)
        self.call_stack.append("set value: " + str(value))

    def __get__(self, instance, owner):
        self.call_stack.append("get value: " + str(self.value))
        self.get_count += 1
        return self.value


class MethodMock():

    def __init__(self):
        self.returns = None
        self.calls = []

    def __call__(self, *kargs, **kwargs):
        print 'calling method mock'
        self.calls.append(type('MockCall', (object,), {'args':kargs, "kwargs": kwargs}))

    def was_called():
        return len(self.calls) > 0

