module types
pub type constraint
  pub Mark(name: string, mark: (string) -> int)
  pub Faith(name: string, faith: (string, string) -> int)
pub fun constraint/show(c: constraint)
  c.name
pub fun constraint/(==)(c1: constraint, c2: constraint) : bool
  c1.name == c2.name
pub alias stratum = list<constraint>
pub alias strata = list<stratum>
pub value struct column
  constraint: constraint
  violations: list<int>
pub alias columnar = list<column>
pub fun show(c: column)
  c.constraint.show ++ ": " ++ c.violations.map(show).join(",")
pub fun column/(==)(c1: column, c2: column) : bool
  c1.constraint == c2.constraint && c1.violations == c2.violations
pub alias csv = list<list<string>>
pub alias map<k,v> = list<(k,v)>
pub value type feature-value
  Yes
  No
  Place(place: string)
pub alias feature = (string, feature-value)
pub alias features = list<feature>
pub fun feature-value/show(v: feature-value): string
  match v
    Yes -> "Yes"
    No -> "No"
    Place(s) -> s
pub fun feature-value/(==)(v1: feature-value, v2: feature-value): bool
  match (v1, v2)
    (Yes, Yes) -> True
    (No, No) -> True
    (Place(s1), Place(s2)) -> s1 == s2
    _ -> False
