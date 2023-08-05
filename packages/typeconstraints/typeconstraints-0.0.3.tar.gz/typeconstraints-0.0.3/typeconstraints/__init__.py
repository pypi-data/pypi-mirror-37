#!/usr/bin/env python3
import inspect
'Type checking decorator lib for functions and methods'

def _check_callable(candidate):
    aspec = inspect.getargspec(candidate)
    args = aspec.args
    count = len(args)
    if count>0 and args[0] == "self":
        count -= 1
    if count != 1:
        raise AssertionError("typeconstraint callable arguments should take just one argument")

def _check_typelist(tl):
    if not isinstance(tl, list):
        raise AssertionError("Typelist should be a list")
    for index in range(0, len(tl)):
        if type(tl[index]) != type(bool) and callable(tl[index]) is False:
            raise AssertionError("Typelist should contain only types and callables")
        if type(tl[index]) != type(bool) and callable(tl[index]):
            _check_callable(tl[index])

def _check_typedict(td):
    if type(td) != type(dict()):
        raise AssertionError("Typedict should be a dict")
    for key in td.keys():
        if type(td[key]) != type(bool) and callable(td[key]) == False:
            raise AssertionError("Typelist should contain only types and callables")
        if callable(td[key]):
            _check_callable(tl[index])

def _check_arglist(arglist,typelist):
    _check_typelist(typelist)
    if len(arglist) != len(typelist):
        raise AssertionError("Number of types and number of argument don't match")
    for index in range(0,len(arglist)):
        if _type_ok(arglist[index],typelist[index]) == False:
            return False
    return True

def _type_ok(arg,constraint):
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


#Helper callable for arguments that have more than one valid type
class ANYOF(object):
    def __init__(self,typelist):
        _check_typelist(typelist)
        self.typelist=typelist
    def __call__(self,arg):
        for index in range(0,len(self.typelist)):
            if _type_ok(arg,self.typelist[index]):
                return True
        return False

#Helper callable for single type arguments that may also be specified as None
class NONNABLE(object):
    def __init__(self,ntype):
        if type(ntype) != type(bool) and callable(ntype) == False:
            raise AssertionError("Nonable must be instantiated with a type or callable argument.")
        self.nonnable = ntype 
    def __call__(self, arg):
        if type(arg) == type(None):
            return True
        return _type_ok(arg,self.nonnable)

class MIXEDARRAY(object):
    def __init__(self,typelist,maxsize= -1, pad_ok=False, pad_type=type(None)):
        _check_typelist(typelist)
        _check_arglist([minsize,maxsize,pad_ok,pad_type],[int,int,bool,type(bool)])
        self.typelist = typelist
        self.maxsize = maxsize
        self.pad_ok = pad_ok
        self.pad_type = pad_type
    def __call__(self,arg):
        if not isinstance(arg,list):
            return False
        if len(arg) < len(typelist):
            return False
        paddedargs = args[:]
        if len(arg) > len(typelist):
            if self.pad_ok:
                while len(paddedargs) < len(typelist):
                    paddedargs.append(self.pad_type)
            else:
                return False
        for index in range(0,len(typelist)):
            if not _type_ok(arg[index],self.typelist[index]):
                return False
        return True

#Helper callable for dict arguments with typed named members.
class MIXEDDICT(object):
    def __init__(self,typedict,ignore_extra=False,optionals=[]):
        _check_typedict(typedict)
        _check_arglist([ignore_extra,optionals],[bool,ARRAYOF(str)])
        self.ignore_extra = ignore_extra
        self.typedict = typedict
        self.tdkeys = set(typedict.keys())
        self.optionals = set(optionals)
        self.nonoptionals = self.tdkeys - self.optionals
    def __call__(self,arg):
        if type(arg) != type(dict()):
            return False
        akeys =set(arg.keys())
        extra = self.tdkeys - akeys
        if self.ignore_extra == False:
            if len(extra) > 0:
                return False
        missing = self.nonoptionals - akeys
        if len(missing) > 0:
            return False
        checkthese = akeys - extra
        for key in checkthese:
            if _type_ok(arg[key],self.typedict[key]) == False:
                return False
        return True

#Helper callable for array arguments that should contain single type elements.
class ARRAYOF(object):
    def __init__(self,etype,minsize=1, maxsize=-1):
        if type(etype) != type(bool) and callable(etype) == False:
            raise AssertionError("ARRAYOF must be instantiated with a type or callable argument.")
        _check_arglist([minsize,maxsize],[int,int])
        self.etype = etype
        self.minsize = minsize
        self.maxsize = maxsize
    def __call__(self,arg):
        if type(arg) != type([]):
            return False
        if len(arg) < self.minsize:
            return False
        if self.maxsize != -1 and len(arg) > self.maxsize:
            return False
        for index in range(len(arg)):
            if _type_ok(arg[index],self.etype) == False:
                return False
        return True

def typeconstraints(typelist,rvtype=None):
    if __debug__:
        #typelist should be a valid list of types and/or callables
        _check_typelist(typelist) 
        if rvtype != None:
            _check_typelist(rvtype)
        def type_constraint_assert(typelist,kwtypelist,args,kwargs,name,is_rval=False):
            #Make sure we don't check positional arguments that don't have type constraints
            maxarg = len(args)
            if maxarg > len(typelist):
                maxarg = len(typelist)
            #Check each positional argument
            for index in range(0,maxarg):
                if not _type_ok(args[index],typelist[index]):
                    if isinstance(typelist[index],type):
                        errstr = name + ":Indexed argument " + str(index) + " has type " + str(type(args[index])) + " but is expected to be of type " + str(typelist[index])
                    else:
                        errstr = name + ":Indexed argument " + str(index) + " did not pass constraint function checking by " + str(typelist[index].__class__)
                    raise AssertionError(errstr)
            #Check each named argument
            for key in kwargs.keys():
                if not key in kwtypelist:
                    errstr = name + ":Unexpected named argument '" + key + "'"
                    raise AssertionError(errstr)
                if not _type_ok(kwargs[key],kwtypelist[key]):
                    if type(kwtypelist[key]) == type(bool):
                        errstr = name + ":Named argument '" + key  + "' has type " + str(type(kwargs[key])) + " but is expected to be of type " + str(kwtypelist[key])
                    else:
                        errstr = name + ":Named argument '" + key  + "'  did not pass constraint function checking by " + kwtypelist[key].__name__
                    raise AssertionError(errstr)
        def factory(of):
            #Create a key value version of the constraint type list using the argument spec of the original function.
            aspec = inspect.getargspec(of)
            args = aspec.args
            if len(typelist) != len(args):
                raise AssertionError(of.__name__ + " with " + str(len(args)) + " arguments used with " + str(len(typelist)) + " typeconstraints")
            kwtypelist = dict()
            for ind in range(0,len(typelist)):
                kwtypelist[args[ind]] = typelist[ind]
            #Define and return the type constraint checking wrapper function
            def wf(*args,**kwargs):
                #Assert the type constraints before calling the wrapped function
                type_constraint_assert(typelist,kwtypelist,args,kwargs,of.__name__)
                if rvtype==None:
                    return of(*args, **kwargs)
                else:
                    rval = of(*args, **kwargs)
                    if isinstance(rval,tuple):
                        rvlist = list(rval)
                    else:
                        rvlist = [rval]
                    type_constraint_assert(rvtype,{},rvlist,{},of.__name__,True)
                    return rval
            return wf
        return factory
    else:
        def fastfactory(of):
            def wf(*args,**kwargs):
                return of(*args, **kwargs)
            return wf
        return fastfactory


