from util import lst, fnc, reflect
from itertools import izip
import inspect
import faith, mark
### eval ###
def marked(c):
    """mark constraints only take one argument. When the flexibility
    is no longer needed, it would be MUCH better to replace this with
    if c in faith.__dict__.itervalues(): return False
    elif c in mark.__dict__.itervalues(): return True
    else: raise AttributeError("Constraint not found in faith or mark modules")
    or make a wrapper class like I did in Caml
    """
    return 1==len(inspect.getargspec(c)[0])
def eval(c,cand,input):
    if marked(c):
        return c(cand)
    else:
        return c(input,cand)
### some constraints ###
id_everything = lambda x,y:x==y # needs to use Levenshtein distance
id_vc = fnc.cur(faith.ID, 'voice')
id_cont = fnc.cur(faith.ID, 'contin')
id_place = fnc.cur(faith.ID, 'place')
### main code ###
# maybe I could try just generating the possible bounding sets instead
# of looking at all candidate strings. unfortunately you can generate all
# the bounding sets you want but you still have to find a candidate that
# matches its profile. so you could START with a target violation profile
# and stop as soon as you find an example of it. Hacking Max and Dep to help
# specify the length of strings to look at might help this work well in
# practise.
def bounding_set(col):
    "[int] -> (int, int) which is a (bound, offset) pair"
    best = col[0]
    worst = col[0]
    for n in col:
        if n < best:  best = n
        elif n > worst: worst = n
    if best==worst:
        return best, 0
    else:
        return best+1, 1
def removen(l, i):
    return l[:i] + l[i+1:]
def remove_col(tab, i):
    return lst.transpose(removen(lst.transpose(tab), i))
def bounding_tree(tab):
    "set([vln]) -> ([vln], tree [vln]) where type a tree = (a, [a tree])"
    top_row = iter(tab).next()
    if len(tab)==1:
        return top_row, []
    if len(top_row)==1:
        return [lst.fst(bounding_set(map(lst.car, tab)))], []
    bounder = map(bounding_set, lst.transpose(tab))
    return (map(lst.fst, bounder),
            [bounding_tree(remove_col(filter(lambda row:row[i]==best-different,
                                             tab),
                                      i))
             for i,(best,different) in enumerate(bounder)])

def bounds(cand, (bound, children)):
    """A candidate is bounded if (1) if it is simply bounded by the current
    node's violation profile or (2) if it is bounded by
    one of the current node's children for which its violations are less than
    or equal to the current node's."""
    return (simply_bounds(cand, bound) or
            children and
            any(bounds(removen(cand, i), children[i])
                for i,(cn,bn) in enumerate(izip(cand,bound)) if cn < bn))
def simply_bounds(cand, bound):
    # this is not very efficient, but I'm not sure how to speed it up in
    # a nice way.
    return (any(bn < cn for cn,bn in izip(cand, bound)) and
            all(bn <= cn for cn,bn in izip(cand, bound)))
def eval_gen(i, cons, cand):
    return tuple([eval(c,cand,i) for c in cons])
def gen(i, o, cons):
    candidates = gen_strings(stop=len(o))
    first = candidates.next()
    vlns = eval_gen(i, cons, first)
    winners = {vlns:[first]}
    bounders = set([vlns])
    btree = bounding_tree(bounders)
    for cand in candidates:
        vlns = eval_gen(i, cons, cand)
        if not bounds(vlns, btree):
            winners.setdefault(vlns, []).append(cand)
            if vlns not in bounders:
                bounders.add(vlns)
                btree = bounding_tree(bounders)
                #print cand, ":", vlns, '(', len(winners), ')'
    for bound in bounders:
        if bounds(bound, btree):
            del winners[bound]
    return winners, bounders, btree
def gen_count_winners(i, o, cons):
    "Just count the winners of each type instead of recording them."
    candidates = gen_strings(stop=len(o))
    first = candidates.next()
    vlns = eval_gen(i, cons, first)
    winners = {vlns:1}
    bounders = set([vlns])
    btree = bounding_tree(bounders)
    for cand in candidates:
        vlns = eval_gen(i, cons, cand)
        if not bounds(vlns, btree):
            if vlns in winners:
                winners[vlns] += 1
            else:
                winners[vlns] = 0
            if vlns not in bounders:
                bounders.add(vlns)
                btree = bounding_tree(bounders)
                #print cand, ":", vlns, '(', len(winners), ')'
    for bound in bounders:
        if bounds(bound, btree):
            del winners[bound]
    return winners, bounders, btree
def gen_strings(start=0, stop=100, reverse=True):
    "Coming soon--the ability to specify your own alphabet!"
    alfa = 'abdefghijklmnoprstuvwz' # plus some utf-8 ones later
    if reverse:
        it = xrange(len(alfa)**stop - 1, -1, -1)
    else:
        it = xrange(len(alfa)**stop)
    for n in it:
        acc = []
        i = 1
        while i <= n:
            acc.append(alfa[(n // i) % len(alfa)])
            i *= len(alfa)
        yield ''.join(acc)
        while i < len(alfa)**stop:
            acc.append(alfa[0])
            i *= len(alfa)
            yield ''.join(acc)
def update_tuple(x, t, i):
    return tuple(x if i==j else y for j,y in enumerate(t))
def update_tuples(f, ts, i):
    return [update_tuple(x,t,i) for x,t in zip(f([t[i] for t in ts]), ts)]
def candidate_tree(tab):
    "set([(str,[vln])]) -> ([(str,[vln])], tree [(str,[vln])])"
    top_row = iter(tab).next()
    if len(tab)==1:
        return top_row, []
    if len(top_row[1])==1:
        return (tab,[lst.fst(bounding_set(map(lst.car,map(lst.snd,tab))))]), []
    bounder = map(bounding_set, lst.transpose(map(lst.snd, tab)))
    return ((tab,map(lst.fst, bounder)),
            [candidate_tree(update_tuples(lambda row:remove_col(row, i),
                                          filter(lambda (word,row):
                                                   row[i]==best-different,
                                                 tab),
                                          1))
             for i,(best,different) in enumerate(bounder)])
    return (map(lst.fst, bounder),
            [bounding_tree(remove_col(filter(lambda row:row[i]==best-different,
                                             tab),
                                      i))
             for i,(best,different) in enumerate(bounder)])
####### forward running gen ######
def gen_repair(i, marks, faiths):
    """This isn't all of gen, just the candidate generation. The evaluation
    will still have to be run."""
    os = set([i])
    isactive = True
    while isactive:
        lenbefore = len(os) # you can add yet another for as a trick to avoid
        os.update(lst.concat(m(o) for o in os for m in marks))
        os.update(lst.concat(f(i, o) for o in os for f in faiths))
        isactive = len(os)!=lenbefore # the expence of the concat
    return os
if __name__=="__main__":
    from pprint import pprint
    # only shows off Max and Dep
    # print tableau('foo', ('foo', 'foon', 'fo'), constraints)
    example = [[0, 1, 1, 3], [0, 3, 6, 1], [0, 6, 3, 1], [9, 9, 9, 0]]
    bt = bounding_tree(example)
##    assert bounds([0,1,1,3], bt) == ## False
##     assert bounds([0,1,1,1001], bt) == False
##     assert bounds([1,2,2,1], bt) == False
##     assert bounds([1,2,2,3], bt) == False
##     assert bounds([1,2,2,8], bt) == True

##     winners, bounds, boundingtree = gen_count_winners('inkomai', 'xxx',
##                                                       [faith.depIO,
##                                                        faith.maxIO,
##                                                        faith.depInitSigma,
##                                                        mark.onset])
##     print winners
##     #print winners.keys(), map(len, winners.itervalues())
##     print bounds
##     pprint(boundingtree)
