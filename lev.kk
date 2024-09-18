module lev
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
alias table = list<list<int>>
pub fun levenshtein(s1: string, s2: string): table
  []
pub fun optimal(table: table): list<(operation, (int, int))>
  []
