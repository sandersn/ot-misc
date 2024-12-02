import type { Word } from "./word.ts"
export type Faith = {
  kind: "faith"
  name: string
  eval(input: string, output: string): number
}
export type Mark = {
  kind: "mark"
  name: string
  eval(input: string): number
}
export type Constraint = Faith | Mark
export type Stratum = Constraint[]
export type Strata = Stratum[]
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
}
export type Foot = {
  s1: Syllable
  s2?: Syllable
}
// TODO: Unify these with normal faith/mark once I have a good representation for each
export type StressFaith = {
  kind: "faith"
  name: string
  evaluate(underlying: Word, parse: Word): number
}
export type StressMark = {
  kind: "mark"
  name: string
  evaluate(parse: Word): number
}
export type StressConstraint = StressMark | StressFaith

export function Faith(name: string, faith: (input: string, output: string) => number): Faith {
  return { kind: "faith", name, eval: faith }
}
export function Mark(name: string, mark: (input: string) => number): Mark {
  return { kind: "mark", name, eval: mark }
}
export function StressFaith(name: string, evaluate: (overt: Word, parse: Word) => number): StressFaith {
  return { kind: "faith", name, evaluate }
}
export function StressMark(name: string, evaluate: (overt: Word) => number): StressMark {
  return { kind: "mark", name, evaluate }
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
  constraint: Constraint
  violations: Erc[]
}
export function Column(constraint: Constraint, violations: Erc[]): Column {
  return { constraint, violations }
}
export type MarkColumn = {
  constraint: Constraint
  violations: number[]
}
export function MarkColumn(constraint: Constraint, violations: number[]): MarkColumn {
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
