"(Hayes 2001)"
from rcd import *
def lfcd(cols, specificity):
    promote, demote = favour(cols, compose(lose_disfav, snd),
                             markcol,
                             fav_active,
                             cur(specific, cols, specificity),
                             cur(autonomous, cols))
    if promote==[] or demote==[]:
        return add_stratum(cols, [])
    else:
        return add_stratum(promote, lfcd(filter_rows(promote, demote),
                                         specificity))
def favour(cols, *prins):
    def loop(cols, prin, *ps):
        if not ps:
            return prin(cols)
        else:
            succeed, fail = bifilter(prin, cols)
            if prin==fav_active and succeed==[]:
                return fail
            if succeed==[]:
                return loop(fail, *ps)
            elif len(succeed)==1 or prin==markcol:
                return succeed
            else:
                return loop(succeed, *ps)
    promote = loop(cols, *prins)
    return promote, keyedsetdiff(cols, promote, key=fst)
def specific(cols, specificity, col):
    if fst(col) in specificity:
        return specificity[fst(col)] in map(fst, cols)
    else:
        return False
def autonomous(cols, rest):
    rows = map(snd, cols)
    most_helpers = cur(countif, positive)
    return map(fst, plateau(sorted([(col, maxby(most_helpers,
                                                filterby(positive,
                                                         snd(col),
                                                         rows),
                                                test=lt)) \
                                    for col in rest],
                                   cmp=lt, key=compose(most_helpers,snd)),
                            key=snd))
##     ##
##     loop_cols = cols
##     last_prin = prins[-1]
##     for prin in prins[:-1]:
##         succeed, fail = bifilter(prin, loop_cols)
##         if prin=fav_active and succeed==[]:
##             promote = fail
##             break
##         elif not succeed:
##             loop_cols = fail
##         elif len(succeed)==1 or prin==markcol:
##             promote = succeed
##             break
##         else:
##             loop_cols = succeed
##     else:
##         promote = last_prin(cols)
# test (but only one...)
