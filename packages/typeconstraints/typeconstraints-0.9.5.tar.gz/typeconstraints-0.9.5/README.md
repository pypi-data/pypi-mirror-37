# typeconstraints
Simple Python decorator implementing basic type constraints

Note: This is a real early beta version, the API may still change a bit.

Usage:

```python
from typeconstraints import typeconstraints

#If we can't suffice with a type as constraints, helper functions are supported
def arr_of_int(arg):
    if not isinstance(arg, list):
        return False
    for ind in range(0,len(arg):
        if type(arg[ind]) != int:
            return False
    return True 

#Decorator list the types or constraint checking function for each function argument.
@typeconstraints([int,str,arr_of_int])
def simple_function(foo,bar,baz):
    pass

simple_function(42,"hi there",[1,1,2,3,5,8,13,21])

```

The typeconstraints comes with a number of predefined convenience callables. 
The following are tested to be currently functional. 

* NONNABLE(tc) : Attribute should either be either ve a valid value of type tc or None
* ANYOF(tc1,tc2) : Attribute should either be of type tc1 or of type tc2
* ARRAYOF(tc): Attribute should be a list and each element in the list should be of type tc.
* DICTOF(tcval,tckey=str): Attribute should be a dict. The keys should all be of type tckey
                           and the values of type tcval
* MIXEDARRAY(tclist,max\_size=-1,pad\_type=NoneType):
    Attribute should be an array filled with elements of the consecutive types defined in tclist.
    Optionally the list may be padded with element of type pad_type up to a size of max_size. 
* MIXEDDIX(tcdict,ignore\_extra=False,optionals=None):
    Attribute should be a dict with keys that match those in tcdict and values of the type defined
    for those keys in tcdict. Keys mentioned in optionals may be left out, but if they are there\
    their value type should match the definition. Keys not mentioned in tcdict can optionally be ignored.




