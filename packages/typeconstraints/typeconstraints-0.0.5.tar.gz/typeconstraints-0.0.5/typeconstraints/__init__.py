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
        if not _type_ok(arglist[index], typelist[index]):
            return False
    return True

def _type_ok(arg, constraint):
    #Simple type constraint, argument should either be the same type or a derived
    # type of the one specified.
    if isinstance(constraint, type):
        if isinstance(arg, constraint):
            return True
    else:
        #Alternatively a constraint may be a constraint checking function
        if callable(constraint):
            rval = constraint(arg)
            return rval
    return False

#Helper callable for arguments that have more than one valid type
#pylint: disable=too-few-public-methods
class ANYOF(object):
    """Helper type-constraint callable for allowing an argument to have any
    of a defined set of types"""
    def __init__(self, typelist):
        _check_typelist(typelist)
        self.typelist = typelist
    def __call__(self, arg):
        for index in range(0, len(self.typelist)):
            if _type_ok(arg, self.typelist[index]):
                return True
        return False

#Helper callable for single type arguments that may also be specified as None
class NONNABLE(object):
    """Helper type-constraint callable for allowing an argument of a specific
    type to be allowed to have a None value"""
    def __init__(self, ntype):
        if isinstance(ntype, type) and not callable(ntype):
            raise AssertionError("Nonable must be instantiated with a type or callable argument.")
        self.nonnable = ntype
    def __call__(self, arg):
        if isinstance(arg, type(None)):
            return True
        return _type_ok(arg, self.nonnable)

class MIXEDARRAY(object):
    """Helper type-constraint callable for allowing an list type argument to have
    distinct types per location in the list."""
    def __init__(self, typelist, maxsize=-1, pad_type=type(None)):
        _check_typelist(typelist)
        _check_arglist([maxsize, pad_type], [int, type])
        self.typelist = typelist
        self.maxsize = maxsize
        self.pad_ok = maxsize > len(typelist)
        self.pad_type = pad_type
    def __call__(self, arg):
        if not isinstance(arg, list):
            return False
        if len(arg) < len(self.typelist):
            return False
        if self.maxsize != -1 and len(arg) > self.maxsize:
            return False
        paddedtypelist = self.typelist[:]
        if len(arg) > len(self.typelist):
            if self.pad_ok:
                while len(paddedtypelist) < len(arg):
                    paddedtypelist.append(self.pad_type)
            else:
                return False
        #pylint: disable=consider-using-enumerate
        for index in range(0, len(paddedtypelist)):
            #pylint: enable=consider-using-enumerate
            if not _type_ok(arg[index], paddedtypelist[index]):
                return False
        return True

#Helper callable for dict arguments with typed named members.
class MIXEDDICT(object):
    """Helper type-constraint callable for allowing a dict type argument to have
    distinct types per named element in the dictionary."""
    def __init__(self, typedict, ignore_extra=False, optionals=None):
        _check_typedict(typedict)
        _check_arglist([ignore_extra, optionals], [bool, ARRAYOF(str)])
        self.ignore_extra = ignore_extra
        self.typedict = typedict
        self.tdkeys = set(typedict.keys())
        if optionals is None:
            self.optionals = set()
        else:
            self.optionals = set(optionals)
        self.nonoptionals = self.tdkeys - self.optionals
    def __call__(self, arg):
        if not isinstance(arg, dict):
            return False
        akeys = set(arg.keys())
        extra = akeys - self.tdkeys
        if not self.ignore_extra:
            if extra:
                return False
        missing = self.nonoptionals - akeys
        if missing:
            return False
        checkthese = akeys - extra
        for key in checkthese:
            if not _type_ok(arg[key], self.typedict[key]):
                return False
        return True

#Helper callable for array arguments that should contain single type elements.
class ARRAYOF(object):
    """Helper type-constraint callable for allowing an list type argument with a set type
    for each of the elements in the list."""
    def __init__(self, etype, minsize=1, maxsize=-1):
        if isinstance(etype, type) and not callable(etype):
            raise AssertionError("ARRAYOF must be instantiated with a type or callable argument.")
        _check_arglist([minsize, maxsize], [int, int])
        self.etype = etype
        self.minsize = minsize
        self.maxsize = maxsize
    def __call__(self, arg):
        if not isinstance(arg, list):
            return False
        if len(arg) < self.minsize:
            return False
        if self.maxsize != -1 and len(arg) > self.maxsize:
            return False
        for argx in arg:
            if not _type_ok(argx, self.etype):
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
                if not _type_ok(args[index], typelist[index]):
                    if isinstance(typelist[index], type):
                        errstr = name + ":Indexed argument " + str(index) + " has type " + \
                                str(type(args[index])) + " but is expected to be of type " + \
                                str(typelist[index])
                    else:
                        errstr = name + ":Indexed argument " + str(index) + \
                                " did not pass constraint function checking by " + \
                                str(typelist[index].__class__)
                    raise AssertionError(errstr)
            #Check each named argument
            for key in kwargs.keys():
                if not key in kwtypelist:
                    errstr = name + ":Unexpected named argument '" + key + "'"
                    raise AssertionError(errstr)
                if not _type_ok(kwargs[key], kwtypelist[key]):
                    if isinstance(kwtypelist[key], type):
                        errstr = name + ":Named argument '" + key  + "' has type " + \
                                str(type(kwargs[key])) + " but is expected to be of type " + \
                                str(kwtypelist[key])
                    else:
                        errstr = name + ":Named argument '" + key  + \
                                "'  did not pass constraint function checking by " + \
                                kwtypelist[key].__name__
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
