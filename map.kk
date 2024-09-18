module map
import types
pub fun assoc(m : map<k,v>, k : k, ?(==): (k, k) -> bool) : maybe<v>
  match m
    Cons((k1,v1),m1) -> if k1 == k then Just(v1) else assoc(m1,k)
    Nil -> Nothing
