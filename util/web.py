"""web.py -- web utility functions

TODO:Do all these regexen need to be compiled first?"""
import re
import text
import data_struct
import cgi

def wrap(item,wrapping):
    """str*str->str--string mod, plus make item safe for sample view"""
    return wrapping % safeforms(item)

def findmods(s):
    """
    str->[]-- Returns a list of all the string mod instances in `s`

    uses a regular expression string which
    matches all text in the form  '%(' +anything+ ')s'
    >>> findmods("%(something)s text text text text %(else)s")
    ['%(something)s', '%(else)s']
    """
    p = re.compile(r'(%\({1,1}\w*\)s{1,1})')
    return p.findall(s)
def findmod_names(s):
    """
    str->[]-- Returns a list of all the string mod instances in `s`

    uses a regular expression string which
    matches all text in the form  '%(' +anything+ ')s'
    >>> findmod_names("%(something)s text text text text %(else)s")
    ['something', 'else']
    """
    p = re.compile(r'%\({1,1}(\w*)\)s{1,1}')
    return p.findall(s)
def fill_missingmods(template, contentdict):
    "str*{str:str}->{str:str}--Return new content dict with error message filled in for unmatched mods in template"
    c = dict(contentdict)
    for item in findmod_names(template):
        if item not in contentdict:
            c[item] = 'Error Code: 002; No Match For '+item
    return c
def safeforms(source):
    """str->str -- strip out all html references to forms, links, and javascript
    As an aside, the regex style used here is abominable. Commenting would have helped in changing it.
    """
    forms = re.compile(r'(<{1}/?form{1}.*?>{1})', re.IGNORECASE)
    source = forms.sub('<!-- form element commented out for preview -->', source)
    links = re.compile(r'(<a{1}\b.*?href={1})(.{1}).*?\2(.*?>)', re.IGNORECASE)
    source = links.sub('\g<1>\g<2>#\g<2>\g<3>', source)
    scripts = re.compile(r'(<{1}/?script{1}.*?>{1})', re.IGNORECASE)
    source = scripts.sub('<!-- scripting commented out for preview -->', source)
    #filter out <tag on*="javascript">
    #(the (?:...) construction means parens that don't return a group for later use)
    #all the ? spread around are generally to allow for spaces and different quotes
    #except for *?, which is non-greedy *
    #\W and \w are an attempt to get only on* type words
    source = re.sub(r'(?i)\Won\w*? ?= ?(?:"|\').*?(?:"|\')', '', source)
    return source
def safescript(source):
    """str->str--break up any </script> tags that are meant to be embedded.
    NOTE:This is not meant to be terribly robust"""
    return source.replace("</script>","</scri'+'ipt>")
def escape(s):
    """str->str--escape < > & ' and " """
    return cgi.escape(text.squash_newlines(s), 1)
def realdict(fd):
    """FieldStorage->{}--Get a real dict from a cgi FieldStorage dict-like-object
    NOTE:Does not allow for multiple entries with the same name (eg checkboxen)"""
    d={}
    for k in fd.keys():
        if fd[k].filename:
            d[k] = fd[k]
        else:
            d[k] = fd[k].value
    return d
def row_ender(length, end):
    """int*str->iter:str--generate end row text

    Example:
    >>> rows = row_ender(3, '</tr><tr>')
    >>> rows.next(), rows.next(), rows.next(), rows.next()
    ('', '', '</tr><tr>', '')
    """
    return data_struct.alternator(*(length-1)*[''] + [end])
def _test():
    import doctest, web
    return doctest.testmod(web)
if __name__=="__main__":
    _test()
