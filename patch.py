from object import  mock, MethodMock
import warnings
import importlib

class PatchObject(object):
#, original_object,  attributes, methods
    def __init__(self, *args, **kwargs):
        self.mock_class = mock(*args, **kwargs)
        self.instances = []
        self.class_method_calls = []

    def __dir__(self):
        return dir(self.mock_class)
    def __call__(self, *kargs, **kwargs):
        new_mock = self.mock_class()
        self.instances.append(new_mock)
        return new_mock

    def __getattr__(self, name):
        if name.startswith("__"):
            return getattr(self.mock_class, name)

        new_mock = MethodMock()
        return MethodMock()


    def first_instance(self):
        return self.instances[0]

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


