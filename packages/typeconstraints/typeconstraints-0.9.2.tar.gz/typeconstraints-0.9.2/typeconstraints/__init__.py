#!/usr/bin/env python3
"""Type checking decorator lib for functions and methods.

This module provides a way to add runtime type assertions to functions and methods.
It provides a typeconstraints decorator that can be used to type-asert both method
arguments and return values.

Example:

    @typeconstraints([int,float],[bool])
    myfunction(arg1,arg2):
        if arg1*arg2 > 3.1415927:
            return True
        else:
            return False

The typeconstraints decorator takes two arguments:

    * A type-constraints list for the method arguments
    * A type-constraints list for the method return values.

Each type-constraint in each of these lists is allowed to be one of the following:

    * An actual type
    * A callable taking a single argument and returning a boolean.

This module also contains a set of predefined type-constraint callables:

    * NONNABLE   : For asserting arguments of a given type that may also ne None
    * ANYOF      : For asserting arguments that are allowed to be of one of a set of defined types.
    * ARRAYOF    : For asserting arguments that should be a list of elements of a fixed type
    * MIXEDDICT  : For asserting arguments that should be dict objects where named fields must have
                   fixed types.
    * MIXEDARRAY : For asserting arguments that should be list objects where elements at positions
                   must have fixed types.
"""
import inspect

def _check_callable(candidate):
    args = list(inspect.signature(candidate).parameters.keys())
    count = len(args)
    if count > 0 and args[0] == "self":
        count -= 1
    if count != 1:
        raise AssertionError("typeconstraint callable arguments should take just one argument")

def _check_typelist(typelist):
    if not isinstance(typelist, list):
        raise AssertionError("Typelist should be a list")
    #pylint: disable=consider-using-enumerate
    for index in range(0, len(typelist)):
        #pylint: enable=consider-using-enumerate
        if not isinstance(typelist[index], type) and not callable(typelist[index]):
            raise AssertionError("Typelist should contain only types and callables")
        if not isinstance(typelist[index], type) and callable(typelist[index]):
            _check_callable(typelist[index])

def _check_typedict(typedict):
    if not isinstance(typedict, dict):
        raise AssertionError("Typedict should be a dict")
    for key in typedict.keys():
        if isinstance(typedict[key], type) and not callable(typedict[key]):
            raise AssertionError("Typelist should contain only types and callables")
        if not isinstance(typedict[key], type) and  callable(typedict[key]):
            _check_callable(typedict[key])

def _check_arglist(arglist, typelist):
    _check_typelist(typelist)
    if len(arglist) != len(typelist):
        raise AssertionError("Number of types and number of argument don't match")
    #pylint: disable=consider-using-enumerate
    for index in range(0, len(arglist)):
        #pylint: enable=consider-using-enumerate
        ok, msg = _type_ok(arglist[index], typelist[index])
        if not ok:
            return False, "Argument number " + str(index) + " of type " + str(type(arglist[index])) + \
                    " match failure against typelist " + str(typelist) + " [" + msg + "]" 
    return True, ""

def _type_ok(arg, constraint):
    #Simple type constraint, argument should either be the same type or a derived
    # type of the one specified.
    if isinstance(constraint, type):
        if isinstance(arg, constraint):
            return True, ""
    else:
        #Alternatively a constraint may be a constraint checking function
        if callable(constraint):
            rval = constraint(arg)
            msg = ""
            if not rval and "error_msg" in dir(constraint):
                msg = constraint.error_msg
            return rval,msg
    return False, "Type constraint is neither a type nor a callable."

#Helper callable for arguments that have more than one valid type
#pylint: disable=too-few-public-methods
class ANYOF(object):
    """Helper type-constraint callable for allowing an argument to have any
    of a defined set of types"""
    def __init__(self, typelist):
        _check_typelist(typelist)
        self.typelist = typelist
        self.error_msg = ""
    def __call__(self, arg):
        for index in range(0, len(self.typelist)):
            ok, msg = _type_ok(arg, self.typelist[index])
            if ok:
                self.error_msg = ""
                return True
        self.error_msg = "Argument of type " + str(type(arg)) + " not ANYOF types: " + str(self.typelist)
        return False

#Helper callable for single type arguments that may also be specified as None
class NONNABLE(object):
    """Helper type-constraint callable for allowing an argument of a specific
    type to be allowed to have a None value"""
    def __init__(self, ntype):
        if isinstance(ntype, type) and not callable(ntype):
            raise AssertionError("Nonable must be instantiated with a type or callable argument.")
        if not isinstance(ntype, type) and callable(ntype):
            _check_callable(ntype)
        self.nonnable = ntype
        self.error_msg = ""
    def __call__(self, arg):
        self.error_msg = ""
        if isinstance(arg, type(None)):
            return True
        rval, msg = _type_ok(arg, self.nonnable)
        if not rval:
            self.error_msg = "Argument of type " + str(type(arg)) + " not NONNABLE type " + \
                    str(self.nonnable) + " [" + msg + "]"
        return rval

class MIXEDARRAY(object):
    """Helper type-constraint callable for allowing an list type argument to have
    distinct types per location in the list."""
    def __init__(self, typelist, maxsize=-1, pad_type=type(None)):
        _check_typelist(typelist)
        arglist_ok, msg = _check_arglist([maxsize, pad_type], [int, type])
        if not arglist_ok:
            raise AssertionError("MIXEDARRAY constructor assert error: [" + msg + "]" )
        self.typelist = typelist
        self.maxsize = maxsize
        self.pad_ok = maxsize > len(typelist)
        self.pad_type = pad_type
        self.error_msg = ""
    def __call__(self, arg):
        self.error_msg = ""
        if not isinstance(arg, list):
            self.error_msg = "Argument of type " + str(type(arg)) + " not MIXEDARRAY " + \
                    str(self.typelist)
            return False
        if len(arg) < len(self.typelist):
            self.error_msg = "Argument of type " + str(type(arg)) + " with length " + \
                    str(len(arg)) + "  not MIXEDARRAY " + str(self.typelist) 
            return False
        if self.maxsize != -1 and len(arg) > self.maxsize:
            self.error_msg = "Argument of type " + str(type(arg)) + " with length " + \
                    str(len(arg)) + "  not MIXEDARRAY " + str(self.typelist) + \
                    " with padding disabled"
            return False
        paddedtypelist = self.typelist[:]
        if len(arg) > len(self.typelist):
            if self.pad_ok:
                while len(paddedtypelist) < len(arg):
                    paddedtypelist.append(self.pad_type)
            else:
                self.error_msg = "Argument of type " + str(type(arg)) + " with length " + \
                    str(len(arg)) + "  not MIXEDARRAY " + str(self.typelist) + \
                    " with padding disabled"
                return False
        #pylint: disable=consider-using-enumerate
        for index in range(0, len(paddedtypelist)):
            #pylint: enable=consider-using-enumerate
            ok, msg = _type_ok(arg[index], paddedtypelist[index])
            if not ok:
                self.error_msg = "Argument of type " + str(type(arg)) + " with length " + \
                    str(len(arg)) + " and element " + str(index) + " of type " + \
                    str(type(arg[index])) + " not MIXEDARRAY " + str(self.typelist) + \
                    " with padding set to " + str(self.pad_type) + " and pad type " + \
                    str(self.pad_type) + " [" + msg + "]"
                return False
        return True

#Helper callable for dict arguments with typed named members.
class MIXEDDICT(object):
    """Helper type-constraint callable for allowing a dict type argument to have
    distinct types per named element in the dictionary."""
    def __init__(self, typedict, ignore_extra=False, optionals=None):
        _check_typedict(typedict)
        arglist_ok, msg = _check_arglist([ignore_extra, optionals], [bool, NONNABLE(ARRAYOF(str))])
        if not arglist_ok:
            raise AssertionError("MIXEDDICT constructor assert error: [" + msg + "]" )
        self.ignore_extra = ignore_extra
        self.typedict = typedict
        self.tdkeys = set(typedict.keys())
        if optionals is None:
            self.optionals = set()
        else:
            self.optionals = set(optionals)
        self.nonoptionals = self.tdkeys - self.optionals
        self.error_msg = ""
    def __call__(self, arg):
        self.error_msg = ""
        if not isinstance(arg, dict):
            self.error_msg = "Argument of type " + str(type(arg)) + " not MIXEDDICT " + \
                    str(self.typelist)
            return False
        akeys = set(arg.keys())
        extra = akeys - self.tdkeys
        if not self.ignore_extra:
            if extra:
                self.error_msg = "Argument of type " + str(type(arg)) + " not MIXEDDICT " + \
                    str(self.typedict) + " with only keys " + str(self.tdkeys) + \
                    ", extra keys:" + str(extra)
                return False
        missing = self.nonoptionals - akeys
        if missing:
            self.error_msg = "Argument of type " + str(type(arg)) + " not MIXEDDICT " + \
                    str(self.typedict) + " with mandatory keys " + str(self.nonoptionals) + \
                    ", missing keys:", str(missing)
            return False
        checkthese = akeys - extra
        for key in checkthese:
            ok, msg = _type_ok(arg[key], self.typedict[key])
            if not ok:
                self.error_msg = "Argument of type " + str(type(arg)) + " and named element '" + \
                        key + "' of type " + str(type(arg[key])) + " not MIXEDDICT " + \
                        str(self.typedict) + " [" + msg + "]"
                return False
        return True

#Helper callable for array arguments that should contain single type elements.
class ARRAYOF(object):
    """Helper type-constraint callable for allowing an list type argument with a set type
    for each of the elements in the list."""
    def __init__(self, etype, minsize=1, maxsize=-1):
        arglist_ok, msg = _check_arglist([etype, minsize, maxsize], [type, int, int])
        if isinstance(etype, type) and not callable(etype):
            raise AssertionError("ARRAYOF must be instantiated with a type or callable argument.")
        if not isinstance(etype, type) and callable(etype):
            _check_callable(etype)
        arglist_ok, msg = _check_arglist([minsize, maxsize], [int, int])
        if not arglist_ok:
            raise AssertionError("ARRAYOF constructor assert error: [" + msg + "]" )
        self.etype = etype
        self.minsize = minsize
        self.maxsize = maxsize
        self.error_msg = ""
    def __call__(self, arg):
        self.error_msg = ""
        if not isinstance(arg, list):
            self.error_msg = "Argument of type " + str(type(arg)) + " not ARRAYOF " + \
                    str(self.etype)
            return False
        if len(arg) < self.minsize:
            self.error_msg = "Argument of type " + str(type(arg)) + "with length " + \
                    len(arg) + " to short for  ARRAYOF " + str(self.etype) + \
                    " with minimum length of " + str(self.minsize)
            return False
        if self.maxsize != -1 and len(arg) > self.maxsize:
            self.error_msg = "Argument of type " + str(type(arg)) + "with length " + \
                    str(len(arg)) + " to long for  ARRAYOF " + str(self.etype) + \
                    " with maximum length of " + str(self.maxsize)
            return False
        ndx = 0;
        for argx in arg:
            ok, msg = _type_ok(argx, self.etype)
            if not ok:
                self.error_msg = "Argument of type " + str(type(arg)) + "with length " + \
                    str(len(arg)) + " and element number " + str(ndx) + " of type " + str(type(argx)) + \
                    " is not a valid ARRAYOF " + str(self.etype) + \
                    "because of invalid element type. [" + msg + "]"
                return False
            ndx += 1
        return True

class DICTOF(object):
    """Helper type-constraint callable for allowing a dict type argument with a set type
    for each of the elements in the dictionary."""
    def __init__(self,value_type=str,key_type=str):
        if isinstance(key_type, type) and not callable(key_type):
            raise AssertionError("DICTOF must be instantiated with types or callable arguments.")
        if not isinstance(key_type, type) and callable(key_type):
            _check_callable(key_type)
        if isinstance(value_type, type) and not callable(value_type):
            raise AssertionError("DICTOF must be instantiated with types or callable arguments.")
        if not isinstance(value_type, type) and callable(value_type):
            _check_callable(value_type)
        self.key_type = key_type
        self.value_type = value_type
        self.error_msg = ""
    def __call__(self,typedmap):
        self.error_msg = ""
        for key in typedmap.keys():
            ok, msg = _type_ok(key, self.key_type)
            if ok:
                val = typedmap[key]
                ok2, msg2 = _type_ok(val, self.value_type)
                if not ok2:
                    self.error_msg = "Dictionary element with key '" + str(key) + \
                            "' and type " + str(type(val)) + "in DICTOFF with value_type " + \
                            str(self.value_type) + " does not have a valid value type. [" + \
                            msg2 + "]"
                    return False
            else:
                self.error_msg = "Dictionary element in in DICTOFF with key_type of " + \
                        str(self.key_type) + " contains key of type " + str(type(key)) + "[" + \
                        msg + "]"
                return False
        return True

class DUCK(object):
    def __init__(self,original_duck):
        self.methods = set()
        self.argcount = dict()
        self.error_msg = ""
        for candidate in set(dir(original_duck)) - set(dir(object)):
            method = getattr(original_duck,candidate)
            if callable(method):
                self.methods.add(candidate)
                self.argcount[candidate] = len(list(inspect.signature(method).parameters.keys()))
    def __call__(self,other_duck):
        self.error_msg = ""
        methods2 = set()
        for candidate in set(dir(other_duck)) - set(dir(object)):
            if callable(getattr(other_duck,candidate)):
                method = getattr(other_duck,candidate)
                methods2.add(candidate)
        missing_methods = self.methods - methods2
        if missing_methods:
            self.error_msg = "Duck-typed argument object is missing at least one method:" + str(list(missing_methods))
            return False
        for methodname in self.methods:
            method = getattr(other_duck,methodname)
            argcount = len(list(inspect.signature(method).parameters.keys()))
            if argcount != self.argcount[methodname] - 1:
                self.error_msg = "Duck-typed argument object has a different argument count for " + methodname + " method." + str(argcount) + "!=" + str(self.argcount[methodname])
                return False
        return True


def typeconstraints(typelist, rvtype=None):
    """The typeconstraint decorator allows a function or method to be augmented with strict
    (run-time) type asserts for all passed function arguments and returned return values."""
    if __debug__:
        #typelist should be a valid list of types and/or callables
        _check_typelist(typelist)
        if rvtype != None:
            _check_typelist(rvtype)
        def _type_constraint_assert(typelist, kwtypelist, args, kwargs, name):
            #Make sure we don't check positional arguments that don't have type constraints
            maxarg = len(args)
            if maxarg > len(typelist):
                maxarg = len(typelist)
            #Check each positional argument
            for index in range(0, maxarg):
                ok, msg = _type_ok(args[index], typelist[index])
                if not ok:
                    if isinstance(typelist[index], type):
                        errstr = name + ":Indexed argument " + str(index) + " has type " + \
                                str(type(args[index])) + " but is expected to be of type " + \
                                str(typelist[index]) + " [" + msg + "]"
                    else:
                        errstr = name + ":Indexed argument " + str(index) + \
                                " did not pass constraint function checking by " + \
                                str(typelist[index].__class__) + " [" + msg + "]"
                    raise AssertionError(errstr)
            #Check each named argument
            for key in kwargs.keys():
                if not key in kwtypelist:
                    errstr = name + ":Unexpected named argument '" + key + "'"
                    raise AssertionError(errstr)
                ok, msg = _type_ok(kwargs[key], kwtypelist[key])
                if not ok:
                    if isinstance(kwtypelist[key], type):
                        errstr = name + ":Named argument '" + key  + "' has type " + \
                                str(type(kwargs[key])) + " but is expected to be of type " + \
                                str(kwtypelist[key]) + " [" + msg + "]"
                    else:
                        errstr = name + ":Named argument '" + key  + \
                                "'  did not pass constraint function checking by " + \
                                kwtypelist[key].__name__  + " [" + msg + "]"
                    raise AssertionError(errstr)
        def _type_constraint_assert_factory(original_function):
            #Create a key value version of the constraint type list using the argument spec
            # of the original function.
            args = args = list(inspect.signature(original_function).parameters.keys())
            if len(typelist) != len(args):
                raise AssertionError(original_function.__name__ + " with " + str(len(args)) + \
                        " arguments used with " + str(len(typelist)) + " typeconstraints")
            kwtypelist = dict()
            #pylint: disable=consider-using-enumerate
            for ind in range(0, len(typelist)):
                #pylint: enable=consider-using-enumerate
                kwtypelist[args[ind]] = typelist[ind]
            #Define and return the type constraint checking wrapper function
            def _type_constraint_assert_wrapper(*args, **kwargs):
                #Assert the type constraints before calling the wrapped function
                _type_constraint_assert(typelist, kwtypelist, args, kwargs,\
                        original_function.__name__)
                if rvtype is None:
                    return original_function(*args, **kwargs)
                else:
                    rval = original_function(*args, **kwargs)
                    if isinstance(rval, tuple):
                        rvlist = list(rval)
                    else:
                        rvlist = [rval]
                    _type_constraint_assert(rvtype, {}, rvlist, {}, original_function.__name__)
                    return rval
            return _type_constraint_assert_wrapper
        return _type_constraint_assert_factory
    else:
        def _type_constraint_null_factory(original_function):
            def _type_constraint_null_wraper(*args, **kwargs):
                return original_function(*args, **kwargs)
            return _type_constraint_null_wraper
        return _type_constraint_null_factory
