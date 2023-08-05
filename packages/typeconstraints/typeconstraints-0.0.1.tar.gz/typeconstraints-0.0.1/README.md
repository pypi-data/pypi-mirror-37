# typeconstraints
Simple Python decorator implementing basic type constraints

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
@typeconstraints(int,str,arr_of_int)
def simple_function(foo,bar,baz):
    pass

simple_function(42,"hi there",[1,1,2,3,5,8,13,21])

```
