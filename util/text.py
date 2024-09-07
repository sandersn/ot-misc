"""text.py -- text manipulation functions

The dictionary bracematch provides a handy dict in case you want to make decisions which require
matching one brace type to another. I may add more exotic matches later.
"""
bracematch={'[':']', "{":"}", "(":")", "<":">"}
import re
from fnc import compose
def squash_newlines(s):
    """str->str :: deletes line breaks"""
    return s.replace('\n', " ").replace('\r', " ")
def remove_newlines(s):
    """str->str :: deletes line breaks"""
    return s.replace('\n', "").replace('\r', "")
def escape_singlequotes(s):
    return s.replace("'", "\\'")
def escape_doublequotes(s):
    return s.replace('"', '\\"')
escape_quotes = compose(escape_singlequotes, escape_doublequotes) #escape all quotes
def escape_slash(s):
    return s.replace('\\', '\\\\')
def i18nrepr(s):
    return '"%s"' % escape_doublequotes(escape_slash(str(s)))
rteditsafe = compose(i18nrepr, squash_newlines)
def escape_mod(s):
    """str->str--escape any %, (except for ones before a dict mod: %(key)s)
    >>> escape_mod("This 100% cool: %(coolthing)s. Wasn't it?")
    "This 100%% cool: %(coolthing)s. Wasn't it?"
    """
    return s.replace("%", "%%").replace("%%(", "%(")
def unescape_mod(s):
    """str->str--unescape any %% to just %"""
    return s.replace("%%", "%")
def between(s, start, end):
    """str*str*str->str--Extract the string between start and end.
    NOTE:Returns nothing if either start or end is not found. This may change.
    >>> x = '<html><head><style> body {color:black;}; .other {color:grey;}; </style> <body> <p>stuff</p> </body></html>'
    >>> between(x, '<style>', '</style>')
    ' body {color:black;}; .other {color:grey;}; '
    >>> between(x, '{', '}') #only grabs the first occurence
    'color:black;'
    >>> between(x, '<foo>', '</style>') #Won't find anything
    ''
    
    '"""
    try:
        start_pos=s.index(start)+len(start)
        return s[start_pos:s.index(end, start_pos)]
    except ValueError:
        return ''
def not_between(s, start, end):
    try:
        start_pos=s.index(start)+len(start)
        return s[:s.index(start)] + s[s.index(end, start_pos)+len(end):]
    except ValueError:
        return ''
def before(s, end):
    "str*str->str"
    try:
        return s[:s.index(end)]
    except ValueError:
        return ''
def after(s, start):
    "str*str->str"
    try:
        return s[s.index(start)+len(start):]
    except ValueError:
        return ''
def format_list(format, l, sep='\n', default=''):
    """str*[]*str->str--String mod format on each item in l; gives default if l is empty
    >>> format_list("%5d", [1,2,3,4], '|')
    '    1|    2|    3|    4'
    >>> format_list("<div>%s</div>", [1,'hi', 14], '&nbsp;')
    '<div>1</div>&nbsp;<div>hi</div>&nbsp;<div>14</div>'
    >>> format_list('much ado about nothing', [], default='twelfth night')
    'twelfth night'
    
    Haskell version of text.format_list is just
    format_list s =map ((%) s)
    (See comment below for an exactly equivalent Python version using map)
    (I'm not sure which I like better, but I suspect the current version is faster)
    """
    if l:
        return sep.join([format % x for x in l]) # = return sep.join(map(format.__mod__, l))
    else:
        return default
def split_save(word, splits):
    """str*(str|[str])->[str] --Splits a given word on the string array of splits, saving the split 

    Pass a string for the second argument to use one-character splits. Pass a list of strings
    to split on any length of string.

    The primary reason this function is useful is that it does not consume the text of the things it splits on,
    and that it is easy to split on multiple things:
    >>> split_save('hello', 'hi') #a str param for splits will act as a list of chars
    ['h', 'ello']
    >>> split_save('hello', ['h', 'i'])
    ['h', 'ello']
    >>> split_save('hhhhhello', 'hi')
    ['h', 'h', 'h', 'h', 'h', 'ello']
    >>>     #now for a real-world example:
    >>> split_save("([nested (stuff) goes] here)", "()[]")
    ['(', '[', 'nested ', '(', 'stuff', ')', ' goes', ']', ' here', ')']
    >>>     #or for longer strings to split on (notice how j' and t' are chosen greedily over ' ):
    >>> split_save("'j'aime t'ecrire.'", ["'","j'", "t'", '.'])
    ["'", "j'", 'aime ', "t'", 'ecrire', '.', "'"]

    NOTE:This function uses re. Hope this doesn't bother anyone! I had some old inefficient code
    that was non-re dependent, but it is gone."""

    #need the filter None because re.split spews empty strings a lot due to regex splitting rules
    return filter(None, re.split("("+"|".join(map(re.escape, splits))+")", word))
def last_word(s, sep=None):
    """Get the last word. Uses str.split, so there might be a more efficient version.

    >>> last_word('source.admin.defaults._newsform', '.')
    '_newsform'
    >>> last_word("He who laughs last laughs best.")
    'best.'
    """
    return s.split(sep)[-1]
def chomp(s,c='\n'):
    """str*str|1|->str--remove last character if it matches c
    >>> chomp("hello:", ':')
    'hello'
    >>> chomp("hello", ':')
    'hello'
    
    '"""
    if s and s[-1] == c:
        return s[:-1]
    else:
        return s
##strip_mod = compose(chomp, chomp, reverse, chomp, chomp, reverse) #it's pacman!
def strip_mod(s):
    return s[2:-2]
def strtuple(t):
    """any->str--converts a tuple to a string, except that singletons don't get the trailing ,
    >>> strtuple((1,2,3))
    '(1, 2, 3)'
    >>> strtuple((1,))
    '(1)'
    
    '"""
    return str(tuple(t)).replace(",)", ")")
def _test():
    import doctest, text
    return doctest.testmod(text)
if __name__=="__main__":
    _test()
