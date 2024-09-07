try: # 2.3 compatibility (set was not a builtin at the time)
    set([1])
except NameError:
    import sets
    set = sets.Set
def car(l):
    "Yeah, so I broke down and wrote car and cdr functions. Leave me alone!"
    return l[0]
def cdr(l):
    """I'm not addicted! errrrr I lie. Maybe I *am* addicted. -_-"""
    return l[1:]
def cadr(l):
    "hah! Don't insult me yet!"
    return l[1]
def fst((x,y)):
    "OK,now that I've implemented caml's fst and snd you are free to insult me"
    return x
def snd((x,y)):
    "and these don't cons either, unlike cdr above!"
    return y
def bifilter(fn, l):
    """fn*[]->([],[]) --Returns the two halves of a list, divided on whether fn returns True or False.

    True half is returned first so as to mimic filter if you want to ignore the second half.
    Same as
    return filter(fn, l), filter(not fn, l)

    >>> #divide everything into odd and even
    >>> bifilter(lambda x: x % 2, [1,2,3,4,5,6])
    ([1, 3, 5], [2, 4, 6])
    >>> #sort some IPs (note that max is used like an n-ary or here ^_^)
    >>> bifilter(lambda s: max([s.startswith(pre) for pre in ['192','127']]), ['192.0.0.255', '127.0.0.1', '172.120.16.201'])
    (['192.0.0.255', '127.0.0.1'], ['172.120.16.201'])
    >>> #sometimes everything might be true (or false), in which you'd probably be better off using filter
    >>> bifilter(lambda x: x < 100, [1,2,3,4,5])
    ([1, 2, 3, 4, 5], [])
    
    This code works properly with iterators, and is likely faster. The
    old code might be a little clearer."""
    t = []; f = []
    for x in l:
        if fn(x): t.append(x)
        else: f.append(x)
    return t,f
#OLD:
#    return filter(fn, l), filter(lambda x:not fn(x), l)
partition = bifilter
def split_step(step, l):
    """int*[]->[[]...]Divides l into step sublists. Each sublist contains every stepth element of l.

    This is equivalent to [l[i::step] for i in range(step)] in Python 2.3
    The old code is maintained to preserve compatibility with Python 2.2
    There are other ways to do this, like:
    [l[i:i+step] for i in range(step)], but this produces different results.
    If you like the other version better, try it out too.
    
    >>> split_step(3,[1,2,3,4,5,6,7])
    [[1, 4, 7], [2, 5], [3, 6]]
    >>> split_step(4,[1,2,3,4,5,6,7])
    [[1, 5], [2, 6], [3, 7], [4]]
    >>> #a real example: extracting the good stuff from a list into separate lists
    >>> #pretend you don't care about the dummy text
    >>> split_step(3, ['dummy', 12, False, 'text', 13, True, 'here', 14, False])
    [['dummy', 'text', 'here'], [12, 13, 14], [False, True, False]]
    """
    if step > len(l):
        return [l]
    else:
        return [[l[j] for j in range(i,len(l),step)] for i in range(step)]
def group(l, n):
    """I think this definition favours readability over efficiency - Kaleb"""
    if n<=0:
        raise ValueError("Group length is %i. Accepts positive numbers." % n)
    if len(l):
        return [[l[j] for j in range(i*n,(i+1)*n)] for i in range(len(l)/n)]
    else:
        return []
def window(l, n, inc=1):
    if n<=0 or inc<=0:
        raise ValueError("Window length and increment accept only positive numbers.")
    if len(l):
        return [l[j:j+n] for j in range(0,len(l),inc) if j+n<=len(l)]
    else:
        return []
def two_time(l):
    """[]->[] -- an list that steps through a list two at a time

    >>> " | ".join(["%s,%s" %(prev,next) for prev,next in two_time([1,2,3,4,5,6])])
    '1,2 | 2,3 | 3,4 | 4,5 | 5,6'
    
    This is just window 2, so I recommend that you use it instead.
    """
    return window(l, 2)
def unzip(ts):
    return zip(*ts)
transpose = unzip
def findif(fn, *ls):
    """fn*[]...->any -- Returns first item in l for which fn is true, None if none are.
    If you pass multiple lists, fn must return True given all items

    >>> findif(lambda x:x, ['', '', 'x', 'y'])
    'x'
    >>> findif(lambda x,mask: x > 3 and mask, [1,2,3,4,5], [1,1,0,0,1])
    (5, 1)
    >>> findif(lambda x: x > 13, [1,2,3,4,5])
    >>> #not found, so returns None
    """
    for args in unzip(ls):
        if fn(*args):
            if len(args)==1:
                return car(args)
            else:
                return args
def takewhile(f, l):
    "a->bool*[a]->[a]--requires a list, or something that supports index/slice"
    i = 0
    while i < len(l) and f(l[i]):
        i+=1
    return l[:i]
def every(pred, *ls):
    """fn*[]...->bool -- is pred true for all items in l?

    pred :: any->bool
    >>> all(lambda x: x>5, [7,8,9])
    True
    >>> all(lambda x: x>5, [3,7,8,9])
    False
    >>> all(lambda x: x>5, [])
    True
    """
    for args in zip(*ls):
        if not pred(*args):
            return False
    return True
def some(pred, *ls):
    """fn*[]...->bool -- is pred true for all items in l?

    pred :: any->bool
    >>> any(lambda x: x>5, [3,7,8,9])
    True
    >>> any(lambda x: x>5, [])
    False
    """
    for args in zip(*ls):
        if pred(*args):
            return True
    return False
def binary2nary(binary_test, l):
    return every(lambda (x,y):binary_test(x,y), window(l, 2))
def same(l):
    """[]->bool | any -- If all elements are equal, return the element, otherwise False

    Notes:
    Returns True for an empty list.
    Depends on == (__eq__) working properly

    Equivalent to reduce(lambda x,y:x==y and y, l)

    >>> same([1,1,1])
    1
    >>> same([1,0,1])
    False
    >>> same([False,False,False])
    True
    >>> same([0,0,0])
    True
    """
    return binary2nary(lambda x,y:x==y, l)
def avg(l):
    """[num]->num -- Average an iterator of numbers.

    Technically this can be anything that implements + and /.
    Mileage may vary for non-numerical objects, however.

    >>> avg([1,2,3,4])
    2.5
    >>> avg([1.0,2.0,3.0,4.0])
    2.5
    """
    total = len = 0
    for len,x in enumerate(l):
        total += x
    return total / (len + 1.0)
def avglists(*lists):
    """[[]...]->[num] -- Averages multiple lists of numbers

    >>> avglists([1,2,3], [4,5,6], [7,8,9])
    [2.0, 5.0, 8.0]
    """
    return map(avg, lists)
def cross(*ls):
    """[[]] -> [[]] Return all permutations of lists in n.

    Examples:
    >>> cross([1],[2,3],[3])
    [[1, 2, 3], [1, 3, 3]]
    >>> cross([1,2,3],[2],[3])
    [[1, 2, 3], [2, 2, 3], [3, 2, 3]]
    """
    if not ls:
        return [[]]
    else:
        rests = cross(*cdr(ls))
        acc = []
        for x in car(ls):
            acc.extend([[x]+rest for rest in rests])
        return acc
def append_unique(l1,l2):
    """[]*[]->[] -- Append to l1 items from l2 that weren't already there

    >>> append_unique([1,2,3],[2,3,4])
    [1, 2, 3, 4]
    >>> append_unique(['N', 'DET', 'ADJ'], ['V', 'N', 'DET'])
    ['N', 'DET', 'ADJ', 'V']

    NOTE:This function is non-destructive. The name is Lisp-style.
    Also, it relies on __eq__ to do the Right Thing.
    """
    acc1 = {}
    for x in l1:
        acc1[x] = False
    return l1 + filter(lambda x: x not in acc1, l2)
def mapn(fn,*ls):
    """fn*[]...->[] -- map a list extending it, not appending
    Can be called with multiple lists

    fn :: a->[b]
    This is different from map's usage, whose fn is :: a->b, not [b]

    >>> mapn(lambda x:[x+1,x+2,x+3], [3,4,5])
    [4, 5, 6, 5, 6, 7, 6, 7, 8]
    >>> mapn(lambda x,y:(x,y), [1,2,3], [4,5,6]) #multiple lists, like a flattening zip
    [1, 4, 2, 5, 3, 6]
    """
    acc = []
    for args in zip(*ls):
        acc.extend(fn(*args))
    return acc
def uniq(l):
    """[] -> [] -- Return a copy of l with all duplicates removed.

    >>> uniq([1,2,1])
    [1, 2]
    >>> uniq(["DET", "N", "V", "DET", "ADJ", "N"])
    ['DET', 'N', 'V', 'ADJ']

    NOTE:This function is non-destructive. The original documentation made this a bit unclear.
    Also, it relies on __eq__ to do the Right Thing.
    """
    acc = {}
    for x in l:
        if x not in acc:
            acc[x] = False
    return acc.keys()
def flatten(l):
    """[]->[] -- Convert all levels of nesting into a single list, consing as needed

    Examples will probably help the most:
    >>> flatten([1,[[2]]])
    [1, 2]
    >>> flatten([[[[[[[1]]]]],[2]],3,4,[[5],6]])
    [1, 2, 3, 4, 5, 6]

    Obviously, this function can be slow*, so be careful!
    *It's highly recursive and creates a new list for each level of recursion.
    """
    flat = []
    for x in l:
        if isinstance(x,list):
            flat += flatten(x)
        else:
            flat.append(x)
    return flat
def concat(ls):
    "[[a]] -> [a] -- Flatten one level of lists. All items MUST be lists."
    acc = []
    for l in ls:
        acc += l
    return acc
def in_all(x, ls):
    """a'*[]->bool -- Is x in all ls?
    
    >>> in_all(1, ([1],[1],[1]))
    True
    """
    return every(lambda l:x in l, ls)
def tails(l):
    "[a] -> [[a]] -- All subslices to end of the list"
    if l:
        acc = []
        for i in range(len(l)):
            acc.append(l[i:])
        return acc
    else:
        return []
def all_pairs(l):
    "[a] -> [(a,a)] -- All unique pairs of items in l"
    acc = []
    for i in xrange(len(l)):
        for j in xrange(i+1, len(l)):
            acc.append((l[i],l[j]))
    return acc
def maxby(f, l):
    """(a->int) -> [a] -- Return the maximum in l as defined by f.
    NOTE:maxby actually takes an iter, just like the builtin max.
    The name 'max' is a bit misleading since the definition of f can
    produce any item in the list, eg min can be implemented with
    f = lambda n:-n
    NOTE:As of Python 2.5, the built-in max has an argument 'key' that
    renders this utility obsolete."""
    it = iter(l)
    best = it.next()
    bestval = f(best)
    for x in it:
        val = f(x)
        if val > bestval:
            best = x
            bestval = val
    return best
def _test():
    import doctest
    doctest.testmod()
if __name__=="__main__":
    _test()
