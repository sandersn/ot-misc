import { partition, pickIndices } from "./util/array.ts"
import { Column, type Strata } from "./types.ts"
/**
 * A candidate is a loser when its promoted columns have a winning mark in them.
 * If the promoted columns are all tied, then the candidate is not a loser, and
 * the demoted columns are still interesting, so keep them.
 */
function removeLosersFromDemote(demote: Column[], promote: Column[]): Column[] {
  let ties = []
  for (let i = 0; i < promote[0].violations.length; i++) {
    let tied = true
    for (const p of promote) {
      if (p.violations[i] !== "=") {
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
  let acc: Strata = []
  while (true) {
    let [demote, promote] = partition(columns, c => c.violations.some(v => v === "l"))
    if (demote.length == 0 || promote.length == 0) {
      acc.push(columns.map(c => c.constraint))
      return acc
    } else {
      acc.push(promote.map(c => c.constraint))
      columns = removeLosersFromDemote(demote, promote)
    }
  }
}
