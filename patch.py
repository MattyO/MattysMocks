from object import  mock, MethodMock
import warnings
import importlib

class PatchObject(object):
#, original_object,  attributes, methods
    def __init__(self, *args, **kwargs):
        self.mock_class = mock(*args, **kwargs)
        self.class_methods = {}
        self.instances = []

    def __dir__(self):
        return dir(self.mock_class)

    def __call__(self, *kargs, **kwargs):
        new_mock = self.mock_class()
        self.instances.append(new_mock)
        return new_mock

    def __getattr__(self, name):
        if name.startswith("__"):
            return getattr(self.mock_class, name)

        if name not in self.class_methods.keys():
            self.class_methods.update({name: MethodMock()})

        return self.class_methods[name]

    @property
    def class_method_calls(self):
        all_class_method_calls = []
        for class_method_name, method_object in self.class_methods.items():
            for call in method_object.calls:
                call.name = class_method_name
            all_class_method_calls += method_object.calls

        return all_class_method_calls

    @property
    def first_instance(self):
        if len(self.instances) == 0:
            return None

        return self.instances[0]

    @property
    def all_calls(self):

        all_calls = self.method_calls + self.attribute_calls
        all_calls = sorted(all_calls, key=lambda c: c.time)

        return all_calls

    @property
    def method_calls(self):
        all_calls = []
        all_calls += self.class_method_calls
        if self.first_instance != None: 
            all_calls += self.first_instance.method_calls

        all_calls = sorted(all_calls, key=lambda c: c.time)
        return all_calls

    @property
    def attribute_calls(self):
        all_calls = []
        for instance in self.instances:
            print instance.attribute_calls
            all_calls += instance.attribute_calls

        all_calls = sorted(all_calls, key=lambda c: c.time)

        return all_calls


def function(path,*args, **kwargs ):
    returns = kwargs.get("returns", None)
    kwargs.pop("returns", None)
    module_name, original_function_name = path.rsplit('.', 1)
    module = __import__(module_name, locals(), globals(), [original_function_name])
    #module = importlib.import_module('.'.join(path.split('.')[:-1]))
    original_function= getattr(module, original_function_name)
    function_mock = MethodMock(returns=returns)

    def wrapper(fn):
        def test_wrapped(self):
            setattr(module, original_function_name, function_mock)
            try:
                output = fn(self, function_mock)
            finally:
                pass
                setattr(module, original_function_name, original_function)
            return output
        return test_wrapped
    return wrapper

def object(path, attributes=[], methods={}):
    module_name, original_class_name = path.rsplit('.', 1)
    module = __import__(module_name, locals(), globals(), [original_class_name])
    #module = importlib.import_module('.'.join(path.split('.')[:-1]))
    original_class = getattr(module, original_class_name)
    #warnings.warn("path is " + path + " " + str(type(original_class)))

    patch = PatchObject(template=original_class, methods=methods, attributes=attributes)

    def wrapper(fn):
        def test_wrapped(self):
            setattr(module, original_class_name, patch)
            try:
                output = fn(self, patch)
            finally:
                setattr(module, original_class_name, original_class)
            return output
        return test_wrapped
    return wrapper


