import random
from util.fnc import cur, flip, ident, compose, uncurry
from util.cl import positionif # but some others I used as well...
from operator import *
from util.reflect import traced
from util.lst import unzip, fst, snd, car, takewhile
## util ##
def memq(x, l):
    "I'm not completely sure this is needed, but using == could cause problems"
    for y in l:
        if x is y:
            return y
    return False
def bin_key(test, key):
    return named('%s key=%s' % (fn_name(test), fn_name(key)),
                 lambda x,y:test(key(x),key(y)))
## winner evaluation ##
def winner(cs):
    def loop(tab, start_col):
        new = list(set(tab) - set(worst_candidates(tab,start_col)))
        if not new or len(new)==1:
            raise StopIteration(new)
        else:
            return new
    try:
        return reduce(loop, range(len(car(cs))), cs)
    except StopIteration, e:
        return e.args[0]
nonzero = cur(ne, 0)
def worst_vln(l, **kws):
    return positionif(nonzero, l, **kws)
def worst_candidates(tab, start):
    worst = plateau(sorted(filter(lambda row:fst(row)==False,
                                  zip(map(lambda _:worst_vln(_, start=start),
                                          tab),
                                      tab)),
                           cmp=bin_key(cmp, car)),
                    key=car)
    return remove_best(worst, len(worst)==len(tab))
def remove_best(results, violation_on_all):
    "(list (index * row)) -> (list (index * row))"
    best = violation_on_all and min(map(uncurry(flip(ref)), results)) or 0
    # map(cadr ...)?
    return map(snd, filter(lambda (index, row): row[index]!=best, results))
def plateau(l, key=ident):
    return takewhile(lambda _: key(_)==key(car(l)), l)
### code ###
def gla(con, tabs, schedule):
  return reduce(lambda con,sch: gla_inner(con, tabs, *sch), schedule, con)
def gla_inner(con, tabs, n, plasticity, noise):
  for i in range(n):
      tab = random.choice(tabs)
      neo = perturb(con, noise)
      possible = winner(unzip(map(snd, sorted(zip(neo, unzip(map(snd,tab))),
                                              cmp=bin_key(compose(neg,cmp), lambda x:x[0][1])))))
      actual = snd(random.choice(filter(fst, tab)))
      if tuple(actual) not in possible:  #not memq(actual, possible):
          con = correct(neo, map(sub, car(possible), actual), plasticity)
  return con
def correct(con, w_l_d, plasticity):
  return map(lambda (c,score),direction:(c,score + sgn(direction)*plasticity),
             con, w_l_d)
def sgn(n):
    "I bet this is defined and I just don't know the name"
    return cmp(n, 0)
def perturb(con, noise):
    return map(lambda (c,score): (c,score+random.normalvariate(0, noise)), con)
## gla(map(lambda c:(c,100), 'onset *complex-onset *syll#?C *coda *?coda max-? max-V linearity id-io-syllabic max-oo? dep? id-br-syllabic max-br *low-glide align-stemL-syllL contiguity id-io-low id-br-long').split(),
##     read_sexp('ot_learning/ilokano.sexp'),
##     [(7000,2,10),
##      (7000,0.2,2),
##      (7000,0.2,0.2)])
[('onset', 481.78189580101525),
 ('*complex-onset', 3759.286696100135),
 ('*syll#?C', 2014.5384724270318),
 ('*coda', -1941.9899479646413),
 ('*?coda', 1034.5678444898392),
 ('max-?', -2170.2665502736718),
 ('max-V', 150.41326976407402),
 ('linearity', -710.26090259889963),
 ('id-io-syllabic', 1121.5560673435341),
 ('max-oo?', -131.99405516532966),
 ('dep?', 1124.7404916957873),
 ('id-br-syllabic', 659.37423533244748),
 ('max-br', 1077.3938947065224),
 ('*low-glide', 721.14898551096223),
 ('align-stemL-syllL', -886.96334770031774),
 ('contiguity', -435.31900160029249),
 ('id-io-low', 664.11894349968463),
 ('id-br-long', 748.54869274505268)]
