#!/usr/bin/env python3
import inspect
import types

def typeconstraints(typelist):
    def type_ok(arg,constraint):
        #Simple type constraint, argument should either be the same type or a derived type of the one specified.
        if type(constraint) == type(bool):
            if type(arg) is constraint or isinstance(arg,constraint):
                return True
            else:
                return False
        else:
            #Alternatively a constraint may be a constraint checking function
            if callable(constraint):
                return constraint(arg)
            else:
                #May add other types later, for now only types and callables are supported.
                return False
    def type_constraint_assert(typelist,kwtypelist,args,kwargs,name):
        #Make sure we don't check positional arguments that don't have type constraints
        maxarg = len(args)
        if maxarg > len(typelist):
            maxarg = len(typelist)
        #Check each positional argument
        for index in range(0,maxarg):
            if not type_ok(args[index],typelist[index]):
                if type(typelist[index]) == type(bool):
                    errstr = name + ":Indexed argument " + str(index) + " has type " + str(type(args[index])) + " but is expected to be of type " + str(typelist[index])
                else: 
                    errstr = name + ":Indexed argument " + str(index) + " did not pass constraint function checking by " + typelist[index].__name__
                raise TypeError(errstr)
        #Check each named argument
        for key in kwargs.keys():
            if not key in kwtypelist:
                errstr = name + ":Unexpected named argument '" + key + "'"
                raise TypeError(errstr)
            if not type_ok(kwargs[key],kwtypelist[key]):
                if type(kwtypelist[key]) == type(bool):
                    errstr = name + ":Named argument '" + key  + "' has type " + str(type(kwargs[key])) + " but is expected to be of type " + str(kwtypelist[key])
                else:
                    errstr = name + ":Named argument '" + key  + "'  did not pass constraint function checking by " + kwtypelist[key].__name__
                raise TypeError(errstr)
    def factory(of):
        #Create a key value version of the constraint type list using the argument spec of the original function.
        aspec = inspect.getargspec(of)
        args = aspec.args
        if len(typelist) != len(args):
            raise TypeError(of.__name__ + " with " + str(len(args)) + " arguments used with " + str(len(typelist)) + " typeconstraints")
        kwtypelist = dict()
        for ind in range(0,len(typelist)):
            kwtypelist[args[ind]] = typelist[ind]
        #Define and return the type constraint checking wrapper function
        def wf(*args,**kwargs):
            #Assert the type constraints before calling the wrapped function
            type_constraint_assert(typelist,kwtypelist,args,kwargs,of.__name__)
            #Call the wrapped function
            return of(*args, **kwargs)
        return wf
    return factory

