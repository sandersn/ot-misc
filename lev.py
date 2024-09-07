from util.data_struct import avg
from util.lst import cross
from util import dct
from util.reflect import postmortem
from unifeat import unify
SUB = 'substitute'; DEL = 'delete'; INS = 'insert'
def _levenshtein(s1,s2,indel,(delete,insert,subst)):
    "[a]*[a]*float*(a->float)*(a->float)*(a->float) -> [[float]]"
    table = [[indel*i for i in range(len(s2)+1)]]
    for i,c1 in enumerate(s1):
        row = [(i+1)*indel]
        for j,c2 in enumerate(s2):
            row.append(min([table[-1][j+1]+delete(c1),
                            table[-1][j]+subst(c1,c2),
                            row[-1]+insert(c2)]))
        table.append(row)
    return table
def levenshtein(s1, s2):
    return _levenshtein(s1,s2, 1, (lambda _:1,
                                   lambda _:1,
                                   lambda c1,c2: 2 if c1!=c2 else 0))
def levenshtein_cons(s1, s2):
    def sub_cons(c1,c2):
        if c1.get('cons')!=c2.get('cons'):
            return 1000000
        elif c1!=c2:
            return 2
        else:
            return 0
    return _levenshtein(s1,s2, 1, (lambda _:1, lambda _:1, sub_cons))
def flevenshtein_cons(dst, src, avgdistance):
    return _levenshtein(dst, src, avgdistance, (lambda j: avgdistance,
                                                lambda i: avgdistance,
                                                featuredistance_cons))
def flevenshtein (dst, src, avgdistance):
    return _levenshtein(dst, src, avgdistance, (lambda j: avgdistance,
                                                lambda i: avgdistance,
                                                featuredistance))
def levenshtein_fancy(s,t,(ins,delt,sub)):
    def row(prev_row, (i,d)):
        def best(current_row, ((n_1,n),c)):
            m_1 = current_row[-1]
            return current_row + [min(ins(c)+m_1, sub(c,d)+n_1, delt(d)+n)]
        return reduce(best, zip(window(prev_row, 2), s), [i+1])
    return reduce(row, enumerate(t), range(len(s)+1))[-1]
def optimal(table):
    trail = []
    i = len(table) - 1
    j = len(table[0]) - 1
    while not (i == 0 and j == 0):
        subs = table[i-1][j-1]
        # finish early if at one of the edges
        if i==0:
            trail.extend([(INS, (0, k)) for k in range(j-1,-1,-1)])
            break
        else:
            delt = table[i-1][j]
        if j==0:
            trail.extend([(DEL, (k, 0)) for k in range(i-1,-1,-1)])
            break
        else:
            inst = table[i][j-1]
        best = min([delt,subs,inst])
        if subs==best:
            trail.append((SUB, (i-1, j-1)))
            i -= 1; j -= 1
        elif inst==best:
            trail.append((INS, (i, j-1))) # just j is significant
            j -= 1
        else:
            trail.append((DEL, (i-1, j))) # just i is significant
            i -= 1
    trail.reverse()
    return trail
class Properties():
    """Only type your properties once, in the __init__ parameter list.
    Doesn't work very well and is overly complicated. I should delete it."""
    def __init__(self, d):
        for k,v in d.items():
            if k=='self': continue
            def prop():
                def fget(self):
                    return self.__dict__["_"+k]
                def fset(self, v):
                    self.__dict__["_"+k] = v
                def fdel(self):
                    del self.__dict__["_"+k]
                return fget,fset,fdel
            self.__dict__["_"+k] = v
            self.__dict__[k] = property(*prop())
def init_attrs(self, d):
    "Only type your attributes once, in the __init__ parameter list"
    self.__dict__.update(d)
    del self.self
def mkstr(x):
    "utf-8-string | str | list -> utf-8-string"
    if isinstance(x, list):
        return ''.join(x)
    else:
        return x
class Rule():
    def __init__(self, pos, dst, src, before, after, word1, word2):
        word1 = mkstr(word1)
        word2 = mkstr(word2)
        type = 'none'
        init_attrs(self, locals())
    def __str__(self):
        return ('%s(%s): %s -> %s / %s_%s (%s %s)' %
                (self.type, self.pos, self.src, self.dst,
                 self.before, self.after, self.word1, self.word2))
    def to_html(self):
        return ('%s(%s): %s &rarr; %s / %s_%s (%s %s)' %
                (self.type, self.pos, self.src, self.dst,
                 self.before, self.after, self.word1, self.word2))
    __repr__ = to_html # this is wrong, but convenient
    def eq_all(self, other):
        return self.type==other.type and \
               self.pos==other.pos and \
               self.src==other.src and \
               self.dst==other.dst and \
               self.before==other.before and \
               self.after==other.after
    def hash_all(self):
        return hash(self.type) ^ hash(self.pos) ^ \
               hash(self.src) ^ hash(self.dst) ^ \
               hash(self.before) ^ hash(self.after)
    def hash_env(self):
        "hash rules with identical src/dst/pos the same"
        return hash(self.type) ^ hash(self.before) ^ hash(self.after)
    def eq_env(self, other):
        "rules are equal irrespective of position and src/dst segments"
        return self.type==other.type and \
               self.before==other.before and \
               self.after==other.after
    def hash_rule(self):
        "hash rules with identical before/after/pos the same"
        return hash(self.type) ^ hash(self.src) ^ hash(self.dst)
    def eq_rule(self, other):
        "rules are equal irrespective of position and surroundings"
        return self.type==other.type and \
               self.src==other.src and \
               self.dst==other.dst
    def hash_rule_smartenv(self):
        if self.before=="#": # but really we only want to do this if
            # the OTHER is also '#' too, but there is no other to compare to
            prefix = hash(self.after)
        elif self.after=="#":
            prefix = hash(self.before)
        else:
            prefix = hash(self.before) ^ hash(self.after)
        return (hash(self.type) ^ hash(self.src) ^ hash(self.dst) ^
                (0 if self.before=="#" or self.after=="#"
                 else hash(self.before) ^ hash(self.after)))
    def eq_rule_smartenv(self, other):
        """this is like eq_all except with smart equality on before/after
        or it's like eq_rule, except that some kinds of before/after are
        different."""
        return (self.type==other.type and
                self.src==other.src and
                self.dst==other.dst and
                (self.before==other.before=="#" or self.after==other.after=="#"
                 or (self.before==other.before and self.after==other.after)))
    # choose the appropriate hash/eq pair (default to all)
    # (client code is encouraged to change these itself as need dictates)
    __eq__ = eq_all
    __hash__ = hash_all
    def __iter__(self):
        yield self.type
        yield self.pos
        yield (self.src,self.dst)
        yield (self.before,self.after)
def setRuleCompare(method):
    names = 'all env rule rule/smartenv'.split()
    eqs = dict(zip(names,
                   [Rule.eq_all, Rule.eq_env,
                    Rule.eq_rule, Rule.eq_rule_smartenv]))
    hashes = dict(zip(names,
                      [Rule.hash_all, Rule.hash_env,
                       Rule.hash_rule, Rule.hash_rule_smartenv]))
    Rule.__eq__ = eqs.get(method, Rule.eq_all)
    Rule.__hash__ = hashes.get(method, Rule.hash_all)
class Sub(Rule):
    def __init__(self, pos, (dst,src), (before, after), word1, word2):
        Rule.__init__(self, pos, dst, src, before, after, word1, word2)
        self.type = SUB
class Del(Rule):
    def __init__(self, pos, dst, (before, after), word1, word2):
        Rule.__init__(self, pos, '', dst, before, after, word1, word2)
        self.type = DEL
class Ins(Rule):
    def __init__(self, pos, src, (before, after), word1, word2):
        Rule.__init__(self, pos, src, '', before, after, word1, word2)
        self.type = INS
def enviro(s1, s2, avgdistance=1, lev=flevenshtein):
    s = ["#"]+list(s1)+["#"] # this bounds checking is extraordinarily LAME
    t = ["#"]+list(s2)+["#"] # but it works
    def foo((action,(i,j))):
        i = i + 1
        j = j + 1
        if action==SUB:
            return Sub(i, (s[i],t[j]), (s[i-1],s[i+1]), s1, s2)
        elif action==DEL:
            return Del(i-1, s[i], (s[i-1],s[i+1]), s1, s2)
        elif action==INS:
            return Ins(i-1, t[j], (s[i-1],s[i]), s1, s2)
    return map(foo, optimal(lev(unify(s1), unify(s2), avgdistance)))
### feature-based levenshtein ###
def featuredistance(dst, src):
  "{str:bool}*{str:bool}->int"
  # DEBUG if dst.get('cons')!=src.get('cons'): print '!',
  unshared_features = set(dst) ^ set(src)
  dst = dct.except_(dst, *unshared_features)
  src = dct.except_(src, *unshared_features)
  return len(unshared_features) + len(set(dst.items()) ^ set(src.items()))/2
def avgdistance(w1, w2):
  "If w1 or w2 is nil, just compute the feature weight of the non-nil one"
  if w1 and w2:
      return avg (map(lambda _:featuredistance(*_), cross(w1, w2)))
  else:
      return sum(map(lambda _:featuredistance(_,{}), w1 or w2))
def totalavgdistance(lang1, lang2):
  return avg(map(avgdistance, lang1, lang2)) / 2
# this stuff is all a lame hack!
def featuredistance_cons(dst, src):
    "{str:bool}*{str:bool}->int -- Prevent matches between consonant and vowel"
    if dst.get('cons')!=src.get('cons'):
        return 1000000
    else:
        return featuredistance(dst, src)
def totalavgdistance_cons(lang1, lang2):
    return avg(map(avgdistance_cons, lang1, lang2)) / 2
def avgdistance_cons(w1, w2):
  "If w1 or w2 is nil, just compute the feature weight of the non-nil one"
  if w1 and w2:
      return avg (map(lambda _:featuredistance_cons(*_),
                      filter(lambda (c1,c2):c1.get('cons')==c2.get('cons'),
                             cross(w1, w2))))
  else:
      return sum(map(lambda _:featuredistance(_,{}), w1 or w2))
