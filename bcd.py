import ot
from rcd import *
## util ##
def subsets(l, n):
    """[a] -> [[a]] -- All order-independent subsets of l of
length n. Don't pass n=0; you'll get spurious results, not []
NOTE:This emulates sets. Shouldn't it USE sets?"""
    if len(l) < n:
        return []
    elif n==1:
        return [[x] for x in l] # I don't think map(list,l) is safe
    elif len(l)==1:
        return [l]
    else:
        return map(lambda rest: [car(l)]+rest, subsets(cdr(l), n-1)) + \
               subsets(cdr(l), n)
## code ##
def bcd(cols, speculative=False, prev=None, acc=[]):
    if prev:
        acc = add_stratum(prev, acc)
        cols = filter_rows(prev, cols)
    promote, demote = bifilter(compose(lose_disfav, snd), cols)
    if not promote: # crashed!
        return list(reversed(add_stratum(demote,acc)))
    else:
        m,f = bifilter(markcol, promote)
        if m:
            return bcd(f+demote, speculative, m, acc)
        elif not demote:
            return list(reversed(add_stratum(promote, acc)))
        elif speculative:
            return list(reversed(acc))
        elif some(fav_active, promote):
            x = min_subset(filter(fav_active, promote), cols)
            return bcd(demote+keyedsetdiff(promote, x, key=fst),
                       False, x, acc)
        else:
            return bcd(demote, False, promote, acc)
def min_subset(actives, cols):
    return best_set(findif(ident, [filter(lambda _:frees_mark(_, cols),
                                             subsets(actives, i)) \
                                      for i in range(1, len(cols))]),
                    cols)
def best_set(sets, cols):
    if len(sets)==1:
        return sets[0]
    else:
        return maxby(lambda _:len(filter(ot.marked,
                                         concat(bcd(filter_rows(_, cols),
                                                    True)))),
                      sets, test=gt)
def frees_mark(set, cols):
    return some(lambda (title, col): ot.marked(title) and win_fav(col),
                filter_rows(set, cols))
