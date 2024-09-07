# Note: constraints (ought to) return the number of violations incurred
# True/False is a degenerate case of this.
# Markedness constraints look only at the output (or input), while
# Faithfulness constraints compare the input and output
from itertools import izip
from util.lst import concat, cross
from util import lst, fnc, text
from unifeat import unify, phonemes
VOWELS = "aiueo" # super lame. Should go away
### constraints ###
def onset(o):
    return [syll[0]['cons'] for syll in syllabify(unify(o))].count(False)
def nuc(o):
    return [not any(not ph['cons'] for ph in syll) for syll in syllabify(unify(o))]
def onset_repair(o):
    def recreate_syllables(syllables):
    # this is kind of a hack ok to avoid returning feature structure
        i = 0
        acc = []
        for s in syllables:
            acc.append(o[i:i+len(s)])
            i += len(s)
        return acc
    ident = lambda syllable: syllable
    delete = lambda syllable: ''
    epenthesise = lambda syllable: 't' + syllable
    syllables = syllabify(unify(o))
    opss = cross(*[([ident] if syll[0]['cons'] else [ident,delete,epenthesise])
                   for syll in syllables])
    syllables = recreate_syllables(syllables)
    return (''.join(concat(op(syll) for op,syll in izip(ops,syllables)))
            for ops in opss)
def syllabify(phs):
    """state C ->  emit C; go {C(.) V}
    state V ->  emit V; go {V(.) CC CV(.) C$}
    state CC -> emit C.C; go {C(.) V}
    state CV -> emit CV; go {V(.) CC CV(.) C$}
    state C$ -> emit C; go {}"""
    phs = iter(phs)
    prev = {}
    try:
        ph = phs.next()
    except StopIteration:
        return []
    acc = []
    syllables = []
    def advanceCons():
        ph = phs.next()
        if ph['cons']:
            syllables.append(list(acc))
            acc[:] = []
            state = "C"
        else:
            state = "V"
        return ph, state
    def advanceVowel():
        ph = phs.next()
        if not ph['cons']:
            prev = {}
            syllables.append(list(acc))
            acc[:] = []
            state = "V"
        else:
            prev = ph
            try:
                ph = phs.next()
                if ph['cons']:
                    state = "CC"
                else:
                    syllables.append(list(acc))
                    acc[:] = []
                    state = "CV"
            except StopIteration:
                acc.append(prev)
                raise
        return ph, state, prev
    if ph['cons']==True:
        state = "C"
    else:
        state = "V"
    try:
        while True:
            if state=="C":
                acc.append(ph)
                ph, state = advanceCons()
            elif state=="V":
                acc.append(ph)
                ph, state, prev = advanceVowel()
            elif state=="CC":
                acc.append(prev)
                syllables.append(list(acc))
                acc = [ph]
                ph, state = advanceCons()
            elif state=="CV":
                acc.append(prev)
                acc.append(ph)
                ph, state, prev = advanceVowel()
    except StopIteration:
        syllables.append(list(acc))
    return syllables
def star_unvc_obs (w):
    return lst.any(lambda _:'-'==phonemes[_].get('voice') and \
                            '-'==phonemes[_].get('contin'),
                w)
def ICC(f,w):
    "feature*word->bool -- Make sure consonant clusters all have feature f"
    def is_equal_feature((c1,c2)):
        return phonemes[c1].get(f)==phonemes[c2].get(f)
    return not lst.every(lambda _: lst.every(is_equal_feature,lst.window(_,2)),
                         split_seq(w,VOWELS))
 #the filter line is pretty hoky but not bad.
icc_vc = fnc.cur(ICC, 'voice')
icc_cont = fnc.cur(ICC, 'contin')
icc_place = fnc.cur(ICC, 'place')
def no_low(o):
    return o.count('a')
### utils ###
def split_seq(s, splits):
    "This is hoky and inefficient and not as cool (or confusing) as the Lisp version"
    return filter(fnc.negate(fnc.isin(splits)), text.split_save(s,splits))
