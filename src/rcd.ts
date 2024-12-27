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
// TODO: this whole things should use strata (Array<Set<Constraint>>) instead of just Constraint[]
export function ripcd(overt: Syllable[], hierarchy: StressMark[]): StressMark[] {
  while (true) {
    let interp = parseInterpretive(overt, hierarchy)
    let uf = underlyingForm(interp)
    let prod = parseProduction(uf, hierarchy)
    if (interp.equal(prod)) {
      return hierarchy
    }
    let row = markToERC(
      hierarchy.map(h => h.evaluate(prod)),
      hierarchy.map(h => h.evaluate(interp)),
    )
    let i = row.indexOf("w")
    assert(i >= 0)
    let [losers, ok] = partition(zip(hierarchy.slice(0, i), row.slice(0, i)), ([h, erc]) => erc === "l")
    hierarchy = [...ok.map(([h, _]) => h), hierarchy[i], ...losers.map(([h, _]) => h), ...hierarchy.slice(i + 1)]
  }
}
