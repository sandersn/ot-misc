#!/usr/bin/env python
import csv
import os
import optparse
import pprint
from util.fnc import car, compose, cur, flip
from util.lst import bifilter, mapn, unzip
from util.reflect import traced
from operator import sub
import sexp
from rcd import rcd, nonrcd
from bcd import bcd
from lfcd import lfcd
from gla import gla
#import types # in case you were wondering where funcall is in Python...
#funcall = types.FunctionType.__call__
## utils
def drop(n, l):
    "Pointless in Python unless you need a name for slice-to-end"
    return l[n:]
def group_by(f, l):
    "I have written this four or five times this year. SAVE as split_by in lst"
    acc = []
    group = []
    for x in l:
        if f(x):
            acc.append(group)
            group = [x]
        else:
            group.append(x)
    acc.append(group)
    return acc
def splitat(n, l):
    return l[:n],l[n:]
## con (these are all extremely fake and should come from faith/mark instead)
def idasp(i,o): # anyway they are only good for Hayes' pseudo-Korean example
    return "Id (asp)"
def idvoice(i, o):
    return "Id (voice)"
def idasp_v(i, o):
    return "Id (asp)/_V"
def idvoice_v(i, o):
    return "Id (voice)/_V"
def no_pvmvpv(o):
    return "*[+v][-v][+v]"
def nodh(o):
    return "*dh"
def novoiceobs(o):
    return "*[-son/+voice]"
def noasp(o):
    return "*aspiration"
con = {"Id (asp)": idasp,
       "Id (voice)": idvoice,
       "Id (asp)/_V": idasp_v,
       "Id (voice)/_V": idvoice_v,
       "*[+v][-v][+v]": no_pvmvpv,
       "*dh" : nodh,
       "*[-son/+voice]": novoiceobs,
       "*asp": noasp}
## code
specificity = {}
def vln2int(vln):
    "Convert '1' to 1, as well as '' to 0"
    try:
        return int(vln)
    except ValueError:
        return 0
def abs2relative(tableau):
    [win], rivals = bifilter(car, map(compose(cur(map,vln2int), cur(drop,2)),
                                      tableau))
    win, rivals = drop(1, win), map(cur(drop,1), rivals)
    return map(cur(map, flip(sub), win), rivals)
def marklike(title):
    return title[0]=="*"
def specificlike(title1, title2):
    return title1.startswith(title2) and title1 != title2
def title2col(titles):
    "side effect: fill up specificity"
    cols = map(con.get, titles)
    for i,title in enumerate(titles):
        try:
            specificity[cols[i]] = cols[map(cur(specificlike,title), titles).index(True)]
        except ValueError:
            pass
    return cols
def read_sexp(fname, method):
    return zip([idasp, idvoice, idasp_v, idvoice_v,
                no_pvmvpv, nodh, novoiceobs, noasp],
               sexp.read(file(fname).read())[0])
def read_csv(fname, method):
    titles, tableaux = splitat(1, group_by(car, csv.reader(file(fname))))
    if method=='gla':
        def glarow(line): #throw away any candidate
            return (bool(line[1]), map(lambda s: s and int(s) or 0, line[2:]))
        return titles[0][0][1:], map(cur(map,glarow), tableaux)
    else:
        return zip(title2col(drop(3, titles[0][1])),
                   unzip(mapn(abs2relative, tableaux)))
def write_sexp(con, outf):
    pass
def write_text(con, outf):
    pprint.pprint(con, outf)
def write_html(con, outf):
    pass
def write_tex(con, outf):
    pass
def write_rtf(con, outf):
    pass
def run():
    # read_sexp('ot_learning/pseudo-korean.sexp'), 
    return read_csv('ot_learning/Korean.csv')
def test():
    assert lfcd(read_sexp('ot_learning/pseudo-korean.sexp', 'lfcd'),
                    {idasp_v:idasp, idvoice_v:idvoice}) == \
                    [[nodh], [idasp_v], [no_pvmvpv, noasp], [novoiceobs],
                     [idasp, idvoice, idvoice_v]]
    assert bcd(read_sexp('ot_learning/pseudo-korean.sexp', 'bcd')) == \
                   [[nodh], [idasp], [no_pvmvpv, noasp], [novoiceobs],
                    [idvoice, idasp_v, idvoice_v]]
    assert rcd(read_sexp('ot_learning/pseudo-korean.sexp', 'rcd')) == \
                   [[idasp, idvoice, idasp_v, idvoice_v, nodh],
                    [no_pvmvpv, novoiceobs, noasp]]
    assert nonrcd(read_sexp('ot_learning/pseudo-korean.sexp', 'nonrcd')) == \
                   [[idasp, idvoice, idasp_v, idvoice_v, nodh],
                    [no_pvmvpv, novoiceobs, noasp]]
if __name__=="__main__":
    #hydrogen foo.csv #guess from extension.
    #hydrogen foo.sexp
    #hydrogen -i csv foo.data
    #hydrogen -i xml foo.xml
    #hydrogen --input=sexp foo.data
    #--input=sexp parse input file as s-expression
    #--input=xml parse input file as xml
    #--input=csv parse input file as csv
    #--input=excel (Windows only;Excel must be installed)
    #hydrogen --method=rcd foo.sexp
    #hydrogen --method=lfcd foo.cvs
    #hydrogen -m bcd foo.xml
    #hydrogen foo.xml bar.txt
    #OR hydrogen foo.xml >bar.txt
    #hydrogen - <foo.csv >bar.txt (<foo.xls probably won't work...just FYI )
    #hydrogen -o txt foo.xml >bar.txt
    #hydrogen -o doc foo.xml suck.doc
    #hydrogen -o rtf foo.xml suck.rtf (these are really the same thing)
    #hydrogen --output=tex foo.xml good.tex
    #hydrogen --output=html foo.xml
    #hydrogen -r apriorirankings.csv foo.xml
    #hydrogen -xflipgrid -xexplainall -x... foo.xml
    # just use -x for all the smaller options provided by OTSoft

    # hydrogen OPTIONS INFILE OUTFILE
    # hydrogen OPTIONS INFILE (output to STDOUT)
    # hydrogen OPTIONS - (input from STDIN, output to STDOUT)
    # -i --input= csv sexp xml xls
    # -o --output= txt rtf doc tex html
    # -r --ranking=FILE (for apriori rankings)
    # -m --method rcd bcd lfcd lfcd+s genericOT
    # -x --option flipgrid explainall maxsize ... there are quite a few...
    from optparse import OptionParser, make_option
    import sys
    p = OptionParser(
        usage='usage: %prog [options] INFILE [OUTFILE]',
        version='%prog 0.2', # remember to mention INFILE can be -
        description='''Implement a number of OT learning algorithms in
much the same way that OTSoft did. If input and output types are not given,
they will be guessed from the file extension.''',
#        prog='Hydrogen',
        option_list= [make_option('-i', '--input',
                          choices='csv sexp xml xls'.split(),
                          help='specify input format of csv sexp xml xls'),
                         make_option('-o', '--output',
                          choices='txt html tex doc rtf'.split(),
                         help='specify output format of txt html tex doc rtf'),
                         make_option('-m', '--method',
                          help='use learning methods of rcd bcd lfcd'),
                         make_option('-r', '--ranking', metavar='FILE',
                          help='read a priori rankings from FILE'),
                         make_option('-x', '--option', action='append',
                          choices='flipgrid explainall something else'.split(),
                          help='add options specified somewhere')])
    ms = {'bcd':bcd, 'rcd':rcd, 'lfcd':lambda data:lfcd(data,specificity),
          'gla':lambda data:gla(map(lambda c:(c,100), data[0]),
                                data[1],
                                [(7000,2,10), (7000,0.2,2), (7000,0.2,0.2)])}
    o, args = p.parse_args()
    readers = {'csv':read_csv, 'sexp':read_sexp} #xml and xls LATER, OK?
    writers = {'txt':write_text, 'html':write_html}
    method = ms.get(o.method, rcd)
    readfile = readers.get(o.input or os.path.splitext(args[0])[1][1:],
                           read_csv)
    output = writers.get(o.output, write_text)
    if len(args) > 1:
        outfile = open(args[1],'w')
    else:
        outfile = sys.stdout
    output(method(readfile(args[0], o.method)), outfile)
