export type Faith = {
  kind: "faith";
  name: string;
  eval(input: string, output: string): number;
};
export type Mark = {
  kind: "mark";
  name: string;
  eval(input: string): number;
};
export type Constraint = Faith | Mark;
export type Stratum = Constraint[];
export type Strata = Stratum[];
/// stress types ///
export type Stress = "primary" | "secondary" | "unstressed";
/**
 * Stress only applies to overt and parsed forms. It's undefined for underlying forms.
 * L = light
 * H = heavy
 */
export type Syllable = {
  weight: "l" | "h";
  stress: Stress | undefined;
};
export type Foot = {
  s1: Syllable;
  s2?: Syllable;
};
export function isFoot(s: Foot | Syllable): s is Foot {
  return "s1" in s;
}
export function isSyllable(s: Foot | Syllable): s is Syllable {
  return "weight" in s;
}
/**
 * Additional rules:
 * - Unfooted syllables must be unstressed.
 * - Each foot has exactly one head syllable, which is the only stressed one in that foot.
 * - Head foot's head syllable must have primary stress; other feet's head syllables must have secondary.
 */
export type ProsodicWord = {
  head: Foot;
  feet: (Foot | Syllable)[];
};
// TODO: Unify these with normal faith/mark once I have a good representation for each
export type StressFaith = {
  kind: "faith";
  name: string;
  evaluate(overt: Syllable[], parse: ProsodicWord): number;
  parse(overt: Syllable[], parse: ProsodicWord): ProsodicWord;
  generate(underlying: Syllable[], parse: ProsodicWord): ProsodicWord[];
};
export type StressMark = {
  kind: "mark";
  name: string;
  evaluate(overt: Syllable[]): number;
  parse(overt: Syllable[]): ProsodicWord;
  generate(underlying: Syllable[]): ProsodicWord[];
};
export type StressConstraint = StressMark | StressFaith;

export function Faith(name: string, faith: (input: string, output: string) => number): Faith {
  return { kind: "faith", name, eval: faith };
}
export function Mark(name: string, mark: (input: string) => number): Mark {
  return { kind: "mark", name, eval: mark };
}
export function StressFaith(
  name: string,
  evaluate: (overt: Syllable[], parse: ProsodicWord) => number,
  parse: (overt: Syllable[], parse: ProsodicWord) => ProsodicWord,
  generate: (underlying: Syllable[], parse: ProsodicWord) => ProsodicWord[],
): StressFaith {
  return { kind: "faith", name, evaluate, parse, generate };
}
export function StressMark(
  name: string,
  evaluate: (overt: Syllable[]) => number,
  parse: (overt: Syllable[]) => ProsodicWord,
  generate: (underlying: Syllable[]) => ProsodicWord[],
): StressMark {
  return { kind: "mark", name, evaluate, parse, generate };
}
// TODO: Also need an absolute column that uses numbers (but most code operates on ERCs)
/**
 * L = lose
 * W = win
 * = = equal, tied
 */
export type Erc = "l" | "w" | "=";
/**
 * Column of a tableau, relative to another column
 */
export type Column = {
  constraint: Constraint;
  violations: Erc[];
};
export function Column(constraint: Constraint, violations: Erc[]): Column {
  return { constraint, violations };
}
export type MarkColumn = {
  constraint: Constraint;
  violations: number[];
};
export function MarkColumn(constraint: Constraint, violations: number[]): MarkColumn {
  return { constraint, violations };
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
] as const;
export type Phoneme = Partial<Record<(typeof features)[number], boolean | "labial" | "coronal" | "dorsal">>;
export type Tree<T> = {
  value: T;
  kids: Tree<T>[];
};
export function Tree<T>(value: T, kids: Tree<T>[] = []): Tree<T> {
  return { value, kids };
}
