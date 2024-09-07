map_ = map
filter_ = filter
zip_ = zip
reduce_ = reduce
def map(fn, d):
    """fn*{}->{} -- map a dict to another dict

    fn :: value->new_value

    >>> ans=map_dict(lambda v:v * 2, {'a':1, 'b':2, 'c':3})
    >>> ans=={'a': 2, 'c': 6, 'b': 4}
    True
    """
    e={}
    for k in d:
        e[k] = fn(d[k])
    return e
def map_keys(fn, d):
    """fn*{}->{}--map a dict's keys

    fn :: key->new_key"""
    e={}
    for k,v in d.items(): #d.iteritems():
        e[fn(k)] = v
    return e
def map_items(keymap, present, absent, d):
    """
    keymap :: key->key
    present :: key*val*val->val
    absent :: key*val->val"""
    e = {}
    for oldk,oldv in d.items():
        newk = keymap(oldk)
        if newk in e:
            e[newk] = present(oldk,oldv,e[newk])
        else:
            e[newk] = absent(oldk,oldv)
    return e
def filter_values(fn, d):
    """fn*{}->{} -- filter a dict by values

    fn :: value->bool (whether value should be kept)

    >>> ans=filter_dict_values(lambda x:x > 1, {'a':1, 'b':2, 'c':3})
    >>> ans=={'c': 3, 'b': 2}
    True
    """
    e={}
    for k,v in d.items(): #d.iteritems():
        if fn(v):
            e[k] = v
    return e
def filter_keys(fn, d):
    """fn*{}->{} -- filter a dict by keys

    fn :: key->bool (whether value should be kept)

    >>> ans=filter_dict_keys(lambda x:x in ['a','c'], {'a':1, 'b':2, 'c':3})
    >>> ans=={'c': 3, 'a': 1}
    True
    """
    e={}
    for k,v in d.items(): #d.iteritems():
        if fn(k):
            e[k] = v
    return e
filter = filter_keys #because with keys is the default
def filter_items(fn, d):
    """fn*{}->{} -- filter a dict by keys

    fn :: key*value->bool (whether value should be kept)

    >>> ans=filter_dict_items(lambda x,y:x in ['a','c'] and y > 1, {'a':1, 'b':2, 'c':3})
    >>> ans=={'c': 3}
    True
    """
    e={}
    for k,v in d.items(): #d.iteritems():
        if fn(k,v):
            e[k] = v
    return e
def zip(*ds,**kws):
    """*{}->{} -- zip all values in all dicts under one key in one dict

    Keys that do not exist in all dicts are not copied unless you pass
    default, in which case the values that are missing will be assigned
    the default value.
    
    >>> ans=zip_dict({'a':1,'b':2}, {'a':3, 'b':4})
    >>> ans=={'a': (1, 3), 'b': (2, 4)}
    True
    >>> ans=zip_dict({'a':1,'b':2}, {'a':3, 'b':4, 'c':5}, default=0)
    >>> ans=={'a': (1, 3), 'b': (2, 4), 'c':(0,5)}
    True
    """
    e={}
    if 'default' in kws:
        default = kws['default']
        for k in reduce_(set.__or__, map_(set,ds)):
            e[k] = tuple([d.get(k,default) for d in ds])
    else:
        for k in ds[0]:
            try:
                e[k] = tuple([d[k] for d in ds])
            except KeyError: pass
    return e
def extract(d, *keys):
    """{}*key...->{} -- a dictionary with just the items requested by key
    NOTE:Does not throw errors if a key is not in the dictionary
    >>> d=extract_dict({'real':100, 'info':256, 'xyzzy':17, 'blargle':43}, 'real', 'info')
    >>> d=={'real':100, 'info':256}
    True
    """
    return filter_keys(lambda k: k in keys, d)
def except_(d, *keys):
    """{}*key...->{} -- a dictionary without the items specified by key
    >>> d=except_dict({'real':100, 'info':256, 'xyzzy':17, 'blargle':43}, 'real', 'info')
    >>> d=={'xyzzy':17, 'blargle':43}
    True
    """
    return filter_keys(lambda k: k not in keys, d)
def reduce(present, absent, l, keymap=lambda x:x):
    """fn*fn*[]*fn->{} -- reduce a list to a dict

    present :: key*value->new_or_updated_value
    absent :: key->new_value
    keymap :: given the list item, produce the correct dictionary key
        defaults to identity

    See count_with_dict for examples of usage.
    """
    d = {}
    for k in l:
        j = keymap(k)
        if j in d:
            d[j] = present(k,d[j])
        else:
            d[j] = absent(k)
    return d
def count(l):
    """[a']->{a':int} -- Categorise items in a list, like wc
    
    NB:In Haskell this is just
    count_with_dict = dict_reduce \k,v->v+1 \k->0
    ...But Python doesn't give auto-currying...although I guess you could write
    count_with_dict = lambda l: reduce_dict(lambda k,v:v+1, lambda k:1, l)
    Although that's the effective equivalent of the below code, it's not the moral equivalent.
    Although theoretically superior, it loses in readability to the full func def.
    I grow to dislike typing the word lambda more and more, given alternatives like
    fn, def or \
    Audibly, however, lambda is great fun to say.

    EX:
    >>> ans = count_with_dict("aaabbc")
    >>> ans=={'a': 3, 'c': 1, 'b': 2}
    True
    >>> # But also...
    >>> ans=count_with_dict([1,2,1,1,1,1,1,2,1,0])
    >>> ans=={0: 1, 1: 7, 2: 2}
    True
    """
    return reduce(lambda k,v:v+1, lambda k:1, l)
def collapse(l, keymap=lambda x:x, valuemap=lambda x:x):
    """[]->{}--Collapse a list into a dictionary
        keymap :: x->x -- give the dictionary key for an item in the list
        valuemap :: x->x -- give the dict value for an item in the list
        both functions default to the identity function
    EX:
    >>> dict_collapse(range(5)+range(1,6))
    {0: [0], 1: [1, 1], 2: [2, 2], 3: [3, 3], 4: [4, 4], 5: [5]}
    >>> #ummmmmmm....this is REALLY useful when you need it.
    >>> #see collapse_pairs for an example use"""
    return reduce(lambda k,v:v+[valuemap(k)],lambda k:[valuemap(k)], l, keymap)
def collapse_pairs(pairs):
    "[(a',b')]->{a':[b']}--collapse a list of tuples w/duplicate values into a dict mapping onto a list of values"
    return collapse(pairs, lambda pair:pair[0], lambda pair:pair[1])
def dict_fromkeys_bak(ks, v=None):
    """[]*any->{}--create a dict mapping all keys to the same value
    NOTE:In 2.3, this is dict.fromkeys. Kept around for 2.2 compatibility
    NOTE:Does NOT copy v! Beware of this if passing a mutable value."""
    return dict([(k,v) for k in ks])
