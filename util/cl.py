"""Common Lisp compatibility functions for Python.
Kind of like goopy, except actually copying Common Lisp instead of just
pretending to, and making useless references to it."""
from fnc import ident, negate
from operator import eq
from itertools import islice
def countif(f, l, fromend=False, start=0, end=None, key=ident):
    total = 0
    if fromend: l = reversed(l)
    for x in islice(l,start,end): # should use islice
        if f(key(x)):
            total += 1
    return total
def countifnot(f, l, fromend=False, start=0, end=None, key=ident):
    return countif(negate(f), l, fromend, start, end, key)
def count(x, l, fromend=False, start=0, end=None,
          key=ident, test=eq, testnot=None):
    if testnot:
        def pred(y):
            return not testnot(x,y)
    else:
        def pred(y):
            return test(x,y)
    return countif(pred, l, fromend, start, end, key)
def findif(f, l, fromend=False, start=0, end=None, key=ident):
    if fromend: l = reversed(l)
    for x in islice(l,start,end):
        if f(key(x)):
            return x
    return None
def findifnot(f, l, fromend=False, start=0, end=None, key=ident):
    return findif(negate(f), l, fromend, start, end, key)
def find(x, l, fromend=False, start=0, end=None,
          key=ident, test=eq, testnot=None):
    if testnot:
        def pred(y):
            return not testnot(x,y)
    else:
        def pred(y):
            return test(x,y)
    return findif(pred, l, fromend, start, end, key)
def positionif(f, l, fromend=False, start=0, end=None, key=ident):
    if fromend: l = reversed(l)
    for i,x in enumerate(islice(l,start,end)):
        if f(key(x)):
            if fromend:
                if end:
                    return end - i
                else:
                    return len(l) - i
            else:
                return start+i
    return None
def positionifnot(f, l, fromend=False, start=0, end=None, key=ident):
    return positionif(negate(f), l, fromend, start, end, key)
def position(x, l, fromend=False, start=0, end=None,
             key=ident, test=eq, testnot=None):
    if testnot:
        def pred(y):
            return not testnot(x,y)
    else:
        def pred(y):
            return test(x,y)
    return positionif(pred, l, fromend, start, end, key)
def search(l, sub):
    "KMP matching. TODO:Implement all the keyword args"
    pi = _prefix(sub)
    q = 0
    for i in range(len(l)):
        while q > 0 and sub[q] != l[i]:
            q = pi[q]
        if sub[q]==l[i]:
            q += 1
        if q==len(sub):
            return i - len(sub) + 1 #append to a list for searchall
def _prefix(pre):
    pi = [0]
    k = 0
    for p in islice(pre,1,None):
        while k > 0 and pre[k] != p:
             k = pi[k]
        if pre[k]==p:
            k += 1
        pi.append(k) #(pre[k]==p and k+1 or k) ... oops k+=1 still needed
    return pi
