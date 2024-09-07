"""reflect.py -- reflection and function loading
Nathan, REMEMBER that find_function is just get_attr!
Do NOT recode this function over and over!"""
import text
import types
import fnc
from util.data_struct import car
_indent = 0
def traced(f):
    def tracer(*args, **kwargs):
        global _indent
        _indent += 1
        if kwargs:
            tmp = ", %s" % ', '.join(["%s=%r" % kv for kv in kwargs.items()])
        else:
            tmp = ''
        print "%s%s(%s%s)" % (' |'*_indent,
                              f.func_name,
                              ', '.join(map(repr,args)),
                              tmp)
        try:
            result = f(*args, **kwargs)
        except:
            _indent = 0
            raise
        print "%s%s" % (' |'*_indent, result)
        _indent -= 1
        return result
    tracer.func_name = 'traced-' +f.func_name
    return tracer
def postmortem(*exceptions):
    def deco(f):
        def trier(*args):
            try:
                return f(*args)
            except exceptions, e:
                print '%r\n%s(%s)' % (e, f.func_name,', '.join(map(repr,args)))
                raise e
        return trier
    return deco
def get_modules(package):
    """package->[module]--return all modules in a package"""
    return [find_module('%s.%s' % (package.__name__, mdname)) for mdname in package.__all__]
def find_module(mdname):
    """str->module--find a module dynamically
    NOTE:You can find modules inside packages also.
    NOTE:You can have a trailing . on the module name, but this usage is DEPRECATED"""
    return __import__(text.chomp(mdname,'.'), globals(), locals(), [mdname.split('.')[-1]])
def find_full(full_fnname):
    """find a fully named function, importing the function that it's in
    >>> find_full('os.path.split')('hello/world')
    ('hello', 'world')
    """
    return getattr(find_module(full_fnname[:full_fnname.rfind('.')]), full_fnname[full_fnname.rfind('.')+1:])
def get_funcs(module):
    """module->[fn]--return all functions in a module"""
    return [fn for fn in module.__dict__.values() if type(fn) is types.FunctionType]
def get_obj(s, env):
    """str*{str:any}->str | int | any--evaluate s if it is a string, integer or variable in the passed environment dictionary

    >>> d = {1: '2', '3': '4', 5: '"barf, k"'}
    >>> get_obj('d', locals())
    {1: '2', '3': '4', 5: '"barf, k"'}
    >>> get_obj('444', locals()) + 44
    488
    >>> get_obj("'hello'", locals())
    'hello'
    >>> get_obj('hello', locals()) #throws NameError, as expected*
    Traceback (most recent call last):
      :
    NameError: name 'hello' is not defined

    *always assuming, of course, that you expect the Right Thing. (This line stolen from Larry Wall.)
    """
    if car(s)=="'" or car(s)=='"':
        return s[1:-1]
    elif '0' <= car(s) <= '9':
        return int(s) #maybe float(s)?
    else:
        try:
            return env[s]
        except KeyError, k:
            raise NameError("name %r is not defined" % k.args)
def parse_params(s, env):
    """str*{str:any}->[any]--return actual values for the string list
    NOTE:Merely expects comma separated values with no brackets/parens:
    >>> d = {1: '2'}
    >>> parse_params("1,2,3,'foo','bar',4,d", locals())
    [1, 2, 3, 'foo', 'bar', 4, {1: '2'}]
    """
    if s:
        return [get_obj(p.strip(), env) for p in s.split(',')]
    else:
        return []
def run_fn(s, env):
    """str*{str:any}->any--run the fully namespaced function in s and return its result
    >>> import web
    >>> run_fn("web.escape('<stuff&nonsense>')", locals())
    '&lt;stuff&amp;nonsense&gt;'
    >>> s = 'dangerous->pointer;'
    >>> run_fn("web.escape(s)", locals())
    'dangerous-&gt;pointer;'
    """
    fn,args = s.split("(", 1)
    return find_full(fn)(*parse_params(args[:-1], env))
def find_full_name(module, fn):
    return "%s.%s" % (module.__name__, fn.__name__)
def find_fn_name(fn):
    "eg _newsdelete -> 'source.admin.defaults._newsdelete' "
    return "%s.%s" % (fn.__module__, fn.__name__)
def find_partial_name(fn):
    "eg _newsdelete -> 'defaults._newsdelete' "
    return "%s.%s" % (text.last_word(fn.__module__, '.'), fn.__name__)
def find_simple_name(o):
    """module | fn->str--returns the unnamespaced name"""
    return o.__name__.split('.')[-1]
def protected(o):
    """module | fn->bool--is module or function protected?"""
    return find_simple_name(o).startswith("_")
public = fnc.negate(protected) #is module or function public?
def _test():
    import doctest, reflect
    return doctest.testmod(reflect)
if __name__=="__main__":
    _test()
