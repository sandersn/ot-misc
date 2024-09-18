module list
pub fun transpose(rows: list<list<a>>, acc: list<list<a>> = []): div list<list<a>>
  // NOTE: Uses exceptions for control-flow >=|
  // This is too easy in Koka
  match rows
    Nil -> acc
    _ -> 
      val column = rows.map(head)
      try {
        rows.map(tail).transpose(Cons(column.map(fn (x) x.unjust), acc))
      } fn (e) acc
// TODO: Only used in tests; inline this function
pub fun iota(n: int, acc = []): list<int>
  list(0, n - 1)
pub fun count(l: list<a>, f: a -> bool): int
  l.foldl(0, fn (acc, x) if f(x) then acc + 1 else acc)
