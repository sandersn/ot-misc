"""Note: constraints (ought to) return the number of violations incurred
True/False is a degenerate case of this, but is confusing to read and
should be converted to int at some point
Markedness constraints look only at the output (or input), while
Faithfulness constraints compare the input and output"""
from util.cl import count, countifnot
from util.lst import fst, snd
from lev import *
from unifeat import phonemes
# TODO: Everything really ought to use features for such small data sets
def maxIO(i,o):
    return count(DEL, optimal(levenshtein(i,o)), key=fst)
def depIO(i,o):
    return count(INS, optimal(levenshtein(i,o)), key=fst)
def depInitSigma(i,o):
    return int(optimal(levenshtein(i,o))[0][0]==INS)
def ID(feature):
    return (lambda i,o:
              countifnot(lambda (type,(i_index, o_index)):
                           (phonemes[i[i_index]].get(feature)==
                            phonemes[o[o_index]].get(feature)),
                         filter(lambda a:a[0]==SUB,optimal(levenshtein(i,o)))))
### utilities ###
def powerset(l):
    return ([x for i,x in enumerate(l) if 2**i & n] for n in xrange(2**len(l)))
def rebuild(s, cs):
    "Did I mention how bad these implementations are?"
    cs.reverse()
    for (n, c) in cs:
        s = s[:n] + c + s[n:]
    return s
def remove_ns(l, ns):
    ns.reverse()
    l = list(l)
    for n in ns:
        del l[n]
    return l
def unaligned_chars(i, o, op):
    chars = []
    offset = 0
    for (type, (start,stop)) in optimal(levenshtein(i,o)):
        if type==op==DEL: # this is a lame hack.
            chars.append((start+offset, i[start]))
        elif type==op==INS: # but i[start] is oobounds for INS
            chars.append((start+offset, -1))
        if type==DEL:
            offset -= 1
        elif type==INS:
            offset += 1
    return chars
def revget(d, value, default=None):
    for k,v in d.items():
        if v==value:
            return k
    else:
        return default
def updated(d, src):
    d = dict(d)
    d.update(src)
    return d
def aligned_chars(i, o, feature):
    """let C = set(Con) in
    Con, Input -> Output, Cand
    C, Input -> Cand
    C, Input, Output -> Con (via Repair . RCD)
    Heiberg presents Con, Input -> Cand but she could have got Output from it
    too
    C, output -> ? (maybe Cand?) (maybe Con?)
    Con, output -> ? (maybe Cand?) (maybe input?)
    I don't think you'll ever get Input from Output, not without looking at
    multiple candidates. Otherwise the identity hypothesis overpowers
    everything else. But I could be wrong.
    """
    return ((stop, # do you like nesting as much as I like nesting?
             revget(phonemes,
                       updated(phonemes[o[stop]],
                               {feature:phonemes[i[start]].get(feature)}),
                       default=o[stop]))
            for type, (start, stop) in optimal(levenshtein(i,o))
            if type==SUB and
               phonemes[i[start]].get(feature)!=phonemes[o[stop]].get(feature))
### repairing constraints ###
def max_repair(i,o):
    return (rebuild(o, cs) for cs in powerset(unaligned_chars(i,o,DEL)))
def dep_repair(i,o):
    return (''.join(remove_ns(o, map(fst, cs)))
            for cs in powerset(unaligned_chars(i,o,INS)))
def dep_init_repair(i,o):
    if optimal(levenshtein(i,o))[0][0]==INS:
        yield o[1:]
def ID_repair(feature):
    """WARNING: I am not completely sure that I should smash the output char
    with the input char (using rebuild here) or just go through altering
    features. Need to write some tricky tests. eg align /kat/ [bat] with
    ID(vc) and the repair should be [pat] not [kat]. I think."""
    def id(i,o):
        return (rebuild(o,cs) for cs in powerset(aligned_chars(i, o, feature)))
    return id
if __name__=="__main__":
    assert maxIO('art','cat') == 1
    assert depIO('art','cat') == 1
    assert maxIO('bad','dog') == 2
    assert depIO('bad','dog') == 2
    assert maxIO('ant','anti') == 1

