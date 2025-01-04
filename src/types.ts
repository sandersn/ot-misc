import type { Word } from "./word.ts"
export type StringFaith = {
  kind: "faith"
  name: string
  eval(input: string, output: string): number
}
export type StringMark = {
  kind: "mark"
  name: string
  eval(input: string): number
}
export type SurfaceConstraint = StringFaith | StringMark
export type Stratum = SurfaceConstraint[]
export type Strata = Stratum[]
/// segment types ///
export type Segment = {
  // TODO: Eventually this should be a real phone
  segment: "c" | "v"
  // TODO: A boolean would be good enough for CVT example
  input?: Segment | undefined
}
/// meter types ///
/**
 * ' = primary
 * ` = secondary
 *  = unstressed
 */
export type Stress = "'" | "`" | ""
/**
 * . = light
 * _ = heavy
 */
export type Weight = "." | "_"
/**
 * Stress only applies to overt and parsed forms. It's always unstressed for underlying forms.
 */
export type Syllable = {
  weight: Weight
  stress: Stress
  onset: Segment | undefined
  nucleus: Segment | undefined
  coda: Segment | undefined
}
export type Foot = {
  s1: Syllable
  s2?: Syllable
}
export type Constraint = {
  name: string
  evaluate(parse: Word): number
}
export function Faith(name: string, faith: (input: string, output: string) => number): StringFaith {
  return { kind: "faith", name, eval: faith }
}
export function Mark(name: string, mark: (input: string) => number): StringMark {
  return { kind: "mark", name, eval: mark }
}
export function Constraint(name: string, evaluate: (overt: Word) => number): Constraint {
  return { name, evaluate }
}
// TODO: Also need an absolute column that uses numbers (but most code operates on ERCs)
/**
 * l = lose
 * w = win
 * = = equal, tied
 */
export type Erc = "l" | "w" | "="
/**
 * Column of a tableau, relative to another column
 */
export type Column = {
  constraint: SurfaceConstraint
  violations: Erc[]
}
export function Column(constraint: SurfaceConstraint, violations: Erc[]): Column {
  return { constraint, violations }
}
export type MarkColumn = {
  constraint: SurfaceConstraint
  violations: number[]
}
export function MarkColumn(constraint: SurfaceConstraint, violations: number[]): MarkColumn {
  return { constraint, violations }
}
export let features = [
  "cons",
  "son",
  "strid",
  "voice",
  "round",
  "contin",
  "ATR",
  "RTR",
  "high",
  "low",
  "back",
  "approx",
  "nasal",
  "spread gl",
  "constr gl",
  "anterior",
  "lateral",
  "place",
  "boundary",
] as const
export type Phoneme = Partial<Record<(typeof features)[number], boolean | "labial" | "coronal" | "dorsal">>
export type Tree<T> = {
  value: T
  kids: Tree<T>[]
}
export function Tree<T>(value: T, kids: Tree<T>[] = []): Tree<T> {
  return { value, kids }
}
