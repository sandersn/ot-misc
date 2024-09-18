module ot
import types
// TODO: I really want some way that doesn't rely on passing the right number of arguments to eval
// *probably* this means that Mark should take an input and ignore it.
pub fun eval(constraint: constraint, inputs: list<string>): int
  match constraint
    Mark(_, f) -> 
      match inputs
        [candidate] -> f(candidate)
        _ -> 0
    Faith(_, f) -> 
      match inputs
        [input, candidate] -> f(input, candidate)
        _ -> 0
// TODO: This looks like it should be running on list<erc>s
/**
 * 1. There must be at least one winner.
 * 2. There must be no losers; otherwise this candidate is worse than the bound.
 */
pub fun simply-bounds(candidates: list<int>, bounds: list<int>, anyWinner = False): bool
  match candidates
    [] -> anyWinner
    Cons(c, cands) ->
      match bounds
        [] -> anyWinner
        Cons(b, bounds) -> b <= c && simply-bounds(cands, bounds, b < c || anyWinner)
