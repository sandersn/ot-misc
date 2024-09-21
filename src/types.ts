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
/**
 * L = lose
 * W = win
 * E = equal
 */
export type Erc = 'l' | 'w' | 'e'
export type Constraint = Faith | Mark
export type Stratum = Constraint[]
export type Strata = Stratum[]
export function Faith(name: string, faith: (input: string, output: string) => number): Faith {
    return { kind: "faith", name, eval: faith }
}
export function Mark(name: string, mark: (input: string) => number): Mark {
    return { kind: "mark", name, eval: mark }
}
// TODO: Also need an absolute column that uses numbers (but most code operates on ERCs)
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

