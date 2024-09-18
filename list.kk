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
pub fun iota(n: int, acc = []): div list<int>
  if n <= 0
    then acc
    else iota(n - 1, Cons(n - 1, acc))

