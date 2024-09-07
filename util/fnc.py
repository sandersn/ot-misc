from __future__ import nested_scopes
"""functional.py -- functional utility functions

Bienvenido a Pequeno Lisp!"""
import data_struct
from data_struct import car, cdr
import copy
from operator import not_, contains
from types import FunctionType
import sys
try:
    from operator import eq
except ImportError:
    eq = lambda x,y: x==y
def named(name, f):
    "Change f's name destructively if using Python > 2.3"
    if sys.version_info[0] >= 2 and sys.version_info[1] > 3:
        f.func_name = name
    return f
def fn_name(f):
    "Built-in functions do not have the attribute func_name"
    try:
        return f.func_name
    except AttributeError:
        return repr(f)
def uncurry(fn):
    """Make fn accept a single tuple (using *args syntax)

        Also aliased as star if you want to mirror Python syntax
        Provided in case you have to call a function with zipped data in
    a context that doesn't allow you to type a *. (See example)
    NOTE:Does not work with keyword args.
    The only use I can think of this is in replacement of
    itertools.starmap(fn, l)
    with the example. Of course, it will be slower because I *think* that itertools is a C module.
    But it looks a little more orthogonal. Hard to say.
    Example:
    >>> map(uncurry(lambda x,y,z:x+y+z), [(1,2,3), (2,3,4), (3,4,5)])
    [6, 9, 12]
    """
    return named('uncurry of %s' % fn_name(fn), lambda args: fn(*args))
star = uncurry
def cur(fn, *args):
    """split evalution in two, not real currying
    >>> def add(x,y): return x+y
    ... 
    >>> half_adder = cur(add, 4)
    >>> half_adder(5)
    9
    """
    return named('cur:%d of %s' % (len(args), fn_name(fn)),
                 lambda *rest:fn(*(args+rest)))
def flip(fn):
    """Invert the order in which fn's args are matched to its params
    NOTE:Does not work with keyword args.
    Example:
    >>> def sub(x,y): return x-y
    ...
    >>> sub(3,2)
    1
    >>> flip(sub)(3,2)
    -1
    """
    return named('flip of %s' % fn_name(fn), lambda *args: fn(*args[::-1]))
def compose(*fns):
    """fn...->fn -- compose fns into a single function
    Example:
    >>> def add2(x): return x+2
    ... 
    >>> def mul3(x): return x*3
    ...
    >>> add_then_mul = compose(mul3,add2)
    >>> mul_then_add = compose(add2,mul3)
    >>> add_then_mul(4)
    18
    >>> mul3(add2(4))
    18
    >>> mul_then_add(4)
    14
    >>> add2(mul3(4))
    14
    """
    fns = list(fns)
    name = 'compose of %s'  % ', '.join(map(fn_name, fns))
    fns.reverse()
    return named(name, lambda *args:reduce(lambda arg,fn:fn(arg),
                                           cdr(fns),
                                           car(fns)(*args)))
def negate(fn):
    """fn->fn--Negate the truth value of fn. (ad hoc composition of not and fn)
    The returned function will return bool.
    >>> is_zerolen = negate(len)
    >>> filter(is_zerolen, ([], [1], [2], [], [3])) #grab pointers to all currently empty lists
    ([], [])
    """
    return compose(not_, fn)
def ident(x):
    "any->any--The identity function. id is already taken in Python"
    return x
def iseq(x):
    "a'->fn::(a'->bool)--ad hoc currier for == (that is, __eq__)"
    return cur(eq, x)
def isin(l):
    "[a']->fn::(a'->bool)--ad hoc currier for in (that is, __contains__)"
    return cur(contains, l)
def _test():
    import doctest, fnc
    return doctest.testmod(fnc)
if __name__=='__main__':
    _test()
