module lev
import types
import list
pub type operation
  Sub
  Ins
  Del
pub fun (==)(a: operation, b: operation): bool
  match (a, b)
    (Sub, Sub) -> True
    (Ins, Ins) -> True
    (Del, Del) -> True
    _ -> False
pub alias table = list<list<int>>
// copied from lev.ml, because I think that's the newest functional/foldleft version
fun window2(l: list<a>): div list<(a,a)>
  match l
    [] -> []
    [_] -> []
    Cons(x, Cons(y, rest)) -> Cons((x,y), window2(Cons(y, rest)))
fun lev(s1: list<a>, s2: list<a>, indel: int, delete: a -> int, insert: a -> int, subst: (a, a) -> int): <console/console,exn,div> table
  val s2-len = s2.length
  val table: table = [Cons(s2-len, s2.map-indexed fn (i,_) indel * (s2-len - i))]
  val column = zip(s1,s1.map-indexed fn (i,_) indel * (i+1))
  val yy: table = column.foldl(table, fn(tab, (c1,i)) 
    match tab
      Cons(prev,_) -> 
        val row = zip(s2, prev.reverse.window2).foldl([i], fn (row, k) 
          match (row, k)
            (Cons(last,_), (c2, (j, jp1))) -> 
              Cons(minimum([
                  j + delete(c1), 
                  jp1 + subst(c1, c2), 
                  last + insert(c2)
                ]), 
                row)
            _ -> throw("Terrible error (inner)")
        )
        Cons(row,tab)
      Nil -> throw("Terrible error (outer)")
  )
  yy 
pub fun levenshtein(s1: string, s2: string): <exn,console/console,div> table
  lev(s1.list, s2.list, 1, fn (_) 1, fn (_) 1, fn (c1, c2) if c1 == c2 then 0 else 2)
pub fun optimal(table: table): list<(operation, (int, int))>
  []
pub fun flevenshtein(s1: list<features>, s2: list<features>, avgdistance: int): <exn,console/console,div> table
  lev(s1, s2, avgdistance, fn (_) avgdistance, fn (_) avgdistance, feature-distance)
// ad-hoc set/map functions
fun contains-key(fs: features, f: string): bool
  fs.find(fn ((g,_)) g == f).bool
fun diff-count(f1: features, f2: features): int
  f1.count(fn ((f,_)) !f2.contains-key(f)) 
  + f2.count(fn ((f,_)) !f1.contains-key(f))
fun intersect-keys-unshared-values-count(f1: features, f2: features): int
  f1.count(fn ((f,v))
    f2.find (fn ((g,w))
      f == g && w != v
    ).bool
  )
fun feature-distance(f1: features, f2: features): int
  f1.diff-count(f2) * 2 + f1.intersect-keys-unshared-values-count(f2)
