module faith
import types
import lev
pub fun exclude(l: list<a>, indices: list<int>): list<a>
  fun iter(xs: list<a>, ns: list<int>, i: int = 0, acc: list<a> = []): list<a>
    match ns
      [] -> acc.reverse ++ xs
      Cons(n, rest) -> 
        match xs
          [] -> acc.reverse
          Cons(x, xs) ->
            if n == i 
              then iter(xs, rest, i + 1, acc)
              else iter(xs, ns, i + 1, Cons(x, acc))
  iter(l, indices)
// TODO: vector indexing has an exn effect
fun unaligned-chars(input: string, output: string, operation: lev/operation): exn list<(int, char)>
  var chars := []
  var offset := 0
  val x = levenshtein(input, output).optimal
  x.foreach fn ((op, (start, _)))
    if op == operation && op == Del
      then chars := Cons((start + offset, input.vector[start]), chars)
      else if op == operation && op == Ins
        then chars := Cons((start+offset, ' ' /*-1*/), chars)
        else if op == Del
          then offset := offset - 1
          else if op == Ins
            then offset := offset + 1
            else ()
  chars.reverse
fun powerset(l: list<a>): list<list<a>>
  []
fun rebuild(output: string, indices: list<(int, char)>): string
  ""
  // if l.is-empty
  //   then Cons([], [])
  //   else
  //     val x = l.head
  //     val xs = l.tail
  //     val ps = powerset(xs)
  //     ps ++ ps.map(fn (t) Cons(x, t))
pub fun max-repair(input: string, output: string): exn list<string>
  unaligned-chars(input, output, lev/Del).powerset.map fn (cs) output.rebuild(cs)
