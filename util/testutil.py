from cl import *

def test(title, actual, expected):
    if actual==expected:
        print "%s passed: %s" % (title, actual)
    else:
        print "*** %s failed:\nactual: %s\nexpected: %s" % (title,
                                                            actual,
                                                            expected)
lt2 = lambda n: n<2
test('count', count(2, (2,3,2,4,4,0,2)), 3)
test('count-if', countif(lt2, range(5)), 2)
test('count-if-not', countifnot(lt2, range(5)), 3)
test('count-end', count(2, (2,3,2,4,4,0,2), fromend=True), 3)
test('find', find(2, (2,3,2,4,4,0,2)), 2)
test('find-if', findif(lt2, range(5)), 0)
test('find-if-not', findifnot(lt2, range(5)), 2)
test('find-end', find(2, (2,3,2,4,4,0,2), fromend=True), 2)
test('position', position(2, (2,3,2,4,4,0,2)), 0)
test('position-miss', position(6, (2,3,2,4,4,0,2)), None)
test('position-nil', position(6, ()), None)
test('position-if', positionif(lt2, range(5)), 0)
test('position-if-not', positionifnot(lt2, range(5)), 2)
test('position-end', position(2, (2,3,2,4,4,0,2), fromend=True), 6)

