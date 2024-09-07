import unittest
import hydrogen
import unifeat
import ot
import faith, mark
import lev
from util.fnc import compose, iseq
from util.lst import fst, snd
from util.reflect import traced
import test as OTableauTest
from hydrogen import (idasp, idvoice, idasp_v, idvoice_v, no_pvmvpv, nodh,
                      novoiceobs, noasp)
import ot # a lot of ot is already done in OTableau except for the
# formal evaluation of constraint violations.
test = None # this is a dirty hack, but I HATE typing self.assertEqual
qw = str.split
class TestHydrogen(unittest.TestCase):
    def setUp(self):
        global test
        test = self.assertEqual
    def testUtils(self):
        test(hydrogen.drop(2, range(6)), [2,3,4,5])
        test(hydrogen.drop(0, range(3)), [0,1,2])
        test(hydrogen.drop(4, range(2)), [])
        test(hydrogen.drop(4, []), [])
        def oddp(n): return n % 2
        test(hydrogen.group_by(oddp, range(5)),
             [[0,],[1,2,],[3,4]])
        test(hydrogen.group_by(oddp, []),
             [[]])
        test(hydrogen.splitat(1, range(3)), ([0,], [1,2,]))
        test(hydrogen.splitat(1, []), ([],[]))
        test(hydrogen.splitat(10, range(3)), ([0,1,2],[]))
        # negative numbers work too since this is just a slice
        test(hydrogen.splitat(-2, range(3)), ([0],[1,2]))
    def testMisc(self):
        test(True, hydrogen.marklike("*Asp"))
        test(False, hydrogen.marklike("Max-IO"))
        #test(True, hydrogen.marklike('')) # crashes
        test(False, hydrogen.specificlike('',''))
        test(True, hydrogen.specificlike('Foo', ''))
    def testLev(self):
        # minimum value to trigger bug was 1.5
        test(lev.flevenshtein(unifeat.unify('ap'),unifeat.unify('pbcdpe'),2.0),
             [[0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
              [2.0, 4.0, 6.0, 8.0,10.0, 12.0, 12.0],
              [4.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0]])
        test(lev.optimal([[0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
                          [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 12.0],
                          [4.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0]]),
             [('delete', (0, 0)),
              ('substitute', (1, 0)),
              ('insert', (2, 1)),
              ('insert', (2, 2)),
              ('insert', (2, 3)),
              ('insert', (2, 4)),
              ('insert', (2, 5))])
        # TODO: Fails! Need to write lev.Change.__eq__
        # except this will probably break align.py again
##         test(lev.enviro("ap", "pbcdpe", 2.0),
##              [lev.Del (0, 'a', ("#", 'p')),
##               lev.Sub (1, ('p','p'), ("#", 'a')),
##               lev.Ins (2, 'b', ('p', "#")),
##               lev.Ins (2, 'c', ('p', "#")),
##               lev.Ins (2, 'd', ('p', "#")),
##               lev.Ins (2, 'p', ('p', "#")),
##               lev.Ins (2, 'e', ('p', "#"))])
        test(lev.flevenshtein(
            
            unifeat.unify(['\xc9\x99', 't']),
            unifeat.unify(['t', '\xca\x83', '\xca\x8a', '\xc9\xaa', 't', '\xca\xb0']),
            3.286924),
             [[0.0,      3.286924, 6.573848, 9.860772, 13.147696, 16.43462, 19.721544],
              [3.286924, 6.573848, 9.860772, 8.573848, 11.860772, 15.147696, 18.43462],
              [6.573848, 3.286924, 6.573848, 9.860772, 13.147696, 11.860772, 15.147696]])
        test(lev.optimal([[0.0, 3.286924, 6.5738479999999999, 9.8607720000000008, 13.147696, 16.434619999999999, 19.721544000000002], [3.286924, 6.5738479999999999, 9.8607720000000008, 8.5738479999999999, 11.860772000000001, 15.147696, 18.434619999999999], [6.5738479999999999, 3.286924, 6.5738479999999999, 9.8607720000000008, 13.147696, 11.860772000000001, 15.147696]]),
             [('insert', (0, 0)),
              ('insert', (0, 1)),
              ('substitute', (0, 2)),
              ('insert', (1, 3)),
              ('substitute', (1, 4)),
              ('insert', (2, 5))])
    def testAbs2Relative(self):
        # abs is without titles right now
        abs = [['foo','foo', '',   '1','','2'],
               ['', 'oof','1',  '', '', '1'],
               ['', 'oaf', '',  '2', '', '']]
        # This is the "backward language" so foo -> oof
        rel = [[1,0,1],
               [2,0,-1]]
        test(rel, hydrogen.abs2relative(abs))
    def testReadSexp(self):
        test(zip([hydrogen.idasp, hydrogen.idvoice, hydrogen.idasp_v,
                   hydrogen.idvoice_v, hydrogen.no_pvmvpv, hydrogen.nodh,
                   hydrogen.novoiceobs, hydrogen.noasp],
                  [[0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 0, 1, 1, 0, 0, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 0, 1, 1, 0, 0, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 0, 1, 1, 0, 0, 1, 1],
                   [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 2, 1, 2, 1, 1, 0, 1, 0, 2, 1, 2, 1, 0, 1, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 1, 0, 1, 0, 2, 1, 2, 1, 1, 1, 0, 2, 1, 2, 1, 0, 1, 0, 1, 1, 2, 1, 2, 0, 1, 1, 1, 2, 1, 2, 1, 0, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 1, 0, 1, 1, 2, 1, 2],
                   [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 0, 1, 1, 0, 0, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 0, 1, 1, 0, 0, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                   [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 2, 1, 2, 1, 1, 0, 1, 0, 2, 1, 2, 1, 0, 1, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 1, 0, 1, 0, 2, 1, 2, 1, 1, 1, 0, 2, 1, 2, 1, 0, 1, 0, 1, 1, 2, 1, 2, 0, 1, 1, 1, 2, 1, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, -1, -1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, -1, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, -1, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 2],
                   [1, 0, 1, 0, 1, 1, -1, -1, 0, 0, 1, 1, 1, 0, 1, -1, -1, 0, 0, 1, 0, 1, -1, 0, -1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, -1, 0, -1, 0, 0, 1, 0, 1, -1, -1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 2, 1, 2, 0, 1, 1, 1, 2, 1, 2, 1, 0, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 1, 0, 1, 1, 2, 1, 2],
                   [0, 1, 1, -1, -1, 0, 0, 1, 1, -1, -1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, -1, -1, 0, -1, -1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, -1, -1, 0, 0, -1, -1, 0, 0, 0, 1, 1, 0, 0, 1, 1, -2, -2, -1, -1, -2, -2, -1, -1, -1, -1, 0, -1, -1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, -1, -1, 0, 0, -1, -1, 0, 0, 0, 1, 1, 0, 0, 1, 1]]),
             hydrogen.read_sexp('ot_learning/pseudo-korean.sexp','lfcd'))
    def testAllMethods(self):
        test(hydrogen.lfcd(hydrogen.read_sexp('ot_learning/pseudo-korean.sexp',
                                              'lfcd'),
                  {idasp_v:idasp, idvoice_v:idvoice}),
             [[nodh], [idasp_v], [no_pvmvpv, noasp], [novoiceobs],
              [idasp, idvoice, idvoice_v]])
        test(hydrogen.bcd(hydrogen.read_sexp('ot_learning/pseudo-korean.sexp',
                                             'bcd')),
             [[nodh], [idasp], [no_pvmvpv, noasp], [novoiceobs],
              [idvoice, idasp_v, idvoice_v]])
        test(hydrogen.rcd(hydrogen.read_sexp('ot_learning/pseudo-korean.sexp',
                                              'rcd')),
             [[idasp, idvoice, idasp_v, idvoice_v, nodh],
              [no_pvmvpv, novoiceobs, noasp]])
        test(hydrogen.nonrcd(hydrogen.read_sexp('ot_learning/pseudo-korean.sexp',
                                        'nonrcd')),
             [[idasp, idvoice, idasp_v, idvoice_v, nodh],
              [no_pvmvpv, novoiceobs, noasp]])
    def testEval(self):
        test(ot.eval(lambda x:x+1, 12, 2), 13)
        test(ot.eval(lambda x,y:x+y, 12, 2), 14)
    def testMarked(self):
        test(ot.marked(lambda x:x + 1), True)
        test(ot.marked(lambda x,y:x+1), False)
        test(ot.marked(lambda *x:x+[]), False)
    def testBounds(self):
        pass
    def testSimplyBounds(self):
        test(ot.simply_bounds([2,0,0,0], [0,0,1,1]), False)
        test(ot.simply_bounds([0,0,1,2], [0,0,1,1]), True)
        test(ot.simply_bounds([2,0,0,0], [1,0,0,1]), False)
        test(ot.simply_bounds([0,0,1,1], [0,0,1,1]), False)
        test(ot.simply_bounds([2,0], (2,0)), False)
    def testRemoveNs(self):
        test(faith.remove_ns(range(5), []), [0,1,2,3,4])
        test(faith.remove_ns(range(5), [0,4]), [1,2,3])
        test(faith.remove_ns(range(5), [3]), [0,1,2,4])
        self.assertRaises(IndexError, faith.remove_ns, [], [0,4])
        test(faith.remove_ns(range(5), [0,1,2,3,4]), [])
    def testMaxRepair(self):
        test(set(faith.max_repair('tinkomati', 'inkomai')),
             set(qw('inkomai tinkomai inkomati tinkomati')))
        test(set(faith.max_repair('inkomai', 'komai')),
             set(qw('ikomai nkomai inkomai komai')))
        test(set(faith.max_repair('inkomai', 'komati')),
             set(qw('ikomati nkomati inkomati komati')))
        test(set(faith.max_repair('inkomai', 'ikomati')),
             set(qw('ikomati inkomati')))
    def testDepRepair(self):
        test(set(faith.dep_repair('inkomai', 'komati')),
             set(qw('komai komati')))
        test(set(faith.dep_repair('inkomai', 'inkomati')),
             set(qw('inkomati inkomai')))
        test(set(faith.dep_repair('inkomai', 'tinkomati')),
             set(qw('tinkomati inkomai tinkomai inkomati')))
        test(set(faith.dep_repair('inkomai', 'komai')),
             set(qw('komai')))
        test(set(faith.dep_repair('', 'foo')),
             set([''] + qw('f o fo oo foo')))
    def testOnset(self):
        test(set(mark.onset_repair('inkomai')),
             set(qw('inkomai inkoma inkomati ' +
                    'komai koma komati ' +
                    'tinkomai tinkoma tinkomati')))
    def testGenRepair(self):
        test(ot.gen_repair('inkomai',
                            [mark.onset_repair],
                            [faith.dep_repair,
                             faith.dep_init_repair,
                             faith.max_repair]),
             set(['nkomati',
                  'koma',
                  'tikoma',
                  'nkomai',
                  'inkomati',
                  'tikomati',
                  'ikomati',
                  'tinkomati',
                  'tinkoma',
                  'komai',
                  'tikomai',
                  'ikoma',
                  'komati',
                  'inkomai',
                  'tinkomai',
                  'inkoma',
                  'ikomai',
                  'nkoma']))
    def testBoundingTree(self):
        winners = ot.gen_repair('inkomai',
                                 [mark.onset_repair],
                                 [faith.dep_repair,
                                  faith.dep_init_repair,
                                  faith.max_repair])
        winner_profiles = [[ot.eval(con, output, 'inkomai')
                            for con in [mark.onset,
                                        faith.depIO,
                                        faith.depInitSigma,
                                        faith.maxIO]]
                           for output in winners]
        test(zip(winners, winner_profiles),
             [('nkomati', [0, 1, 0, 1]),
              ('koma', [0, 0, 0, 3]),
              ('ikomati', [1, 1, 0, 1]),
              ('nkomai', [1, 0, 0, 1]),
              ('inkomati', [1, 1, 0, 0]),
              ('tinkomati', [0, 2, 1, 0]),
              ('tinkoma', [0, 1, 1, 1]),
              ('komai', [1, 0, 0, 2]),
              ('tikomati', [0, 2, 1, 1]),
              ('ikoma', [1, 0, 0, 2]),
              ('tikoma', [0, 1, 1, 2]),
              ('komati', [0, 1, 0, 2]),
              ('inkomai', [2, 0, 0, 0]),
              ('tinkomai', [1, 1, 1, 0]),
              ('inkoma', [1, 0, 0, 1]),
              ('ikomai', [2, 0, 0, 1]),
              ('tikomai', [1, 1, 1, 1]),
              ('nkoma', [0, 0, 0, 2])])
        tree = ot.bounding_tree(winner_profiles)
        test(tree,
             ([1, 1, 1, 1],
              [([1, 1, 1],
                [([0, 3], [([3], []), ((0,), [])]),
                 ([1, 2], [([3], []), ((1,), [])]),
                 ((2, 1), [])]),
               ([1, 0, 1],
                [([0, 3], [([3], []), ((0,), [])]),
                 ([1, 1], [([3], []), ((2,), [])]),
                 ((2, 0), [])]),
               ([1, 1, 1],
                [([1, 2], [([3], []), ((1,), [])]),
                 ([1, 1], [([3], []), ((2,), [])]),
                 ([2, 1], [((1,), []), ((2,), [])])]),
               ([1, 1, 1],
                [((2, 1), []),
                 ((2, 0), []),
                 ([2, 1], [((1,), []), ((2,), [])])])]))
        test(ot.bounds([2,0,0,0], tree), False)
        test(ot.bounds([0,0,0,2], tree), False)
        bounders = [(cand,prof) for (cand,prof) in zip(winners,winner_profiles)
                    if not ot.bounds(prof, tree)]
        test(bounders,
             [('nkomati', [0, 1, 0, 1]),
              ('koma', [0, 0, 0, 3]),
              ('ikomati', [1, 1, 0, 1]),
              ('nkomai', [1, 0, 0, 1]),
              ('inkomati', [1, 1, 0, 0]),
              ('tinkomati', [0, 2, 1, 0]),
              ('tinkoma', [0, 1, 1, 1]),
              ('komati', [0, 1, 0, 2]),
              ('inkomai', [2, 0, 0, 0]),
              ('tinkomai', [1, 1, 1, 0]),
              ('inkoma', [1, 0, 0, 1]),
              ('tikomai', [1, 1, 1, 1]),
              ('nkoma', [0, 0, 0, 2])])
        test(ot.bounding_tree(map(snd, bounders)), tree)
    def testCandidateTree(self):
        test(ot.candidate_tree([('cost][us', [1,1,0,0,0,]),
                                ('cos]t[us', [0,1,0,0,1,]),
                                ('cos][tus', [0,0,1,0,0,]),]),
             (([('cost][us', [1, 1, 0, 0, 0]),
                ('cos]t[us', [0, 1, 0, 0, 1]),
                ('cos][tus', [0, 0, 1, 0, 0])],
               [1, 1, 1, 0, 1]),
 [(([('cos]t[us', (1, 0, 0, 1)), ('cos][tus', (0, 1, 0, 0))], [1, 1, 0, 1]),
   [(('cos][tus', (1, 0, 0)), []),
    (('cos]t[us', (1, 0, 1)), []),
    (([('cos]t[us', (1, 0, 1)), ('cos][tus', (0, 1, 0))], [1, 1, 1]),
     [(('cos][tus', (1, 0)), []),
      (('cos]t[us', (1, 1)), []),
      (('cos][tus', (0, 1)), [])]),
    (('cos][tus', (0, 1, 0)), [])]),
  (('cos][tus', (0, 1, 0, 0)), []),
  (([('cost][us', (1, 1, 0, 0)), ('cos]t[us', (0, 1, 0, 1))], [1, 1, 0, 1]),
   [(('cos]t[us', (1, 0, 1)), []),
    (([('cost][us', (1, 0, 0)), ('cos]t[us', (0, 0, 1))], [1, 0, 1]),
     [(('cos]t[us', (0, 1)), []),
      (([('cost][us', (1, 0)), ('cos]t[us', (0, 1))], [1, 1]),
       [(('cos]t[us', (1,)), []), (('cost][us', (1,)), [])]),
      (('cost][us', (1, 0)), [])]),
    (([('cost][us', (1, 1, 0)), ('cos]t[us', (0, 1, 1))], [1, 1, 1]),
     [(('cos]t[us', (1, 1)), []),
      (([('cost][us', (1, 0)), ('cos]t[us', (0, 1))], [1, 1]),
       [(('cos]t[us', (1,)), []), (('cost][us', (1,)), [])]),
      (('cost][us', (1, 1)), [])]),
    (('cost][us', (1, 1, 0)), [])]),
  (([('cost][us', (1, 1, 0, 0)),
     ('cos]t[us', (0, 1, 0, 1)),
     ('cos][tus', (0, 0, 1, 0))],
    [1, 1, 1, 1]),
   [(([('cos]t[us', (1, 0, 1)), ('cos][tus', (0, 1, 0))], [1, 1, 1]),
     [(('cos][tus', (1, 0)), []),
      (('cos]t[us', (1, 1)), []),
      (('cos][tus', (0, 1)), [])]),
    (('cos][tus', (0, 1, 0)), []),
    (([('cost][us', (1, 1, 0)), ('cos]t[us', (0, 1, 1))], [1, 1, 1]),
     [(('cos]t[us', (1, 1)), []),
      (([('cost][us', (1, 0)), ('cos]t[us', (0, 1))], [1, 1]),
       [(('cos]t[us', (1,)), []), (('cost][us', (1,)), [])]),
      (('cost][us', (1, 1)), [])]),
    (([('cost][us', (1, 1, 0)), ('cos][tus', (0, 0, 1))], [1, 1, 1]),
     [(('cos][tus', (0, 1)), []),
      (('cos][tus', (0, 1)), []),
      (('cost][us', (1, 1)), [])])]),
  (([('cost][us', (1, 1, 0, 0)), ('cos][tus', (0, 0, 1, 0))], [1, 1, 1, 0]),
   [(('cos][tus', (0, 1, 0)), []),
    (('cos][tus', (0, 1, 0)), []),
    (('cost][us', (1, 1, 0)), []),
    (([('cost][us', (1, 1, 0)), ('cos][tus', (0, 0, 1))], [1, 1, 1]),
     [(('cos][tus', (0, 1)), []),
      (('cos][tus', (0, 1)), []),
      (('cost][us', (1, 1)), [])])])]))

        test(ot.candidate_tree([('cost][me', [1,0,0,0,0,]),
                                ('cos]t[me', [0,0,0,0,1,]),
                                ('cos][tme', [1,0,1,0,0,]),]),
             (([('cost][me', [1, 0, 0, 0, 0]),
                ('cos]t[me', [0, 0, 0, 0, 1]),
                ('cos][tme', [1, 0, 1, 0, 0])],
               [1, 0, 1, 0, 1]),
 [(('cos]t[me', (0, 0, 0, 1)), []),
  (([('cost][me', (1, 0, 0, 0)),
     ('cos]t[me', (0, 0, 0, 1)),
     ('cos][tme', (1, 1, 0, 0))],
    [1, 1, 0, 1]),
   [(('cos]t[me', (0, 0, 1)), []),
    (([('cost][me', (1, 0, 0)), ('cos]t[me', (0, 0, 1))], [1, 0, 1]),
     [(('cos]t[me', (0, 1)), []),
      (([('cost][me', (1, 0)), ('cos]t[me', (0, 1))], [1, 1]),
       [(('cos]t[me', (1,)), []), (('cost][me', (1,)), [])]),
      (('cost][me', (1, 0)), [])]),
    (([('cost][me', (1, 0, 0)),
       ('cos]t[me', (0, 0, 1)),
       ('cos][tme', (1, 1, 0))],
      [1, 1, 1]),
     [(('cos]t[me', (0, 1)), []),
      (([('cost][me', (1, 0)), ('cos]t[me', (0, 1))], [1, 1]),
       [(('cos]t[me', (1,)), []), (('cost][me', (1,)), [])]),
      (([('cost][me', (1, 0)), ('cos][tme', (1, 1))], [1, 1]),
       [(([('cost][me', (0,)), ('cos][tme', (1,))], [1]), []),
        (('cost][me', (1,)), [])])]),
    (([('cost][me', (1, 0, 0)), ('cos][tme', (1, 1, 0))], [1, 1, 0]),
     [(([('cost][me', (0, 0)), ('cos][tme', (1, 0))], [1, 0]),
       [(('cost][me', (0,)), []),
        (([('cost][me', (0,)), ('cos][tme', (1,))], [1]), [])]),
      (('cost][me', (1, 0)), []),
      (([('cost][me', (1, 0)), ('cos][tme', (1, 1))], [1, 1]),
       [(([('cost][me', (0,)), ('cos][tme', (1,))], [1]), []),
        (('cost][me', (1,)), [])])])]),
  (([('cost][me', (1, 0, 0, 0)), ('cos]t[me', (0, 0, 0, 1))], [1, 0, 0, 1]),
   [(('cos]t[me', (0, 0, 1)), []),
    (([('cost][me', (1, 0, 0)), ('cos]t[me', (0, 0, 1))], [1, 0, 1]),
     [(('cos]t[me', (0, 1)), []),
      (([('cost][me', (1, 0)), ('cos]t[me', (0, 1))], [1, 1]),
       [(('cos]t[me', (1,)), []), (('cost][me', (1,)), [])]),
      (('cost][me', (1, 0)), [])]),
    (([('cost][me', (1, 0, 0)), ('cos]t[me', (0, 0, 1))], [1, 0, 1]),
     [(('cos]t[me', (0, 1)), []),
      (([('cost][me', (1, 0)), ('cos]t[me', (0, 1))], [1, 1]),
       [(('cos]t[me', (1,)), []), (('cost][me', (1,)), [])]),
      (('cost][me', (1, 0)), [])]),
    (('cost][me', (1, 0, 0)), [])]),
  (([('cost][me', (1, 0, 0, 0)),
     ('cos]t[me', (0, 0, 0, 1)),
     ('cos][tme', (1, 0, 1, 0))],
    [1, 0, 1, 1]),
   [(('cos]t[me', (0, 0, 1)), []),
    (([('cost][me', (1, 0, 0)),
       ('cos]t[me', (0, 0, 1)),
       ('cos][tme', (1, 1, 0))],
      [1, 1, 1]),
     [(('cos]t[me', (0, 1)), []),
      (([('cost][me', (1, 0)), ('cos]t[me', (0, 1))], [1, 1]),
       [(('cos]t[me', (1,)), []), (('cost][me', (1,)), [])]),
      (([('cost][me', (1, 0)), ('cos][tme', (1, 1))], [1, 1]),
       [(([('cost][me', (0,)), ('cos][tme', (1,))], [1]), []),
        (('cost][me', (1,)), [])])]),
    (([('cost][me', (1, 0, 0)), ('cos]t[me', (0, 0, 1))], [1, 0, 1]),
     [(('cos]t[me', (0, 1)), []),
      (([('cost][me', (1, 0)), ('cos]t[me', (0, 1))], [1, 1]),
       [(('cos]t[me', (1,)), []), (('cost][me', (1,)), [])]),
      (('cost][me', (1, 0)), [])]),
    (([('cost][me', (1, 0, 0)), ('cos][tme', (1, 0, 1))], [1, 0, 1]),
     [(([('cost][me', (0, 0)), ('cos][tme', (0, 1))], [0, 1]),
       [(([('cost][me', (0,)), ('cos][tme', (1,))], [1]), []),
        (('cost][me', (0,)), [])]),
      (([('cost][me', (1, 0)), ('cos][tme', (1, 1))], [1, 1]),
       [(([('cost][me', (0,)), ('cos][tme', (1,))], [1]), []),
        (('cost][me', (1,)), [])]),
      (('cost][me', (1, 0)), [])])]),
  (([('cost][me', (1, 0, 0, 0)), ('cos][tme', (1, 0, 1, 0))], [1, 0, 1, 0]),
   [(([('cost][me', (0, 0, 0)), ('cos][tme', (0, 1, 0))], [0, 1, 0]),
     [(([('cost][me', (0, 0)), ('cos][tme', (1, 0))], [1, 0]),
       [(('cost][me', (0,)), []),
        (([('cost][me', (0,)), ('cos][tme', (1,))], [1]), [])]),
      (('cost][me', (0, 0)), []),
      (([('cost][me', (0, 0)), ('cos][tme', (0, 1))], [0, 1]),
       [(([('cost][me', (0,)), ('cos][tme', (1,))], [1]), []),
        (('cost][me', (0,)), [])])]),
    (([('cost][me', (1, 0, 0)), ('cos][tme', (1, 1, 0))], [1, 1, 0]),
     [(([('cost][me', (0, 0)), ('cos][tme', (1, 0))], [1, 0]),
       [(('cost][me', (0,)), []),
        (([('cost][me', (0,)), ('cos][tme', (1,))], [1]), [])]),
      (('cost][me', (1, 0)), []),
      (([('cost][me', (1, 0)), ('cos][tme', (1, 1))], [1, 1]),
       [(([('cost][me', (0,)), ('cos][tme', (1,))], [1]), []),
        (('cost][me', (1,)), [])])]),
    (('cost][me', (1, 0, 0)), []),
    (([('cost][me', (1, 0, 0)), ('cos][tme', (1, 0, 1))], [1, 0, 1]),
     [(([('cost][me', (0, 0)), ('cos][tme', (0, 1))], [0, 1]),
       [(([('cost][me', (0,)), ('cos][tme', (1,))], [1]), []),
        (('cost][me', (0,)), [])]),
      (([('cost][me', (1, 0)), ('cos][tme', (1, 1))], [1, 1]),
       [(([('cost][me', (0,)), ('cos][tme', (1,))], [1]), []),
        (('cost][me', (1,)), [])]),
      (('cost][me', (1, 0)), [])])])]))

        test(ot.candidate_tree([('cost',     [1,0,0,0,0,]),
                                ('cos]t',    [0,0,0,1,1,])]),
             (([('cost', [1, 0, 0, 0, 0]),
                ('cos]t', [0, 0, 0, 1, 1])],
               [1, 0, 0, 1, 1]),
 [(('cos]t', (0, 0, 1, 1)), []),
  (([('cost', (1, 0, 0, 0)), ('cos]t', (0, 0, 1, 1))], [1, 0, 1, 1]),
   [(('cos]t', (0, 1, 1)), []),
    (([('cost', (1, 0, 0)), ('cos]t', (0, 1, 1))], [1, 1, 1]),
     [(('cos]t', (1, 1)), []),
      (('cost', (1, 0)), []),
      (('cost', (1, 0)), [])]),
    (('cost', (1, 0, 0)), []),
    (('cost', (1, 0, 0)), [])]),
  (([('cost', (1, 0, 0, 0)), ('cos]t', (0, 0, 1, 1))], [1, 0, 1, 1]),
   [(('cos]t', (0, 1, 1)), []),
    (([('cost', (1, 0, 0)), ('cos]t', (0, 1, 1))], [1, 1, 1]),
     [(('cos]t', (1, 1)), []),
      (('cost', (1, 0)), []),
      (('cost', (1, 0)), [])]),
    (('cost', (1, 0, 0)), []),
    (('cost', (1, 0, 0)), [])]),
  (('cost', (1, 0, 0, 0)), []),
  (('cost', (1, 0, 0, 0)), [])]))
import test_sexp
import test_rcd
suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestHydrogen),
    unittest.TestLoader().loadTestsFromTestCase(test_sexp.TestSexp),
    unittest.TestLoader().loadTestsFromTestCase(test_rcd.TestRcd),
#    OTableauTest.suite,
                            ])
unittest.TextTestRunner().run(suite)
