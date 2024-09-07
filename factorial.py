import unittest
from util.lst import (unzip, transpose, window, same, partition, some, every,
                      fst, snd, cross, concat)
from util.reflect import traced, postmortem
from util.fnc import cur, negate
from operator import gt, sub
memo = set()
def factorial(n):
    total = 1
    for i in range(1,n+1):
        total = total * i
    return total
def mins(f, l):
    it = iter(l)
    try:
        bests = [it.next()]
    except StopIteration:
        return []
    bestval = f(bests[0])
    for x in it:
        val = f(x)
        if val < bestval:
            bestval = val
            bests = [x]
        elif val==bestval:
            bests.append(x)
    return bests
def extract(l, ixs):
    acc = []
    for i in ixs:
        acc.append(l[i])
    return acc
def not_same(l):
    return any(x!=y for x,y in window(l,2))
def indq(l,x):
    for i,y in enumerate(l):
        if x is y:
            return i
    raise ValueError('indq:%s not in list' % x)
def filterby(f, proxy, *ls):
    acc = [[] for _ in ls]
    for p,xs in zip(proxy, transpose(ls)):
        if f(p):
            for a,x in zip(acc,xs):
                a.append(x)
    if len(ls)==1:
        return acc[0]
    else:
        return acc
class Tab():
    def __init__(self, violations, constraints, candidates):
        self.cands = candidates
        self.con = constraints
        self.viols = violations
    def __eq__(self, other):
        return (self.cands==other.cands and
                self.con==other.con and
                self.viols==other.viols)
    def copy(self, violations=None, constraints=None, candidates=None):
        return Tab(violations if violations!=None else self.viols,
                   constraints if constraints!=None else self.con,
                   candidates if candidates!=None else self.cands)
    @property
    def cols(self):
        return Cols(self)
    def c_rows(self):
        return len(self.viols[0])
    def candidates(self):
        return tuple(self.cands)
    def constraints(self):
        return tuple(self.con)
    def sig(self):
        return tuple(self.cands),tuple(self.con)
    def __str__(self):
        return "{%s}x{%s}" % (' '.join(self.cands), ' '.join(self.con))
    __repr__ = __str__
    def rem(self, col):
        i = indq(self.viols, col)
        viols, con = list(self.viols), list(self.con)
        del viols[i]; del con[i]
        return self.copy(viols, con)
    def min_rows_by(self, col):
        best = col[0]
        bests = [0]
        for i,v in enumerate(col[1:]):
            if v < best:
                best = v
                bests = [i+1]
            elif v==best:
                bests.append(i+1)
        return self.copy([extract(col,bests) for col in self.viols],
                         candidates=extract(self.cands, bests))
    ### Hayes' method ###
    def filter_rows_by(demote, promote):
        cands, rows = filterby(tied, transpose(promote.viols),
                               promote.cands, transpose(demote.viols))
        return demote.copy(transpose(rows), candidates=cands)
    def rem_row(self, row):
        i = indq(self.viols, col)
        viols, con = list(self.viols), list(self.con)
        del viols[i]; del con[i]
        return self.copy(viols, con)
    def roundrobin(self):
        acc = []
        rows = transpose(self.viols)
        for i,(row,cand) in enumerate(zip(rows, self.cands)):
            cands = list(self.cands)
            rs = list(rows)
            del cands[i]; del rs[i]
            acc.append(((cand,row),
                        self.copy(transpose(rs), candidates=cands)))
        return acc
    def __car__(self):
        pass
    def __cdr__(self):
        pass
    def __cons__(self):
        pass
    def __append__(self):
        pass
class Cols(Tab):
    def __init__(self, other):
        self.viols = other.viols
        self.con = other.con
        self.cands = other.cands
    def __iter__(self):
        return iter(self.viols)
    def __len__(self):
        return len(self.viols)
    def indices(self, f):
        return set(i for i,col in enumerate(self.viols) if f(col))
    def extract(self, cols):
        self.viols = [self.viols[i] for i in cols]
        self.con = [self.con[i] for i in cols]
        return self
    def partition(self, f):
        tc,fc = [],[]
        tcol,fcol = [],[]
        for c, col in zip(self.con, self.viols):
            if f(col):
                tc.append(c)
                tcol.append(col)
            else:
                fc.append(c)
                fcol.append(col)
        return self.copy(tcol, tc), self.copy(fcol, fc)
class Relative(Tab):
    def __init__(self, winner, viols, con, cands):
        self.winner = winner
        Tab.__init__(self, viols, con, cands)
    def copy(self, violations=None, constraints=None, candidates=None):
        tab = Tab.copy(self, violations, constraints, candidates)
        tab.winner = self.winner
        return tab
## main algorithm ##
# @traced
def fact(C):
    assert not any(len(crit.cols)==0 or crit.c_rows()==0 for crit in C)
    assert same([crit.con for crit in C]), [crit.con for crit in C]
    acc = set()
    for cols in unzip([tab.cols for tab in C]):
        # fix a single constraint, then remove the candidates that are not
        # optimal for that constraint (this is like Eval and a little like RCD)
        crits = [tab.rem(col).min_rows_by(col) for col,tab in zip(cols,C)]
        assert all(len(crit.cols) > 0 for crit in crits), crits
        # quit if all tableaux have a single candidate for this constraint
        if all(crit.c_rows()==1 for crit in crits):
            acc.add(tuple([tab.cands[0] for tab in crits]))
        else:
            # find informative columns
            cols = reduce(set.union,
                          [tab.cols.indices(not_same) for tab in crits])
            # extract informative columns
            crits = [crit.cols.extract(cols) for crit in crits]
            if len(cols)==1:
                # harmonically bounded candidates can create redundant
                # single-column tableaux. In that case, just take the local
                # winner from each column
                acc.add(tuple([snd(min(zip(tab.viols[0], tab.cands)))
                               for tab in crits]))
            elif tuple(map(str, crits)) in memo:
                pass
##                 print 'memoisation skipped %s steps: %s'%(factorial(len(cols)),
##                                                           map(str, crits))
            else:
                # recursive step: continue on the remaining informative columns
                acc.update(fact(crits))
                memo.add(tuple(map(str, crits)))
    return acc
### Hayes' method ###
tied = cur(every)(lambda x:x==0)
negative = cur(gt)(0)
lose_disfav = negate(cur(some)(negative))
#@postmortem(RuntimeError)
def fastrcd(tab):
    """ if you want info on which constraints on not critical
    you can add back in the add_stratum here and throw False instead"""
    promote, demote = tab.cols.partition(lose_disfav)
    if not demote.viols:
        return True
    elif not promote.viols:
        return False
    else:
        return fastrcd(demote.filter_rows_by(promote))
    # non-recursive version
    promote,demote = tab.cols.partition(lose_disfav)
    while promote and demote:
        promote,demote = promote.filter_rows(demote).cols.partition(los_disfav)
    if not demote:
        return True
    elif not promote:
        return False
def relative(((winner,viols),rest)):
    "Create a relative tableau from an absolute one"
    return Relative(winner,
                    [[c-w for c in col] for w,col in zip(viols, rest.viols)],
                    rest.con, rest.cands)
def join(C):
    cands = concat([tab.cands for tab in C])
    viols = map(concat, transpose([tab.viols for tab in C]))
    return Relative(tuple(tab.winner for tab in C), viols, C[0].con, cands)
def hayesfact(C):
    "For all possible combinations of winners, see if they can succeed at RCD."
    tableaux = map(join, cross(*[map(relative, winnertabs)
                                 for winnertabs in map(Tab.roundrobin, C)]))
    return set(tab.winner for tab in tableaux if fastrcd(tab))
test = None
class TestFactorial(unittest.TestCase):
    def setUp(self):
        global memo
        global test
        memo = set()
        test = self.assertEqual
        self.rows = [[2,1,1,0],
                     [1,1,0,0],
                     [1,0,1,0]]
        self.abc = Tab([[2,1,1],
                        [1,1,0],
                        [1,0,1],
                        [0,0,0]],
                       '1 2 3 4'.split(),
                       'a b c'.split())
        self.jk = Tab([[0,0],
                       [1,0],
                       [1,1],
                       [0,1]],
                      '1 2 3 4'.split(),
                      'j k'.split())
        self.xyz = Tab([[0,0,1],
                        [0,1,0],
                        [1,0,0],
                        [0,0,1]],
                       '1 2 3 4'.split(),
                       'x y z'.split())
        # anttila 'cost' example
        self.cost = Tab([[1,0],
                         [0,0],
                         [0,0],
                         [0,1],
                         [0,1]],
                        '*Complex Onset Align-L-W Align-R-P Parse'.split(),
                        '[cost] [cos]t'.split())
        self.costus = Tab([[1,0,0],
                           [1,1,0],
                           [0,0,1],
                           [0,0,0],
                           [0,1,0]],
                        '*Complex Onset Align-L-W Align-R-P Parse'.split(),
                        '[cost][us] [cos]t[us] [cos][tus]'.split())
        self.costme = Tab([[1,0,1],
                           [0,0,0],
                           [0,0,1],
                           [0,0,0],
                           [0,1,0]],
                          '*Complex Onset Align-L-W Align-R-P Parse'.split(),
                          '[cost][me] [cos]t[me] [cos][tme]'.split())
        # relative tableau
        self.relative_abc_a = relative((('a', (2,1,1,0)),
                                        Tab([[1,1],
                                             [1,0],
                                             [0,1],
                                             [0,0]],
                                            '1 2 3 4'.split(),
                                            'b c'.split())))
        self.relative_abc_b = relative((('b', (1,1,0,0)),
                                        Tab([[2,1],
                                             [1,0],
                                             [1,1],
                                             [0,0]],
                                            '1 2 3 4'.split(),
                                            'a c'.split())))
        self.relative_abc_c = relative((('c', (1,0,1,0)),
                                        Tab([[2,1],
                                             [1,1],
                                             [1,0],
                                             [0,0]],
                                            '1 2 3 4'.split(),
                                            'a b'.split())))
    def testFactorial(self):
        test(factorial(4), 24)
        test(factorial(5), 120)
        test(factorial(0), 1)
        test(factorial(1), 1)
    def testMins(self):
        test(mins(lambda (f,s):f, [(1, 'boo'), (2,'bar'), (1, 'funk'), (4, 'jazz')]),
             [(1,'boo'), (1, 'funk')])
        test(mins(lambda x:x, []), [])
        test(mins(lambda n: n % 2, [1,2,3,4,4,5,9,02,99]),
             [2,4,4,2])
    def testTab(self):
        test(self.abc.candidates(), tuple('a b c'.split()))
        test(self.abc.con, '1 2 3 4'.split())
    def testMinByCols(self):
        test(self.abc.min_rows_by([2,1,1]), Tab([[1,1],
                                                 [1,0],
                                                 [0,1],
                                                 [0,0]],
                                                '1 2 3 4'.split(),
                                                'b c'.split()))
        test(self.abc, Tab([[2,1,1],
                            [1,1,0],
                            [1,0,1],
                            [0,0,0]],
                           '1 2 3 4'.split(),
                           'a b c'.split()))
        test(self.abc.rem(self.abc.viols[0]).min_rows_by([2,1,1]),
             Tab([[1,0],
                  [0,1],
                  [0,0]],
                 '2 3 4'.split(),
                 'b c'.split()))
        tmp = self.abc.rem(self.abc.viols[0]).min_rows_by([2,1,1])
        test(tmp.rem(tmp.viols[2]),
             Tab([[1,0],
                  [0,1]],
                 '2 3'.split(),
                 'b c'.split()))
        abc1 = tmp.rem(tmp.viols[2])
        test(abc1.min_rows_by([1,0]), Tab([[0],
                                           [1]],
                                          '2 3'.split(),
                                          'c'.split()))
        test(abc1.min_rows_by([0,1]), Tab([[1],
                                           [0]],
                                          '2 3'.split(),
                                          'b'.split()))
    def testOne(self):
        global memo
        test(set([('b',), ('c',)]), fact([self.abc]))
        test(memo, set([('{b c}x{2 3}',),
                        ('{a b c}x{1 2 3}',)]))
        memo = set()
        test(set([('j',), ('k',)]), fact([self.jk]))
        test(memo, set([('{j k}x{2 4}',)]))
        memo = set()
        test(set([('x',), ('y',), ('z',)]), fact([self.xyz]))
        test(memo, set([('{x y}x{2 3}',),
                        ('{y z}x{1 2 4}',),
                        ('{x z}x{1 3 4}',)]))
    def testAll(self):
        test(fact([self.abc,self.jk,self.xyz]),
             set([('b', 'j', 'y'),
                  ('b', 'k', 'y'),
                  ('b', 'k', 'z'),
                  ('c', 'j', 'x'),
                  ('c', 'k', 'x'),
                  ('c', 'k', 'z')]))
        test(fact([self.costus, self.costme, self.cost]),
             set([('[cost][us]', '[cost][me]', '[cost]'),
                  ('[cos]t[us]', '[cos]t[me]', '[cost]'),
                  ('[cos]t[us]', '[cos]t[me]', '[cos]t'),
                  ('[cos][tus]', '[cost][me]', '[cost]'),
                  ('[cos][tus]', '[cos]t[me]', '[cost]'),
                  ('[cos][tus]', '[cos]t[me]', '[cos]t')]))
    def testPartition(self):
        pass
    def testCopy(self):
        pass
    def testFilterBy(self):
        proxy = [0,1,1,0,1]
        n = [1,2,3,4,5]
        test(filterby(lambda x:x, proxy, n), [2,3,5])
        m = 'aloha'
        test(filterby(lambda x:x, proxy, n, m), [[2,3,5],'l o a'.split(' ')])
    def testFilterRows(self):
        promote = Tab([[1,1]],
                      '4'.split(),
                      'b c'.split())
        demote = Tab([[-1,-1],
                      [0,-1],
                      [-1,0]],
                     '1 2 3'.split(),
                     'b c'.split())
        empty = Tab([], '1 2 3'.split(), [])
        test(demote.filter_rows_by(promote).viols, empty.viols)
        test(demote.filter_rows_by(promote), empty)
        promote = Tab([[0,0]],
                      '4'.split(),
                      'b c'.split())
        stupid_eq = demote.filter_rows_by(promote)
        stupid_eq.viols = map(list, stupid_eq.viols)
        test(stupid_eq.viols, demote.viols)
        test(stupid_eq, demote)
    def testFastRCD(self):
        #pdb.set_trace()
        test(fastrcd(self.relative_abc_a), False)
        test(fastrcd(self.relative_abc_b), True)
        test(fastrcd(self.relative_abc_c), True)
    def testHayesOne(self):
        test(set([('b',), ('c',)]), hayesfact([self.abc]))
        #pdb.set_trace()
        test(set([('j',), ('k',)]), hayesfact([self.jk]))
        test(set([('x',), ('y',), ('z',)]), hayesfact([self.xyz]))
    def testHayes(self):
        test(hayesfact([self.abc,self.jk,self.xyz]),
             set([('b', 'j', 'y'),
                  ('b', 'k', 'y'),
                  ('b', 'k', 'z'),
                  ('c', 'j', 'x'),
                  ('c', 'k', 'x'),
                  ('c', 'k', 'z')]))
        test(hayesfact([self.costus, self.costme, self.cost]),
             set([('[cost][us]', '[cost][me]', '[cost]'),
                  ('[cos]t[us]', '[cos]t[me]', '[cost]'),
                  ('[cos]t[us]', '[cos]t[me]', '[cos]t'),
                  ('[cos][tus]', '[cost][me]', '[cost]'),
                  ('[cos][tus]', '[cos]t[me]', '[cost]'),
                  ('[cos][tus]', '[cos]t[me]', '[cos]t')]))
    def testRelative(self):
        test(self.relative_abc_a,
             Tab([[-1,-1],
                  [0,-1],
                  [-1,0],
                  [0,0]],
                 '1 2 3 4'.split(),
                 'b c'.split()))
    def testJoin(self):
        test(join([self.relative_abc_a]).viols, self.relative_abc_a.viols)
        test(join([self.relative_abc_a]), self.relative_abc_a)
if __name__=="__main__":
    unittest.main()

