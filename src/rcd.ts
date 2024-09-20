import { partition, transpose, zip, filterProxy } from "./util/array"
import { Column, Strata } from './types'
function tied(violations: number[]): boolean {
    return violations.every(v => v == 0)
}
function violationsRow(table: Column[]): number[][] {
    return transpose(table.map(c => c.violations))
}
function filterDemoteByPromote(demote: Column[], promote: Column[]): Column[] {
    // TODO: stop transposing demote and promote just to filter their rows.
    // Either keep this algorithm, but have it use indexing, or find indices some other way, and filter all of demote by them.
    let hierarchy = demote.map(c => c.constraint)
    let filteredColumns = transpose(filterProxy(violationsRow(demote), violationsRow(promote), tied))
    return alwaysZip(hierarchy, filteredColumns).map(([c, v]) => Column(c, v))
}
export function rcd(columns: Column[]): Strata {
    let acc: Strata  = []
    while (true) {
        let [demote, promote] = partition(columns, c => c.violations.some(v => v < 0))
        if (demote.length == 0 || promote.length == 0) {
            acc.push(columns.map(c => c.constraint))
            return acc
        } else {
            acc.push(promote.map(c => c.constraint))
            columns = filterDemoteByPromote(demote, promote)
        }
    }
}

function alwaysZip<T, U>(l1: T[], l2: U[][]): Array<[T,U[]]>  {
    return l2.length === 0
        ? l1.map(x => [x, []])
        : zip(l1, l2)
}
