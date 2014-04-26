#MattysMocks

##Suggested Use

It is suggested that the main way to use this library is though the patch decorators.  Using a decorator removes the task of patching from the context of the test.  I believe this is desirable because it removes errors resulting from managing mocked objects and greatly increases the readability your tests.  
 

##MockObject 

    MockObject(method=[], attributes=[])

__methods__
    
* attribute_calls - returns a list of all gets and sets of attributes all
* all_calls - returns a list of all method and attribute calls
* Creates mocks for methods that have not yet been defined, but will return a warning for methods not defined
* ask a method directly about calls made to it

###MockMethod
__method__

* returns
* was_called
* calls

##Patch
###PatchObject
__methods__

* instances
* first_instance
* class_method_calls
* all_calls - all class method, instance method, and attribute calls
* all_method_calls - a list of all instance method calls
* all_attribute_calls




The PatchObject class creates a class like object.  While MockObject creates a replacement for object for instance level interactions.  PatchObject helps keep track of Class level interactions like class_methods and instances.   

    def test_patch_object(self):
        ClassLikeObject = PatchObject()
        
        ClassLikeObject.newclassmehtod()
        
        new_instance_mock = ClassLikeObject()
        new_instance_mock.somemethod()
        
        self.assertEqual(len(ClassLikeObject.class_method_calls), 1)
        self.assertEqual(ClassLikeObject.insances[0], new_instance)
        self.assertTrue(ClassLikeObject.instances[0].somemethod.was_called)
        
###patch.object decorator


Simple example 

    @patch.object('mock_these.parent_class.DumbClass')
    def test_simple_patch(self, dumb_patch):
        pc = ParentClass()
        pc.method_that_uses_dumb_class()
        
        self.assertEqual(len(dumb_patch.first_instance.calls), 1)
        
Add a method or override what it returns

    @patch.object('mock_these.parent_class.DumbClass', methods=['new_method'])
    def test_new_method(self, dumb_patch):
        dumb_instance = dumb_patch()
        dumb_instance.new_method # doesn't throw a warning
       
        self.assertTrue(dumb_instance.new_method.was_called)
        
    @patch.object('mock_these.parent_class.DumbClass', methods={'somemethod':"new return value"})
    def test_override_return(self, dumb_patch):
        pc = ParentClass()
        self.assertEqual(pc.method_that_return_value_for_dumb_some_method(), "new return value")

Adding attributes or set initial return values is simular to methods


    @patch.object('mock_these.parent_class.DumbClass', attributes=['new_attribute'])
    def test_new_attribute(self, dumb_patch):
        dumb_instance = dumb_patch()
        dumb_instance.new_attribute = "test thing" 
       
        self.assertEqual(len(dumb_patch.attribute_calls), 1)
        
    @patch.object('mock_these.parent_class.DumbClass', attributes={'someattribute':"initial value"})
    def test_attribute_with_initial_value(self, dumb_patch):
        dumb_instance = dumb_patch() 
        self.assertEqual(dumb_instance.someattribute, "initial value")
        self.assertEqual(len(dumb_patch.attribute_calls), 1)

The mock object will throw warnings for methods that aren't found on patched object.

        
###patch.function

TODO: doc for patch.function decorator

##templating
   
manually create a mock_object from template using the object.mock.
   
    templated_mock = object.mock(DumbClass)
    templated_mock_with_extra_stuff = object.mock(DumbClass, methods=[], attributes=[])
    
    
##Future effors
* allow for dynamic return values for methods
* 
