from reflect import traced
@traced
def fact(n):
    if n==0:
        return 1
    else:
        return n * fact(n-1)
@traced
def odd(n):
    if n==0:
        return False
    else:
        return even(n-1)
#@traced
def even(n):
    if n==0:
        return True
    else:
        return odd(n-1)
def despatch(fndict, *params):
    """{fn:fn} | [(fn,fn)...]*any...->any -- return the results of the value function for the first key function that returns true

    The keys of fndict should be functions of the form
    params->bool
    The values of fndict should be functions that take no parameters (this may change).
    NOTE:You may also pass a list of doubles that would turn into the dict if you need to control the order in which
    the functions are evaluated. Otherwise, there is no guarantee as to the order in which the key functions will be evaluated.

    Essentially, this function is a nice way to avoid a giant if series. Instead, you can compartmentalise
    your code into functions.

    For example:
    >>> #To do inline lambda initialisation you MUST use the list of doubles syntax.
    >>> #The Python parser dies upon seeing lambda inside normal dictionary initialisation with : and ,
    >>> french_repairs = [(lambda col,sym: col==12 and sym==".", lambda: "Verb expected!"), (lambda col,sym:col==12 and sym=="N", lambda :"Noun phrase expected!")]
    >>> #but you can wrap it in a dict if you want (useful if you have lots of named functions to pass)
    >>> french_repairs_dict = dict(french_repairs)
    >>> despatch(french_repairs, 12, ".")
    'Verb expected!'
    >>> despatch(french_repairs_dict, 12, "N") #or using a dict
    'Noun phrase expected!'
    >>> despatch(french_repairs, 12, ">")
    >>> #returns None if nothing matches

    Notice that dicts do not guarantee order of matching, but lists of doubles do:
    >>> french_repairs.append((lambda col,sym:col==12 and sym==".", lambda: 'Another error!'))
    >>> french_repairs_dict = dict(french_repairs)
    
    Calls to despatch after this may not return the same results as the added function
    will never be called given french_repairs, but might be called given french_repairs_dict.
    """
    if isinstance(fndict,dict): fndict = fndict.items()
    for fnkey,fnval in fndict:
        if fnkey(*params):
            return fnval()
def memoise(fn, constants=()):
    """fn*[bool]->fn -- memoise given function

    constants is a list of bools telling whether each parameter in order should be
    considered for hashing (true if used, false if not).

    Memoisation is the construction of a lookup table on demand.
    New values are entered into the lookup table as needed.
    For example:
    >>> def complexfunc(x,y,z): print 'complex called!'; return x*y+z
    ... 
    >>> complexfunc(1,2,3)
    complex called!
    5
    >>> mem = memoise(complexfunc)
    >>> mem(1,2,3) #calls complexfunc the first time
    complex called!
    5
    >>> mem(1,2,3) #but just looks it up the second time
    5
    >>> #tell memoise that z is constant
    >>> mem = memoise(complexfunc, [True,True,False]) #(1,1,0) works just as well
    >>> mem(1,2,3)
    complex called!
    5
    >>> mem(1,2,2) #of course note we get wrong results when z is not constant
    5

    NOTE:Normally you do NOT want the memoised function to have side effects
    because it undermines the point of storing the results in a table. This example is
    thus for example purposes only. But x*y+z isn't a very complex calculation either.
    NOTE:This may have limitations due to hashability constraints. Caveat haxor.
    NOTE:Current version does not support keyword arguments. Improvements welcome!
    TODO:Fix this so that it separates tuple conversion into both? of them
    """
    memo = {}
    def runfunc(*params): #maybe need **kw here too?
        if params not in memo:
            memo[params] = fn(*params)
        return memo[params]
    def runfunc_constants(*params):
        hash_params = data_struct.tupleise([p for p,c in zip(params,constants) if c])
        if hash_params not in memo:
            memo[hash_params] = fn(*params)
        return memo[hash_params]
    if constants:
        return runfunc_constants
    else:
        return runfunc
def destructive(fn):
    "fn->fn!--make a function *of one argument* destructive"
    def inner(arg):
        arg = fn(arg)
    return inner
def undestructive(fn):
    "fn!->fn--make a function *of one argument* indestructive (shallow copy)"
    def inner(arg):
        newarg = copy.copy(arg)
        fn(newarg)
        return newarg
    return inner
