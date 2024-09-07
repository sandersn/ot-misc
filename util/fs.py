"""fs.py -- file system utility functions

(except round_up_two, which doesn't really belong)"""
import cPickle
import os
def pprint(o):
    """Pretty prints dicts, lists, and tuples each element on its own line.

    Otherwise just prints object
    This is less complicated than the pprint module and loses some information

    >>> pprint(['t',2,'s',4]) #list
    t
    2
    s
    4
    >>> pprint({'a':3,'b':4, KeyError('c'):'c not found!'}) #dict
    a	3
    'c'	c not found!
    b	4
    >>> pprint(KeyError('c'))
    'c'
    """
    if isinstance(o, dict):
        print '\n'.join(['%s\t%s' % (sym,struct) for (sym,struct) in o.items()])
    elif isinstance(o, list) or isinstance(o, tuple):
        print '\n'.join([('%s' % i) for i in o])
    else:
        print o
def menuLoop(splash, help, menuitems, menufn=None):
    """str*str*{str:func}*func -> None -- A simple menu loop with 'x' or ' ' leaving it.
    
    splash -- the splash string. List product name and version, etc.
    help -- the help string. List the functions and which letter goes with what, preferably
    menuitems -- binds the string one types to the function it invokes.
    Strings should be one lowercase letter. This may change to something more flexible tho.
    (something like Unix's least-typing-required cmd line args)
    The optional menufn is called at each iteration of the menu display
    
    All functions :: None->None"""
    if menufn is None:
        menufn = lambda: None
    choice = 'blah'
    print splash
    print help
    while 1:
        menufn()
        choice = raw_input('%')
        if choice=='' or choice.lower()=='x': return
        choice = choice.lower()[0]
        if choice in menuitems:
            menuitems[choice]()
        else:
            print help
def process_file(inf, outf, fn):
    """str*str*fn -- process inf, writing the results to outf

    fn :: str->str (str is whole text of file)"""
    file(outf, 'w').write(fn(file(inf,'r').read()))
def process_file_lines(inf, outf, fn):
    """str*str*fn -- process inf by line, writing the results to outf

    fn :: str->str (str is single line of file)"""
    infile = file(inf, 'r')
    outfile = file(outf,'w')
    for line in infile:
        outfile.write(fn(line))
def process_file_vars(inf, outf, fn):
    """fn*str*str--process inf's pickled vars, writing them to outf
    (There are no restrictions on fn's type)"""
    save_vars(outf, fname, fn(*load_vars(inf)))
def slurp(fname):
    """str*int->[] --Unpickle variables from fname

    If there is only one variable, return it; otherwise return a list"""
    f = file(fname, 'rb')
    vars = []
    while True:
        try:
            vars.append(cPickle.load(f))
        except EOFError:
            break
    if len(vars)==1:
        return vars[0]
    else:
        return vars
##loadVars = load_vars #Also available under the name 'loadVars' (deprecated)
def dump(fname, *vars):
    """str*any... --Pickle vars to fname"""
    f = file(fname, 'wb')
    for v in vars:
        cPickle.dump(v,f, True)
    f.close()
def makedirs(path):
    "Make all dirs necessary to put the file at the end of path in its requested dir"
    parentpath = os.path.split(path)[0]
    if parentpath and not os.path.exists(parentpath):
        os.makedirs(parentpath)
    return path
def delete_dir(path):
    "recursively delete all subdirectories, files and then the directory itself"
    if os.path.exists(path):
        for f in os.listdir(path):
            if os.path.isdir(os.path.join(path, f)):
                delete_dir(os.path.join(path, f))
            else:
                os.remove(os.path.join(path, f))
        os.rmdir(path)
def round_up_two(n):
    """int->int -- round up to nearest positive power of two

    For example:
    >>> round_up_two(3)
    4
    >>> round_up_two(24) #beware half powers of two because they are not the true power of two.
    32
    >>> round_up_two(8) #true powers of two are not affected
    8
    >>> round_up_two(0) #0 and below go to 1, the nearest positive power of two
    1
    
    WARNING! Apparently longs won't work right until Python 2.4! So this:
    round_up_two(123123343423312)
    doesn't work right yet. It just rolls the bits or something. Probably one could fix this
    with a check for negative inside the loop and converting to long instead.
    Plus I'm sure there is a magical bit equation that does this anyway. Oh well.
    """
    start = 1
    while start < n:
        start <<= 1
    return start
def with_cwd(path):
    "change directory and return a thunk that will restore the old directory"
    old = os.getcwd()
    if path!='': # rest of code will be a nop
        os.chdir(path)
    def restore():
        os.chdir(old)
    return restore
def with_module_wd(modulefile):
    "modulefile should be module.__file__"
    return with_cwd(os.path.split(modulefile)[0])
def _test():
    import doctest, console
    return doctest.testmod(console)
if __name__=="__main__":
    _test()
