" this isn't principally a unit test but a set of correctness tests"
# -*- coding: utf-8 -*-
import unittest
from unifeat import phonemes
from util import dct
def all_features(phonemes, cons=None):
    all = set()
    for fs in phonemes.values():
        if cons is None or ('cons' in fs and fs['cons']==cons):
            all.update(fs.keys())
    return all
def shared_features(phonemes, cons=None):
    shared = set()
    for fs in phonemes.values():
        if cons is None or ('cons' in fs and fs['cons']==cons):
            shared.intersection_update(fs.keys())
    return shared
def duplicates(phonemes):
    return filter(
        lambda cs: len(cs) > 1,
        dict.values(dct.collapse_pairs((tuple(v.items()), k)
                                       for k,v in phonemes.items())))
def remove_features(phonemes, *fs):
    return dct.map(lambda ph: dct.except_(ph, *fs), phonemes)
def restrict_features(phonemes, *fs):
    return dct.map(lambda ph: dct.extract(ph, *fs), phonemes)
# TODO:need to check for shared values, not just shared features.
# for example I asssert that all vowels are approximant. Is this so?
# TODO: Check for identical values
# TODO:make a real test class
test = None # this is a dirty hack, but I HATE typing self.assertEqual
qw = str.split
class TestUnifeat(unittest.TestCase):
    def setUp(self):
        global test
        self.conss = dct.filter_values(lambda v:'cons' in v and v['cons'], phonemes)
        self.vowels = dct.filter_values(lambda v:'cons' in v and not v['cons'],
                                 phonemes)
        test = self.assertEqual
    def testDuplicates(self):
        test(duplicates(phonemes), map(str.split, """k q
ç ʂ ʃ
ʋ ʙ
ɳ ɲ
ɑ a
ɢ g
ʈ c
ɭ ʎ
ɱ m
h χ ʰ
ə ɜ
ɻ j
ɰ ʀ
ɦ ʁ
ʝ ʐ ʒ
ɟ ɖ
ŋ ɴ
ʉ ʊ""".split('\n')))
        
if __name__=="__main__":
    print all_features(phonemes)
    print all_features(phonemes, cons=True)
    print all_features(phonemes, cons=False)
    print 'before' #remove_features(dct.filter_values(lambda v:'cons' in v and v['cons'], phonemes), 'anterior', 'back')
    for dups in duplicates(remove_features(dct.filter_values(lambda v:'cons' in v and v['cons'], phonemes), 'anterior', 'back')):
        for dup in dups:
            print dup,
        print
    print 'after'
    suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestUnifeat),
                            ])
    unittest.TextTestRunner().run(suite)
