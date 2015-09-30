import gc
import inspect

# from http://code.activestate.com/recipes/457665-debug-runtime-objects-using-gcget_objects/

exclude = [
    "function",
    "type",
    "list",
    "dict",
    "tuple",
    "wrapper_descriptor",
    "module",
    "method_descriptor",
    "member_descriptor",
    "instancemethod",
    "builtin_function_or_method",
    "frame",
    "classmethod",
    "classmethod_descriptor",
    "_Environ",
    "RuntimeError",
    "frozenset", "set",
    "method-wrapper",
    "MemoryError",
    "_Printer",
    "_Helper",
    "getset_descriptor",
    "weakref", "property", "cell", "staticmethod", "exceptions"
    ]

def dumpObjects():
    gc.collect()
    oo = gc.get_objects()
    for o in oo:
        if getattr(o, "__class__", None):
            name = o.__class__.__name__
            # print (name)
            if name not in exclude:
                try:
                    filename = inspect.getabsfile(o.__class__)
                    print "Object :", `o`, "..."
                    print "Class  :", name, "..."
                    print "defined:", filename, "\n"
                except TypeError:
                    pass

if __name__=="__main__":

    class TestClass:
        pass

    testObject1 = TestClass()
    testObject2 = TestClass()

    #from wx import Colour
    #color = Colour()

    dumpObjects()
