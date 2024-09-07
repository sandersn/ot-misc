#!/usr/bin/python
# -*- coding: utf-8 -*-
#word on the street has it that #!/usr/bin/env python is safer for multi-platform use.
#from util.data_struct import *
#import pprint
import sys
from util import dct
"""unifeat.py -- a stupid name for something that unifies features of phonemes.
Python unicode support keeps getting stinkier. identifiers are restricted to be ASCII, and UTF-16 encoding
does *not* work. I suppose UTF-8 will be a savings here anyway, but the identifier thing *kills*
me because I was using nice 2.3 dict constructors that avoid all the quoting mess. At least
I only have to quote a fixed number of items and the features are still unquoted (although this STILL requires
2.3, so it may have to go if I want to use hostony)
Some features we want, based on the recent phonology homework:
    1)Lookup ability (based on filtering by specified features)
    2)Feature display (based on selection from a list of symbols)
    3)Multiple feature display, with display of the common features (and common subsets) contrasted with uncommon features
    4)Ability to alter features and update to the resulting symbol
TODO:Very important: need to reduce the features to:
cons: approx, cons(+) sonorant place(labial coronal dorsal) voice strident(fricatives only)
vowel: approx(+) cons(-) son(+) back high ATR low round (this is now TRUE)
"""
features = dict.fromkeys(['cons', 'son', 'strid', 'voice', 'round','contin', 'ATR', "RTR", 'high', 'low', 'back',
    'approx', 'nasal', 'spread gl', 'constr gl', 'anterior', 'lateral'], ("+","-","None"))
features['place'] = "labial", "coronal", "dorsal", "None" #TODO:Put this in someday
#BEGIN 2.2 compatible version of phoneme data
phonemes= dct.map_keys(lambda c:c.decode('utf8'),
                       {'p': {'cons': True, 'son': False, 'place': 'labial', 'voice': False, 'contin': False, 'approx':False},
           'b': {'cons': True, 'son': False, 'place': 'labial', 'voice': True, 'contin': False, 'approx':False},
           't' : {'cons': True, 'son': False, 'place': 'coronal', 'voice': False, 'contin': False, 'approx':False, 'anterior':True,},
           'd' : {'cons': True, 'son': False, 'place': 'coronal', 'voice': True, 'contin': False, 'approx':False, 'anterior':True,},
           'ʈ' : {'cons': True, 'son': False, 'place': 'coronal', 'voice': False, 'contin': False, 'approx':False, 'anterior':False, },
           'ɖ' : {'cons': True, 'son': False, 'place': 'coronal', 'voice': True, 'contin': False, 'approx':False, 'anterior':False,},
           'c' : {'cons': True, 'son': False, 'place': 'coronal', 'voice': False, 'contin': False, 'approx':False, 'anterior':False,},
           'ɟ' : {'cons': True, 'son': False, 'place': 'coronal', 'voice': True, 'contin': False, 'approx':False, 'anterior':False, },
           'k' : {'cons': True, 'son': False, 'place': 'dorsal', 'voice': False, 'contin': False, 'approx':False, 'back':True},
           'g' : {'cons': True, 'son': False, 'place': 'dorsal', 'voice': True, 'contin': False, 'approx':False, 'back':True},
           'q' : {'cons': True, 'son': False, 'place': 'dorsal', 'voice': False, 'contin': False, 'approx':False, 'back':True, },
           'ɢ' : {'cons': True, 'son': False, 'place': 'dorsal', 'voice': True, 'contin': False, 'approx':False, 'back':True, },
           'ʔ' : {'cons': True, 'son': False, 'place': 'dorsal', 'voice': True, 'contin': False, 'approx':False, 'back':True, 'constr gl':True, },
           #row 1 FINISH!
           'm': {'cons': True, 'son': True, 'place': 'labial', 'voice': True, 'nasal':True, 'contin': False, 'approx':False},
           'ɱ': {'cons': True, 'son': True, 'place': 'labial', 'voice': True, 'nasal':True,  'contin': False, 'approx':False,},
           'n': {'cons': True, 'son': True, 'place': 'coronal', 'voice': True, 'nasal':True,  'contin': False, 'approx':False, 'anterior':True},
           'ɳ': {'cons': True, 'son': True, 'place': 'coronal', 'voice': True, 'nasal':True,  'contin': False, 'approx':False, 'anterior':False,},
           'ɲ': {'cons': True, 'son': True, 'place': 'coronal', 'voice': True, 'nasal':True,  'contin': False, 'approx':False, 'anterior':False,},
           'ŋ': {'cons': True, 'son': True, 'place': 'dorsal', 'voice': True, 'nasal':True,  'contin': False, 'approx':False},
           'ɴ': {'cons': True, 'son': True, 'place': 'dorsal', 'voice': True, 'nasal':True,  'contin': False, 'approx':False, },
           #row 2 FINISH!
           'ʙ': {'cons': True, 'son': True, 'place': 'labial', 'voice': True, 'contin': True, 'approx':True, 'lateral':False, },
           'r': {'cons': True, 'son': True, 'place': 'coronal', 'voice': True, 'contin': True, 'approx':True, 'lateral':False},
           'ʀ': {'cons': True, 'son': True, 'place': 'dorsal', 'voice': True, 'contin': True, 'approx':True, 'lateral':False, },
           #row 3 FINISH!
           'ɾ' : {'cons': True, 'son': True, 'place': 'coronal', 'voice': True, 'contin': False, 'approx':True, 'lateral':False, 'anterior':True},
           'ɽ' : {'cons': True, 'son': True, 'place': 'coronal', 'voice': True, 'contin': False, 'approx':True, 'lateral':False, 'anterior':False},
           #row 4 FINISH!
           'ɸ': {'cons': True, 'son': False, 'place':'labial','voice': False, 'approx': False, 'contin': True, 'strid': False},
           'β': {'cons': True, 'son': False, 'place':'labial','voice': True, 'approx': False, 'contin': True, 'strid': False},
           'f': {'cons': True, 'son': False, 'place':'labial','voice': False, 'approx': False, 'contin': True, 'strid': True},
           'v': {'cons': True, 'son': False, 'place':'labial','voice': True, 'approx': False, 'contin': True, 'strid': True},
           'θ': {'cons': True, 'son': False, 'place':'coronal','voice': False, 'approx': False, 'contin': True, 'strid': False, 'anterior':True},
           'ð': {'cons': True, 'son': False, 'place':'coronal','voice': True, 'approx': False, 'contin': True, 'strid': False, 'anterior':True},
           's': {'cons': True, 'son': False, 'place':'coronal','voice': False, 'approx': False, 'contin': True, 'strid': True, 'anterior':True},
           'z': {'cons': True, 'son': False, 'place':'coronal','voice': True, 'approx': False, 'contin': True, 'strid': True, 'anterior':True},
           'ʃ': {'cons': True, 'son': False, 'place':'coronal','voice': False, 'approx': False, 'contin': True, 'strid': True, 'anterior':False},
           'ʒ': {'cons': True, 'son': False, 'place':'coronal','voice': True, 'approx': False, 'contin': True, 'strid': True, 'anterior':False},
           'ʂ': {'cons': True, 'son': False, 'place':'coronal','voice': False, 'approx': False, 'contin': True, 'strid': True, 'anterior':False, },
           'ʐ': {'cons': True, 'son': False, 'place':'coronal','voice': True, 'approx': False, 'contin': True, 'strid': True, 'anterior':False, },
           'ç': {'cons': True, 'son': False, 'place':'coronal','voice': False, 'approx': False, 'contin': True, 'strid': True, 'anterior':False, },
           'ʝ': {'cons': True, 'son': False, 'place':'coronal','voice': True, 'approx': False, 'contin': True, 'strid': True, 'anterior':False, },
           'x': {'cons': True, 'son': False, 'place':'dorsal','voice': False, 'approx': False, 'contin': True, 'strid': False},
           'ɣ': {'cons': True, 'son': False, 'place':'dorsal','voice': True, 'approx': False, 'contin': True, 'strid': False},
           'χ': {'cons': True, 'son': False, 'place':'dorsal','voice': False, 'approx': False, 'contin': True, 'strid': True, },
           'ʁ': {'cons': True, 'son': False, 'place':'dorsal','voice': True, 'approx': False, 'contin': True, 'strid': True, },
           'ħ': {'cons': True, 'son': False, 'place':'dorsal','voice': False, 'approx': False, 'contin': True, 'strid': False, "RTR":True, },
           'ʕ': {'cons': True, 'son': False, 'place':'dorsal','voice': True, 'approx': False, 'contin': True, 'strid': False, "RTR":True, },
           'h': {'cons': True, 'son': False, 'place':'dorsal','voice': False, 'approx': False, 'contin': True, 'strid': True, },
           'ɦ': {'cons': True, 'son': False, 'place':'dorsal','voice': True, 'approx': False, 'contin': True, 'strid': True, },
           #row 5 FINISH!
           'ɬ' : {'cons': True, 'son': False, 'place': 'coronal', 'voice': False, 'contin': True, 'approx':True, 'anterior':True, 'lateral':True},
           'ɮ' : {'cons': True, 'son': False, 'place': 'coronal', 'voice': True, 'contin': True, 'approx':True, 'anterior':True, 'lateral':True, },
           #row 6 FINISH!
           'ʋ' : {'cons': True, 'son': True, 'place': 'labial', 'voice': True, 'contin': True, 'approx':True, 'lateral':False},
           'ɹ' : {'cons': True, 'son': True, 'place': 'coronal', 'voice': True, 'contin': True, 'approx':True, 'anterior':True, 'lateral':False},
           'ɻ' : {'cons': True, 'son': True, 'place': 'coronal', 'voice': True, 'contin': True, 'approx':True, 'anterior':False, 'lateral':False},
           'j' : {'cons': True, 'son': True, 'place': 'coronal', 'voice': True, 'contin': True, 'approx':True, 'anterior':False, 'lateral':False,},
           'ɰ' : {'cons': True, 'son': True, 'place': 'dorsal', 'voice': True, 'contin': True, 'approx':True, 'lateral':False},
           #row 7 FINISH!
           'l' : {'cons': True, 'son': True, 'place': 'coronal', 'voice': True, 'contin': True, 'approx':True, 'anterior':True, 'lateral':True},
           'ɭ' : {'cons': True, 'son': True, 'place': 'coronal', 'voice': True, 'contin': True, 'approx':True, 'anterior':False, 'lateral':True,},
           'ʎ' : {'cons': True, 'son': True, 'place': 'coronal', 'voice': True, 'contin': True, 'approx':True, 'anterior':False, 'lateral':True},
           'ʟ' : {'cons': True, 'son': True, 'place': 'dorsal', 'voice': True, 'contin': True, 'approx':True, 'lateral':True},
           #row 8 FINISH!
           #vowel-part BEGIN!
           'a': {'cons':False,'son':True,'high': False, 'low': True, 'back': False, 'ATR': False, 'round': False, 'approx':True, 'contin':True},
           'ʌ': {'cons':False,'son':True,'high': False, 'low': False, 'back': True, 'ATR': True, 'round': False, 'approx':True, 'contin':True},
           'ɔ': {'cons':False,'son':True,'high': False, 'low': False, 'back': True, 'ATR': False, 'round': True, 'approx':True, 'contin':True},
           'o': {'cons':False,'son':True,'high': False, 'low': False, 'back': True, 'ATR': True, 'round': True, 'approx':True, 'contin':True},
           'ɯ': {'cons':False,'son':True,'high': True, 'low': False, 'back': True, 'ATR': True, 'round': False, 'approx':True, 'contin':True},
           'u': {'cons':False,'son':True,'high': True, 'low': False, 'back': True, 'ATR': True, 'round': True, 'approx':True, 'contin':True},
           'ʊ': {'cons':False,'son':True,'high': True, 'low': False, 'back': True, 'ATR': False, 'round': True, 'approx':True, 'contin':True},
           'ɨ': {'cons':False,'son':True,'high': True, 'low': False, 'back': True, 'ATR': False, 'round': False, 'approx':True, 'contin':True},
           'ə': {'cons':False,'son':True,'high': False, 'low': False, 'back': True, 'ATR': False, 'round': False, 'approx':True, 'contin':True},
           'i': {'cons':False,'son':True,'high': True, 'low': False, 'back': False, 'ATR': True, 'round': False, 'approx':True, 'contin':True},
           'y': {'cons':False,'son':True,'high': True, 'low': False, 'back': False, 'ATR': True, 'round': True, 'approx':True, 'contin':True},
           'ɪ': {'cons':False,'son':True,'high': True, 'low': False, 'back': False, 'ATR': False, 'round': False, 'approx':True, 'contin':True},
           'e': {'cons':False,'son':True,'high': False, 'low': False, 'back': False, 'ATR': True, 'round': False, 'approx':True, 'contin':True},
           'ø': {'cons':False,'son':True,'high': False, 'low': False, 'back': False, 'ATR': True, 'round': True, 'approx':True, 'contin':True},
           'ɛ': {'cons':False,'son':True,'high': False, 'low': False, 'back': False, 'ATR': False, 'round': False, 'approx':True, 'contin':True},
           'œ': {'cons':False,'son':True,'high': False, 'low': False, 'back': False, 'ATR': False, 'round': True, 'approx':True, 'contin':True},
           'æ': {'cons':False,'son':True,'high': False, 'low': True, 'back': False, 'ATR': False, 'round': False, 'approx':True, 'contin':True},
           # extended things (prompted by S** transcriptions)
           # need a 3rd attr 'mid' in addition to 'high' and 'low' for ɜ
           'ɜ': {'cons':False,'son':True,'high': False, 'low': False, 'back': True, 'ATR': False, 'round': False, 'approx':True, 'contin':True},
           'ɒ': {'cons':False,'son':True,'high': False, 'low': True, 'back': True, 'ATR': False, 'round': True, 'approx':True, 'contin':True},
           'ɑ': {'cons':False,'son':True,'high': False, 'low': True, 'back': True, 'ATR': False, 'round': False, 'approx':True, 'contin':True},
           'ʉ': {'cons':False,'son':True,'high': True, 'low': False, 'back': True, 'ATR': False, 'round': True, 'approx':True, 'contin':True},
           'ʏ': {'cons':False,'son':True,'high': True, 'low': False, 'back': False, 'ATR': False, 'round': True, 'approx':True, 'contin':True},
           'w' : {'cons': True, 'son': True, 'place': 'labial', 'voice': True, 'contin': True, 'approx':True, 'anterior':True, 'lateral':False},
           'ʰ': {'cons': True, 'son': False, 'place':'dorsal','voice': False, 'approx': False, 'contin': True, 'strid': True, },
           'ɫ' : {'cons': True, 'son': True, 'place': 'dorsal', 'voice': True, 'contin': True, 'approx':True, 'anterior':False, 'lateral':True},
           "#":{'boundary':True}}) #last (but not least), a concession to reality
def unify(s):
    return map(phonemes.get, s)
def main():
#    if sys.argv[1:]:
    requested = sys.argv[1:]
#    else:
#        import cgi
#        requested = cgi.FieldStorage().getlist("req")
    web_display_features(requested)
def common(ps):
    """[{str:Feature}]->{str:Feature}--find all common attributes that also unify
        (this will eventually need n**2 refinement instead of order n version here 
        (must test all inter-phonemic features instead of just the ones common to _all_ in the list)
        """
    return dict([(f,v) for (f,v) in car(ps).items() if in_all(f, ps) and same_bool([phone[f] for phone in ps])])
def search(fs):
    "{str:Feature}->{str:{str:Feature}}--search for compatible sounds"
    return filter_dict_values(lambda ph: subsumes(ph,fs), phonemes)
def subsumes(d,e):
    "this is the wrong name. leave me alone! (TODO:Think about using Set > or >= instead"
    if e:
        try:
            return all(lambda k:d[k]==e[k], e)
        except KeyError:
            return False
    else:
        return True
def common_fields(p,*ps):
    """[{str:Feature}]->[str]--find all the common field *names*"""
    fields = p.keys()
    for p in ps:
        fields = merge(fields, p.keys())
    return fields
def uncommon(ps, excluded=()):
    "[{Feature}]->[{Feature}]--"
    return map_dict(lambda features:except_dict(features, *excluded.keys()), ps)
def web_display_features(requested):
    selected = extract_dict(phonemes, *requested)
    commons = common(selected.values())    
    print 'Content-type:text/html\n\n'
    print """
    <html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    </head>
    <body>
    Common features:<table border=1><tr>%s</tr></table>
    <table border=1><tr>%s</tr></table>
    </body>
    </html>""" % (gen_feature_row(commons, commons.keys()), 
        show_desired_phonemes(uncommon(selected, commons), phonemes.keys()))
    pprint.pprint(uncommon(selected, commons))
def show_desired_phonemes(ph, desired):
    "{}*[str]->str"
    bgs = alternator("#CCCCCCC", "#DDDDDD")
    #1.find all common fields
    fields = common_fields(*ph.values())
    fields.sort()
    #3.display ALL fields for ALL features, using feature.get(f, "")
    return '</tr>\n<tr>'.join(["<td style='background-color:%s'><h2>%s</h2></td>%s" % \
        (bgs.next(), sym, gen_feature_row(features, fields)) for sym,features in extract_dict(ph, *desired).items()])
def gen_feature_row(features, fields):
    return '\n'.join(["<td>%s</td>" % gen_feature(f, features.get(f,"None")) for f in fields])
    #return '\n'.join(["<td>%s%s</td>" % (x,f) for f,b in features.items()])
def gen_feature(f,state):
    if isinstance(state, int): #2.2 bool):
        return (state and "+" or '-') + f
    elif state=="None":
        return "<span style='color:grey'>%s</span>" % state
    else:
        return state
if __name__=="__main__":
    main()
