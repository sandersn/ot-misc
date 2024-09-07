from ot import bounding_set, remove_col, simply_bounds
from util import lst
from util.lst import transpose, fst, snd, unzip, partition
from util.fnc import compose, iseq
def torder_josh(tab):
    "[(word,[vln])] -> set((word,word))"
    if len(tab)==1:
        return set()
    elif len(tab[0][1])==1:
        losers, winners = lst.partition(
            lambda (_,row):row[0]==bounding_set(lst.mapn(snd, tab))[0],
            tab)
        return set((l, w) for (l,_) in losers for (w,_) in winners)
    else:
        edges = set()
        for i,(best,different) in enumerate(map(bounding_set,
                                                transpose(map(snd, tab)))):
            words, rows = unzip(filter(lambda (_,row):row[i]==best-different,
                                       tab))
            edges.update(torder_josh(zip(words, remove_col(rows, i))))
        return edges
def torder(tab):
    """[(word,[vln])] -> set((word,word))
    where word=str and vln=int and edge=(word,word) and graph=set(edge)"""
    def run():
        return clean(find(tab)[0])
    def find(tab):
        if len(tab)==1 or len(tab[0][1])==1:
            return set(), set()
        torder, exclude = set(), set()
        for i,(best, different) in enumerate(map(bounding_set,
                                                 transpose(map(lst.snd,tab)))):
            winners, losers = partition(lambda (_,row):row[i]==best-different,
                                        tab)
            words, rows = unzip(winners)
            child_torder,child_exclude = find(zip(words, remove_col(rows, i)))
            exclude.update(child_exclude)
            torder.update(child_torder)
            for loser,_ in losers:
                exclude.update((winner,loser) for winner,_ in winners)
                torder.update((loser,winner) for winner,_ in winners)
        return torder - exclude, exclude
    def clean(torder):
        bounded_losers = set(loser for (loser,winner) in torder
                             if not simply_bounds(loser, winner))
        return set((loser,winner) for (loser,winner) in torder
                   if loser not in bounded_losers)
    return run()
from util import reflect
#@reflect.traced
def roundrobin(l):
    """[a]->[(a,[a])]--Capture the x/except(x,l) pattern
    implementation adapted from very clever Scheme code that assumes
    linked lists.  There may be a better way for Python's vector
    lists."""
    acc = []
    before = []; after = list(l)
    for x in l:
        del after[0]
        acc.append((x, before + after))
        before.append(x)
    return acc
def torder2(tabs):
    """Three cases:
    (1) Everybody has only one column left -> no new edges
    (2) Everybody has only one candidate left -> same as torder_node from Josh
    (3) Some have only one candidate left -> These are the winners.
        Add loser->winner edges and recur on the losers.
    This algorithm has a bug for this winner/loser set:
    [[('cos]t[me', (0, 0, 0, 1))],
     [('cos]t', (0, 0, 1, 1))]] = winners
    [[('cos]t[us', (1, 0, 0, 1)), ('cos][tus', (0, 1, 0, 0))]] = loser
    Adding the edges:
    set([('cos]t[us', 'cos]t'), ('cos]t[us', 'cos]t[me')])
    Only the second edge should be added.
    This seems to be symptomatic of a larger case, because only adding [0][0]
    of losers is clearly wrong as well. There are probably a whole case missing
    here that should have no edges added."""
    if all(len(tab[0][1])==1 for tab in tabs):
        return set()
    winners, losers = lst.partition(compose(iseq(1), len), tabs)
    if losers:
        edges = set((l[0],w[0][0]) for loser in losers for l in loser for w in winners)
        if ('cos]t[us', 'cos]t') in edges:
            print winners, losers, edges
        for i in range(len(losers[0][0][1])):
            tabs = []
            for tab in losers:
                bounds = map(bounding_set,transpose(map(lst.snd, tab)))
                words, rows = unzip(filter(lambda(_,row):row[i]==bounds[i][0]-bounds[i][1],#best-different,
                                           tab))
                tabs.append(zip(words, remove_col(rows, i)))
                edges.update(torder2(tabs))
        return edges
    else:
        # original case from torder_nodes
        for (winner, bound),rest in roundrobin(map(lst.car, winners)):
            if all(simply_bounds(vlns, bound) for (_,vlns) in rest):
                return set((loser,winner) for (loser,_) in rest)
            else:
                return set()
def candidate_trees_string(tabs):
    if all(len(tab[0][1])==1 for tab in tabs):
        return '<br/>'.join(map(format_tab, tabs))
    winners, losers = lst.partition(compose(iseq(1), len), tabs)
    if losers:
        children = []
        for i in range(len(losers[0][0][1])):
            tabs = []
            for tab in losers:
                bounds = map(bounding_set, transpose(map(lst.snd, tab)))
                words, rows = unzip(filter(lambda(_,row):row[i]==bounds[i][0]-bounds[i][1],
                                           tab))
                tabs.append(zip(words, remove_col(rows, i)))
            children.append(candidate_trees_string(tabs))
        return ('''<table border=1 bordercolor=black
        cellpadding=1 cellspacing=0
        <tr><td colspan=%s>%s</td></tr><tr><td>%s</td></tr></table>''' %
                (len(children), tabs, '</td><td>'.join(children)))
    else:
        return '<br/>\n'.join(map(format_tab, tabs))
def format_tab(tab):
    return '<br>\n'.join("%s &nbsp; %s" % entry for entry in tab)
if __name__=="__main__":
    for edge in torder_josh([('cost][us', [1,1,0,0,0,]),
                             ('cos]t[us', [0,1,0,0,1,]),
                             ('cos][tus', [0,0,1,0,0,]),
                             
                             ('cost][me', [1,0,0,0,0,]),
                             ('cos]t[me', [0,0,0,0,1,]),
                             ('cos][tme', [1,0,1,0,0,]),
                             
                             ('cost',     [1,0,0,0,0,]),
                             ('cos]t',    [0,0,0,1,1,])]):
        print edge
    print
    tabs = [[('cost][us', [1,1,0,0,0,]),
             ('cos]t[us', [0,1,0,0,1,]),
             ('cos][tus', [0,0,1,0,0,])],
            
            [('cost][me', [1,0,0,0,0,]),
             ('cos]t[me', [0,0,0,0,1,]),
             ('cos][tme', [1,0,1,0,0,])],
            
            [('cost',     [1,0,0,0,0,]),
             ('cos]t',    [0,0,0,1,1,])]]
    for edge in torder2(tabs):
        print edge
    print '<html><body><h2>A Very Important Announcement</h2>'
    print candidate_trees_string(tabs)
    print '</body></html>'
## best output so far:
## ('cos]t', 'cos]t[me')
## ('cost][us', 'cost')
## ('cost][us', 'cost][me')
## ('cos]t[us', 'cos]t[me')
    # --cost-us/cost-me/cost example from Anttila--
    # cost][us < 1 1 0 0 0 >
    # cos]t[us < 0 1 0 0 1 >
    # cos][tus < 0 0 1 0 0 >
    # cost][me < 1 0 0 0 0 >
    # cos]t[me < 0 0 0 0 1 >
    # cos][tme < 1 0 1 0 0 >
    # cost     < 1 0 0 0 0 >
    # cos]t    < 0 0 0 1 1 >
    # bounding tree:
"""
bounding tree just for /cost/
([1, 0, 0, 1, 1],
 [((0, 0, 1, 1), []),
  ([1, 0, 1, 1],
   [((0, 1, 1), []),
    ([1, 1, 1], [((1, 1), []), ((1, 0), []), ((1, 0), [])]),
    ((1, 0, 0), []),
    ((1, 0, 0), [])]),
  ([1, 0, 1, 1],
   [((0, 1, 1), []),
    ([1, 1, 1], [((1, 1), []), ((1, 0), []), ((1, 0), [])]),
    ((1, 0, 0), []),
    ((1, 0, 0), [])]),
  ((1, 0, 0, 0), []),
  ((1, 0, 0, 0), [])])

"""
"""
bounding tree just for /costme/
([1, 0, 1, 0, 1],
 [((0, 0, 0, 1), []),
  ([1, 1, 0, 1],
   [((0, 0, 1), []),
    ([1, 0, 1],
     [((0, 1), []), ([1, 1], [((1,), []), ((1,), [])]), ((1, 0), [])]),
    ([1, 1, 1],
     [((0, 1), []),
      ([1, 1], [((1,), []), ((1,), [])]),
      ([1, 1], [((0,), []), ((1,), [])])]),
    ([1, 1, 0],
     [([1, 0], [((0,), []), ((0,), [])]),
      ((1, 0), []),
      ([1, 1], [((0,), []), ((1,), [])])])]),
  ([1, 0, 0, 1],
   [((0, 0, 1), []),
    ([1, 0, 1],
     [((0, 1), []), ([1, 1], [((1,), []), ((1,), [])]), ((1, 0), [])]),
    ([1, 0, 1],
     [((0, 1), []), ([1, 1], [((1,), []), ((1,), [])]), ((1, 0), [])]),
    ((1, 0, 0), [])]),
  ([1, 0, 1, 1],
   [((0, 0, 1), []),
    ([1, 1, 1],
     [((0, 1), []),
      ([1, 1], [((1,), []), ((1,), [])]),
      ([1, 1], [((0,), []), ((1,), [])])]),
    ([1, 0, 1],
     [((0, 1), []), ([1, 1], [((1,), []), ((1,), [])]), ((1, 0), [])]),
    ([1, 0, 1],
     [([0, 1], [((0,), []), ((0,), [])]),
      ([1, 1], [((0,), []), ((1,), [])]),
      ((1, 0), [])])]),
  ([1, 0, 1, 0],
   [([0, 1, 0],
     [([1, 0], [((0,), []), ((0,), [])]),
      ((0, 0), []),
      ([0, 1], [((0,), []), ((0,), [])])]),
    ([1, 1, 0],
     [([1, 0], [((0,), []), ((0,), [])]),
      ((1, 0), []),
      ([1, 1], [((0,), []), ((1,), [])])]),
    ((1, 0, 0), []),
    ([1, 0, 1],
     [([0, 1], [((0,), []), ((0,), [])]),
      ([1, 1], [((0,), []), ((1,), [])]),
      ((1, 0), [])])])])
"""
"""
bounding tree for all three together
([1, 1, 1, 1, 1],
 [([1, 1, 1, 1],#1
   [([1, 1, 1],
     [([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [((1,), []), ((1,), [])]),
      ((1, 0), [])]), # 1-2-5
    ([1, 1, 1],
     [([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [([1], []), ([1], [])])]),
    ([1, 1, 1],
     [([1, 1], [((1,), []), ((1,), [])]),
      ([1, 1], [((1,), []), ([1], [])]),
      ((0, 1), [])]), # 1-4-5
    ((0, 1, 0), [])]), # 1-5
  ([1, 1, 1, 1],#2
   [([1, 1, 1],
     [([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [((1,), []), ((1,), [])]),
      ((1, 0), [])]), # 2-1-5
    ([1, 1, 1],
     [([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [((1,), []), ([1], [])]),
      ([1, 0], [([0], []), ([1], [])])]),
    ([1, 1, 1],
     [([1, 1], [((1,), []), ((1,), [])]),
      ([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [((1,), []), ([1], [])])]),
    ([1, 1, 0],
     [((1, 0), []), # 2-5-1
      ([1, 0], [([0], []), ([1], [])]),
      ([1, 1], [((1,), []), ([1], [])])])]),
  ([1, 1, 1, 1],#3
   [([1, 1, 1],
     [([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [([1], []), ([1], [])])]),
    ([1, 1, 1],
     [([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [((1,), []), ([1], [])]),
      ([1, 0], [([0], []), ([1], [])])]),
    ([1, 1, 1],
     [([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [([1], []), ([1], [])])]),
    ([1, 1, 0],
     [([1, 0], [([0], []), ([1], [])]),
      ([1, 0], [([0], []), ([1], [])]),
      ([1, 1], [([1], []), ([1], [])])])]),
  ([1, 1, 1, 1],#4
   [([1, 1, 1],
     [([1, 1], [((1,), []), ((1,), [])]),
      ([1, 1], [((1,), []), ([1], [])]),
      ((0, 1), [])]), # 4-1-5
    ([1, 1, 1],
     [([1, 1], [((1,), []), ((1,), [])]),
      ([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [((1,), []), ([1], [])])]),
    ([1, 1, 1],
     [([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [([1], []), ([1], [])])]),
    ([1, 1, 1],
     [((0, 1), []), # 4-5-1
      ([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [([1], []), ([1], [])])])]),
  ([1, 1, 1, 0],#5
   [((0, 1, 0), []), # 5-1
    ([1, 1, 0],
     [((1, 0), []), # 5-2-1
      ([1, 0], [([0], []), ([1], [])]),
      ([1, 1], [((1,), []), ([1], [])])]),
    ([1, 1, 0],
     [([1, 0], [([0], []), ([1], [])]),
      ([1, 0], [([0], []), ([1], [])]),
      ([1, 1], [([1], []), ([1], [])])]),
    ([1, 1, 1],
     [((0, 1), []), # 5-4-1
      ([1, 1], [((1,), []), ([1], [])]),
      ([1, 1], [([1], []), ([1], [])])])])])"""
    # < 1 1 1 1 1 >
    #  1: < 1 0 0 1 >
    #     < 0 1 0 0 >
    #     < 0 0 0 1 >
    #     < 0 0 1 1 >
    #  =  < 1 1 1 1 >
    #    1-2:=< 1 1 1 >
    #        1-2-3:=< 1 1 >
    #             1-2-3-4:=< 0 1 > !!
    #             1-2-3-5:=< 1 1 >
    #        1-2-4:=< 1 1 >
    #        1-2-4-3:=<
    #        1-2-4-5:=<
    #        1-2-5:=< 1 0 > !!
    #    1-3:=< 1 1 1 >
    #    1-4:=< 1 1 1 >
    #    1-5:=< 0 1 0 > !!
    #  2:=< 1 1 1 1 >
    #  3:=< 1 1 1 1 >
    #  4:=< 1 1 1 1 >
    #  5:=< 1 1 1 0 >
