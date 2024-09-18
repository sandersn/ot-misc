module test-ot
import rcd
import types
import hydrogen
import list
import str
import ot
import faith
fun test(actual: a, expected: a, ?(==): (a, a) -> bool, ?show: a -> string): <console/console,exn> ()
  if actual == expected
    then print(".")
    else throw("\t\texpected \n" ++ expected.show ++ "\n\t\tbut got \n" ++ actual.show ++ "\n")
value type test
  Test<a>(name: string, f: () -> io ())
fun testall(tests: list<test>)
  tests.foreach fn (Test(name,f))
    try(f) fn (exn)
      // augment message  with name and number of failures in this test case
      println(name ++ " failed.\n" ++ exn.message)
val testo = [
  Test("abs-to-relative", fn ()
    // abs is without titles right now
    val abs = [["foo", "foo", "", "1", "", "2"],
                ["", "oof","1",  "", "", "1"],
                ["", "oaf", "",  "2", "", ""]]
    // This is the "backward language" so foo -> oof
    val rel = [[1,0,1],
              [2,0,-1]]
    test(rel, abs-to-relative(abs))
  ),
  Test("test-read-sexp", fn ()
    val expected = zipwith([hydrogen/idasp, hydrogen/idvoice, hydrogen/idasp/v,
                    hydrogen/idvoice/v, hydrogen/no-pvmvpv, hydrogen/no-dh,
                    hydrogen/no-voiceobs, hydrogen/no-asp],
                    [[0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 0, 1, 1, 0, 0, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 0, 1, 1, 0, 0, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 0, 1, 1, 0, 0, 1, 1],
                    [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 2, 1, 2, 1, 1, 0, 1, 0, 2, 1, 2, 1, 0, 1, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 1, 0, 1, 0, 2, 1, 2, 1, 1, 1, 0, 2, 1, 2, 1, 0, 1, 0, 1, 1, 2, 1, 2, 0, 1, 1, 1, 2, 1, 2, 1, 0, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 1, 0, 1, 1, 2, 1, 2],
                    [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 0, 1, 1, 0, 0, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 0, 1, 1, 0, 0, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                    [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 2, 1, 2, 1, 1, 0, 1, 0, 2, 1, 2, 1, 0, 1, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 1, 0, 1, 0, 2, 1, 2, 1, 1, 1, 0, 2, 1, 2, 1, 0, 1, 0, 1, 1, 2, 1, 2, 0, 1, 1, 1, 2, 1, 2, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, -1, -1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, -1, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, -1, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 2],
                    [1, 0, 1, 0, 1, 1, -1, -1, 0, 0, 1, 1, 1, 0, 1, -1, -1, 0, 0, 1, 0, 1, -1, 0, -1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, -1, 0, -1, 0, 0, 1, 0, 1, -1, -1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 2, 1, 2, 0, 1, 1, 1, 2, 1, 2, 1, 0, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 1, 0, 1, 1, 2, 1, 2],
                    [0, 1, 1, -1, -1, 0, 0, 1, 1, -1, -1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, -1, -1, 0, -1, -1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, -1, -1, 0, 0, -1, -1, 0, 0, 0, 1, 1, 0, 0, 1, 1, -2, -2, -1, -1, -2, -2, -1, -1, -1, -1, 0, -1, -1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, -1, -1, 0, 0, -1, -1, 0, 0, 0, 1, 1, 0, 0, 1, 1]], Column)
    val actual = read-sexp("ot_learning/pseudo-korean.sexp")
    test(actual, expected) 
  ),
  Test("test-all-methods", fn ()
    test(rcd(read-sexp("ot_learning/pseudo-korean.sexp")),
      [[idasp, idvoice, idasp/v, idvoice/v, no-dh],
      [no-pvmvpv, no-voiceobs, no-asp]])
  ),
  Test("test-eval", fn ()
    test(ot/eval(Mark("mark-length", count), ["hi"]), 2)
    test(ot/eval(Faith("faith-length", fn (x,y) (x++y).count), ["hi", "there"]), 7)
  ),
  Test("test-bounds1", fn ()
    test(simply-bounds([2,0,0,0], [0,0,1,1]), False)
  ),
  Test("test-bounds2", fn ()
    test(simply-bounds([0,0,1,2], [0,0,1,1]), True)
  ),
  Test("test-bounds3", fn ()
    test(simply-bounds([2,0,0,0], [1,0,0,1]), False)
  ),
  Test("test-bounds4", fn ()
    test(simply-bounds([0,0,1,1], [0,0,1,1]), False)
  ),
  Test("test-bounds5", fn ()
    test(simply-bounds([2,0], [2,0]), False)
  ),
  Test("exclude1", fn () 
    test(exclude(iota(5), []), [0,1,2,3,4])
  ),
  Test("exclude2", fn () 
    test(exclude(iota(5), [0,4]), [1,2,3])
  ),
  Test("exclude3", fn () 
    test(exclude(iota(5), [3]), [0,1,2,4])
  ),
  Test("exclude4", fn () 
    // self.assertRaises(IndexError, faith.remove_ns, [], [0,4])
    ()
  ),
  Test("exclude5", fn () 
    test(exclude(iota(5), [0,1,2,3,4]), [])
  ),
  Test("max-repair1", fn ()
    test(faith/max-repair("tinkomati", "inkomai"),
         qw("inkomai tinkomai inkomati tinkomati"))
  ),
  Test("max-repair2", fn ()
    test(faith/max-repair("inkomai", "komai"),
         qw("ikomai nkomai inkomai komai"))
  ),
  Test("max-repair3", fn ()
    test(faith/max-repair("inkomai", "komati"),
         qw("ikomati nkomati inkomati komati"))
  ),
  Test("max-repair4", fn ()
    test(faith/max-repair("inkomai", "ikomati"),
         qw("ikomati inkomati"))
  ),
]
pub fun main ()
  testall(testo)
  println("")
