import { zip, partition, pickIndices } from "./util/array.ts"
import type { Column, Syllable, Strata, StressMark } from "./types.ts"
import { parseInterpretive, parseProduction, underlyingForm } from "./word.ts"
import { markToERC } from "./ot.ts"
import assert from "node:assert"
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
// TODO: this whole thing should use strata (Array<Set<Constraint>>) instead of just Constraint[]
export function ripcd(overt: Syllable[], hierarchy: StressMark[]): StressMark[] {
  for (let rounds = 0; rounds < 10; rounds++) {
    let interp = parseInterpretive(overt, hierarchy)
    let uf = underlyingForm(interp)
    let prod = parseProduction(uf, hierarchy)
    if (interp.equal(prod)) {
      return hierarchy
    }
    let row = markToERC(
      hierarchy.map(h => h.evaluate(prod)),
      hierarchy.map(h => h.evaluate(interp))
    )
    let firstWinner = row.indexOf("w")
    let demotees = []
    let neutrals = []
    assert(firstWinner >= 0)
    for (let i = 0; i < firstWinner; i++) {
      if (row[i] === "l") demotees.push(hierarchy[i])
      else neutrals.push(hierarchy[i])
    }
    hierarchy = [...neutrals, hierarchy[firstWinner], ...demotees, ...hierarchy.slice(firstWinner + 1)]
  }
  throw new Error("RIP/CD did not converge in 10 rounds.")
}
