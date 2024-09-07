"""data_struct.py -- data structure manipulation functions"""
##from __future__ import generators
from __future__ import nested_scopes
import sys
from dct import *
from lst import *
## def alternator(*args):
##     """alternate between args infinitely

##     >>> colours = alternator(1,2,3) #pretend 1 is blue and 2 is brown, etc
##     >>> map(lambda x: colours.next(), range(7))
##     [1, 2, 3, 1, 2, 3, 1]
    
##     NOTE:This is a copy of itertools.cycle with slight differences:
##         1.alternator has a star interface, and thus assumes it will be passed an evaluated list, not a partially evaluated generator.
##         2.cycle evaluates the passed iterator in its first loop and uses that list afterwards.
##         3.cycle returns if passed an empty iterator. alternator throws IndexError.
##         4.In the presence of an infinite iterator, alternator requires the generator
##             to be fully evaluated, and thus would never get to run. cycle would run, but try to soak
##             up all available memory.
##             Neither make sense since they both inherently alternate among finite enumerable choices.
##     I'm keeping this around for 2.2 compatibility, and because of the differences;
##     my code is simpler (to read and to use) and slightly less robust, for example.
##     """
##     cur = 0
##     while True:
##         yield args[cur]
##         cur +=1
##         cur %= len(args)
def swapif(b, t, f):
    """bool*any*any->(any,any)--swap order of t and f only if b is true

    >>> swapif(True, 'CHECKED', 'not')
    ('not', 'CHECKED')
    >>> swapif(False, 'CHECKED', 'not')
    ('CHECKED', 'not')
    """
    if b:
        return f,t
    else:
        return t,f
def flippair(t):
    "(any,any)->(any,any)--Flip the order of a double (pair)"
    return t[1],t[0]
def buildTree(root, fnconvert, fnchildren, fnadd):
    """Build one tree from another, given root<a>. Returns root<b>.

    root is the root of the tree<a>.
    fnconvert(node<a>) -> node<b>
    fnchildren(node<a>) -> sequence of children<a>
    fnadd(node<b>, sequence of children<b> to be added) -> node<b> with children<b> added
    Note that despite the template syntax used in this description, Python does *not* enforce types
    ahead of time, so there isn't any compile-time checking going on (unlike OCaML or something).

    This thing has been missing examples for a long time. Here they are at long last:
    >>> #in this example, <a> is A, and <b> is str. (This is a real-life use)
    >>> class A:
    ...     def __init__(self,tag,children):
    ...         self.tag = tag
    ...         self.children = children
    ...
    >>> #build a small tree<a>
    >>> a = A('root', [A('left', []), A('center', [A('center-left', []), A('center-right',[])]), A('right', [A('very-right', [])])])
    >>> buildTree(a, lambda a: a.tag, lambda a: a.children, lambda b,lb: "(" + b + ' '.join(lb) + ")")
    '(root(left) (center(center-left) (center-right)) (right(very-right)))'

    Right now, I don't see a good way to produce the following output, because buildTree can't track
    tab depths. However, I may add something like this later, depending on further work with HTML.
    '(root
        (left)
        (center
            (center-left)
            (center-right))
        (right
            (very-right)))'
    """
    def build(node1):
        return fnadd(fnconvert(node1), [build(ch) for ch in fnchildren(node1)])
    return build(root)
def monadic(root, f, ret, bind):
    """Build one complex type from another (this isn't really a monad as it
    stands, but it is close to an incorrectly factored one.)

    root :: a.
    f :: a -> b
    ret :: a -> [a] -- [a] should be a's children
    bind :: b * [b] -> b
"""
    def build(node):
        return bind(f(node), [build(ch) for ch in ret(node)])
    return build(root)

#alias backups/standard library functions for 2.2 compatibility
## major,minor,rev,status,smthn = sys.version_info
## if major < 2 or minor < 3: #this if will break for Python 3.1 and 3.2. Oh well. I'll fix it later
##     enumerate = enumerate_bak
dict_fromkeys = dict_fromkeys_bak
## else:
##     dict_fromkeys = dict.fromkeys
##     enumerate = enumerate
def _test():
    import doctest, data_struct
    return doctest.testmod(data_struct)
if __name__=="__main__":
    _test()
