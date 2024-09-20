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
export function Faith(name: string, faith: (input: string, output: string) => number): Faith {
    return { kind: "faith", name, eval: faith }
}
export function Mark(name: string, mark: (input: string) => number): Mark {
    return { kind: "mark", name, eval: mark }
}
export type Column = {
    constraint: Constraint
    violations: number[]
}
export function Column(constraint: Constraint, violations: number[]): Column {
    return { constraint, violations }
}

