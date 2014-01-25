from object import  mock, MethodMock

#fn, path, attributes=[], methods=[]
def object(path, attributes=[], methods={}):
    module = __import__('.'.join(path.split('.')[:-1]) )
    original_class_name = path.split('.')[-1:][0]
    original_class = getattr(module, original_class_name)

    patch = PatchObject(template=original_class)
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

class PatchObject():
#, original_object,  attributes, methods
    def __init__(self, *args, **kwargs):
        self.mock = mock(*args, **kwargs)
        self.instances = []
        self.class_method_calls = []

    def __call__(self, *kargs, **kwargs):
        new_mock = self.mock()
        self.instances.append(new_mock)
        return new_mock

    def __getattr__(self, name):
        print 'getattr for patch object ' + name
        if name.startswith("__"):
            if name == "__dir__":
                return lambda: dir(self.mock)
            return getattr(self.mock, name)

        new_mock = MethodMock()
        return MethodMock()


    def first_instance(self):
        return self.instances[0]

