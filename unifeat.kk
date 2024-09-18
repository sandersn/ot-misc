module unifeat
import types
import map
val phonemes: list<(char, features)> = [
  ('a', [("cons",No),("son",Yes),("high", No), ("low", Yes), ("back", No), ("ATR", No), ("round", No), ("approx",Yes), ("contin",Yes)]),
  ('b', [("cons", Yes), ("son", No), ("place", Place("labial")), ("voice", Yes), ("contin", No), ("approx",No)]),
  ('c', [("cons", Yes), ("son", No), ("place", Place("coronal")), ("voice", No), ("contin", No), ("approx",No), ("anterior",No),]),
  ('d', [("cons", Yes), ("son", No), ("place", Place("coronal")), ("voice", Yes), ("contin", No), ("approx",No), ("anterior",Yes)]),
  ('e', [("cons",No),("son",Yes),("high", No), ("low", No), ("back", No), ("ATR", Yes), ("round", No), ("approx",Yes), ("contin",Yes)]),
  ('p', [("cons", Yes), ("son", No), ("place", Place("labial")), ("voice", No), ("contin", No), ("approx",No)]),
]
pub fun unify(s: string): exn list<features>
    return s.list.map fn (c) phonemes.assoc(c).unjust
