from operator import *
from util.lst import bifilter, some, every, unzip, concat, fst, snd
from util.fnc import *
from util.reflect import traced
from util.cl import countif, findif
import ot
from OTGrammar import RowTab, ColTab
## utils
def filterby(f, proxy, l):
    acc = []
    for x,p in zip(l,proxy):
        if f(p):
            acc.append(x)
    return acc
def maxby(f, l, test=gt):
    if l==[]: raise ValueError('maxby argument is empty list.')
    best = car(l)
    bestval = f(car(l))
    for x in cdr(l):
        val = f(x)
        if test(val, bestval):
            best = x
            bestval = val
    return best
def plateau(l, key=ident):
    if l==[]: return l
    i = 1
    first = key(car(l))
    while i < len(l) and key(l[i])==first:
        i += 1
    return l[:i]
## class Keyed():
##     "Wrapper to allow keying of items in a set. A gross hack, say some."
##     def __init__(self, key, x):
##         self.key = key
##         self.x = x
##     def __hash__(self):
##         return hash(self.key(self.x))
##     def __eq__(self, other):
##         return self.key(other.x)==other.key(other.x)
##     def get(self):
##         return self.x
def keyedsetdiff(xs, ys, key=ident):
    """used in bcd and lfcd. lfcd depends on order preservation for
    some reason, or I'd use the version below which is probably not O(n**2)
    (since set uses a hash algorithm internally, it's probably O(n))"""
    acc = []
    for x in xs:
        if not some(lambda y: key(x)==key(y), ys):
            acc.append(x)
    return acc
##     keyed = cur(Keyed, key)
##     return map(Keyed.get, set(map(keyed, xs)) - set(map(keyed, ys)))
## code
def table(cands, constraints, input):
    return [(c,[ot.eval(c,l,input) - ot.eval(c,w,input) for w,l in cands]) \
            for c in constraints]
positive = cur(lt, 0)
negative = cur(gt, 0)
win_fav = cur(some, positive)
tied = cur(every, lambda x:x==0)
lose_disfav = negate(cur(some,negative))
# maybe someday I should create a Col class....nahhhh
markcol = compose(ot.marked, fst)
fav_active = compose(win_fav, snd)
def add_stratum(promote, l):
    return [map(fst, promote)] + l
def filter_rows_(promote, demote):
    d = ColTab(demote)
    return RowTab(filterby(tied, ColTab(promote).violations, d.violations),
                  d.hierarchy)
def rcd_(tab):
    promote, demote = bifilter(compose(lose_disfav,snd), tab.col_tuples)
    if not promote or not demote:
        return add_stratum(tab.col_tuples, [])
    else:
        return add_stratum(promote, rcd_(filter_rows_(promote, demote)))
def filter_rows(promote, demote):
    return filter_rows_(promote, demote).col_tuples
def rcd(cols):
    return rcd_(ColTab(cols))
def nonrcd(cols):
    tab = ColTab(cols)
    strata = []
    while True:
        promote, demote = bifilter(compose(lose_disfav, snd), tab.col_tuples)
        if not promote or not demote:
            return list(reversed(add_stratum(tab.col_tuples, strata)))
        else:
            strata = add_stratum(promote, strata)
            tab = filter_rows_(promote, demote)
