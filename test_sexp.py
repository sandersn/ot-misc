import unittest
from sexp import read, _atom
test = None
class TestSexp(unittest.TestCase):
    def setUp(s):
        global test
        test = s.assertEqual
    def test_atom(s):
        test(_atom("#t"), True)
        test(_atom("#f"), False)
        test(_atom('1001'), 1001)
        test(_atom('1.1'), 1.1)
        test(_atom("foo"), 'foo')
        test(_atom('"bar"'), 'bar')
    def testRead(s):
        test(read('1 2 3'), [1,2,3])
        test(read('1.1 2 "bear"'), [1.1, 2, 'bear'])
        test(read('1 (1) (2 3 (4)) 5'), [1, [1], [2, 3, [4]], 5])
        test(read('1 (1) (2 3 (4)) 5 ()'), [1, [1], [2,3,[4]], 5, []])
        test(read('(1 . 2)'), [(1,2)])
        test(read('(1 . 2) (3 . 4) (foo . #t) (bar . #f)'),
             [(1, 2), (3, 4), ('foo', True), ('bar', False)])
        test(read('(1 . -1)'), [(1,-1)])
        test(read('(-1 . -1)'), [(-1,-1)])
if __name__=="__main__":
    unittest.main()
