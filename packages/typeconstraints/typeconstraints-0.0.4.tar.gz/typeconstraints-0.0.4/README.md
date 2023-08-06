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

* NONNABLE(int) : Attribute should either be an int or the value None
* ANYOF(int,float) : Attribute should either be an int or a float
* ARRAYOF(str): Attribute should be a list and each element in the list should be a string.

The following callables arent fully functional yet:

* MIXEDARRAY([str,int,bool],max\_size=20,pad\_ok=True,pad\_type=float)
* MIXEDDIX({"foo": str,"bar": float},ignore\_extra=True,optionals=["bar"])


