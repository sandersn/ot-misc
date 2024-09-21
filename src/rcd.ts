import { partition, transpose, zip, pickIndices } from "./util/array"
import { Column, Strata } from './types'
/**
 * A row is a loser when 
 */
function removeLosersFromDemote(demote: Column[], promote: Column[]): Column[] {
    let ties = []
    for (let i = 0; i < promote[0].violations.length; i++) {
        let tied = true
        for (const p of promote) {
            if (p.violations[i] !== 'e') {
                tied = false
                break
            }
        }
        if (tied) {
            ties.push(i)
        }
    }
    return demote.map(c => ({ ...c, violations: pickIndices(c.violations, ties) }))
}
export function rcd(columns: Column[]): Strata {
    let acc: Strata  = []
    while (true) {
        let [demote, promote] = partition(columns, c => c.violations.some(v => v === 'l'))
        if (demote.length == 0 || promote.length == 0) {
            acc.push(columns.map(c => c.constraint))
            return acc
        } else {
            acc.push(promote.map(c => c.constraint))
            columns = removeLosersFromDemote(demote, promote)
        }
    }
}
