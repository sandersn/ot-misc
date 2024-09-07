from util.lst import fst,snd
import unittest
import rcd
import faith
import mark
test = None
class TestRcd(unittest.TestCase):
    def setUp(self):
        global test
        test = self.assertEqual
## belongs in test_bcd.py when I get to that
##     def testSubsets(self):
##         test(bcd.subsets([1,2,3],1), [[1],[2],[3]])
##         test(bcd.subsets([1,2,3],2), [[1,2],[1,3]])
    def testfilterby(self):
        test(rcd.filterby(bool, [0,1,1,0,1], "hullo"), list('ulo'))
        test(rcd.filterby(bool, [0,1,1,0,1], "hull"), ['u','l'])
        test(rcd.filterby(bool, [0,1,1,], "hullo"), list('ul'))
        test(rcd.filterby(lambda _:False, [0,1,1,], "hullo"), [])
    def testmaxby(self):
        test(rcd.maxby(lambda n:-n, [1,2,3,4]), 1)
        test(rcd.maxby(lambda n:n, [1,2,3,4]), 4)
        self.assertRaises(ValueError, rcd.maxby, lambda n:-n, [])
        self.assertRaises(ValueError, max, [])
    def testplateau(self):
        def oddp(n): return n % 2
        test(rcd.plateau([1,1,2]), [1,1])
        test(rcd.plateau([1,2,3]), [1])
        test(rcd.plateau([1,3,5,4,6,7], key=oddp), [1,3,5])
        test(rcd.plateau([]), [])
        test(rcd.plateau([1,1,1,]), [1,1,1])
## belongs in test_gla.py when I get to that (if ever)
##     def testbin_key(self):
##         test(rcd.bin_key(lambda n,m:n+1==m-1, lambda n:n*2)(1,2), True)
##         test(rcd.bin_key(lambda n,m:n+1==m-1, lambda n:n*2)(2,1), False)
    def testkeyedsetdiff(self):
        test(rcd.keyedsetdiff('abc', 'abd'), list('c'))
        test(rcd.keyedsetdiff([('a',1),('b',1),('c',2)],
                              [('a',2),('b',2),('d',3)], key=fst), [('c',2)])
        test(rcd.keyedsetdiff('abc', ''), list('abc'))
        test(rcd.keyedsetdiff('', 'abc'), [])
        test(rcd.keyedsetdiff(['idasp', 'idvoice', 'idasp_v', 'idvoice_v',
                               'no_pvmvpv', 'nodh', 'novoiceobs', 'noasp'],
                              ['nodh']),
             ['idasp', 'idvoice', 'idasp_v', 'idvoice_v',
              'no_pvmvpv', 'novoiceobs', 'noasp'])
        test(set('abc') - set('abd'), set('c'))
    def testTable(self):
        test(rcd.table((('fo', 'foo'),
                        ('fo', 'fa'),
                        ('fo', 'f')),
                       [faith.maxIO, faith.depIO, mark.no_low],
                       "fo"),
             [(faith.maxIO, [0, 0, 1]),
              (faith.depIO, [1, 0, 0]),
              (mark.no_low, [0, 1, 0])])
    def testOneLiners(self):
        test(rcd.positive(1), True)
        test(rcd.positive(0), False)
        test(rcd.positive(-1), False)
        test(rcd.negative(1), False)
        test(rcd.negative(0), False)
        test(rcd.negative(-1), True)
        test(rcd.win_fav([]), False)
        test(rcd.win_fav([1,1]), True)
        test(rcd.win_fav([0,0]), False)
        test(rcd.win_fav([0,1]), True)
        test(rcd.tied([]), True)
        test(rcd.tied([0,1]), False)
        test(rcd.tied([0,0,0]), True)
        test(rcd.lose_disfav([]), True)
        test(rcd.lose_disfav([0,0,0]), True)
        test(rcd.lose_disfav([1,1,1]), True)
        test(rcd.lose_disfav([-1,-1,1]), False)
        test(rcd.lose_disfav([-1, 0, 0]), False)
        test(rcd.markcol((faith.maxIO, [1,1,1])), False)
        test(rcd.markcol((mark.no_low, [0,1,1])), True)
        test(rcd.fav_active((faith.depIO,[])), False)
        test(rcd.fav_active((faith.depIO,[1,1])), True)
        test(rcd.fav_active((faith.depIO,[0,0])), False)
        test(rcd.fav_active((faith.maxIO,[0,1])), True)
    def testaddstratum(self):
        test(rcd.add_stratum([('still',[1,1,1]),('a',[0,0,0])],
                             [['total'], ['fake']]),
             [['still', 'a'], ['total'], ['fake']])
        test(rcd.add_stratum([], 'total fake'.split()),
             [[]] + 'total fake'.split())
    def testfilter_rows(self):
        test(rcd.filter_rows([('Max',     [0,2,0,1,1]),
                              ('Dep-init',[1,0,0,0,1])],
                             [('Onset',   [-1,-1,1,0,-1]),
                              ('Dep',     [1, 0,-1,-1,0])]),
             [('Onset', (1,)),
              ('Dep', (-1,))])
        test(rcd.filter_rows([('Onset', [1])],
                             [('Dep', [-1])]),
             [('Dep', [])])
    def testRcd(self):
        test(rcd.rcd([('Onset',   [-1,-1,1,0,-1]),
                      ('Max',     [0,2,0,1,1]),
                      ('Dep',     [1,0,-1,-1,0]),
                      ('Dep-init',[1,0,0,0,1])]),
             [['Max','Dep-init'],['Onset'],['Dep']])
        test(rcd.rcd(rcd.table((('fo', 'foo'),
                                ('fo', 'fa'),
                                ('fo', 'f')),
                               [faith.maxIO, faith.depIO, mark.no_low],
                               "fo")),
             [[faith.maxIO, faith.depIO, mark.no_low]])
    def testNonRcd(self):
        test(rcd.nonrcd([('Onset',   [-1,-1,1,0,-1]),
                         ('Max',     [0,2,0,1,1]),
                         ('Dep',     [1,0,-1,-1,0]),
                         ('Dep-init',[1,0,0,0,1])]),
             [['Max','Dep-init'],['Onset'],['Dep']])
        test(rcd.nonrcd(rcd.table((('fo', 'foo'),
                                   ('fo', 'fa'),
                                   ('fo', 'f')),
                                  [faith.maxIO, faith.depIO, mark.no_low],
                                  "fo")),
             [[faith.maxIO, faith.depIO, mark.no_low]])
suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestRcd),
                            ])
if __name__=="__main__":
    unittest.TextTestRunner().run(suite)
