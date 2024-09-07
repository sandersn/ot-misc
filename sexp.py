### read sexp ###
import string
class _ref():
    """_ref is intended to allow state change of a variable, but it is only
    needed because of Python's bungled lexical scope (to be fixed in Py3000,
    yes we *know* but it's borken *now*.)"""
    def __init__(self, val):
        self.val = val
    def set(self, val):
        self.val = val
    def __call__(self, *args):
        return self.val
    def get(self):
        return self.val
def _atom(s):
    if s=="#t":
        return True
    elif s=="#f":
        return False
    elif s[0]=='"' and s[-1]=='"':
        return s[1:-1]
    else:
        try:
            return int(s)
        except ValueError:
            try:
                i,d = s.split('.')
            except ValueError:
                return s
            if i.isdigit() and d.isdigit():
                return float(s)
            else:
                return s
def read(s):
    comment = _ref(False)
    def reader(s):
        l = []
        w = _ref([])
        def push():
            if w():
                l.append(_atom(''.join(w())))
            w.set([])
        while True:
            try:
                c = s.next()
            except StopIteration:
                push()
                return l
            if comment():
                if c=='\n':
                    comment.set(False)
            elif c==';':
                push()
                comment.set(True)
            elif c=='(':
                push()
                l.append(read(s))
            elif c==')':
                push()
                if '.' not in l:
                    return l
                else:
                    i = l.index('.')
                    del l[i]
                    return tuple(l)
            elif c in string.whitespace:
                push()
            else:
                w().append(c)
    return reader(iter(s))
