import * as unifeat from "./unifeat.ts"
import { Mark } from "./types.ts"
import type { Phoneme } from "./types.ts"
import { zipWith, count, sequence } from "./util/array.ts"

unifeat.phonemes
export let onset = Mark("onset", (output: string) => {
  return count(syllabify(unifeat.phonesToFeatures(output)), syll => !syll[0]["cons"])
})
export function onsetRepair(output: string): string[] {
  function recreateSyllables(syllables: Phoneme[][]): string[] {
    let i = 0
    let out = []
    for (let s of syllables) {
      out.push(output.slice(i, i + s.length))
      i += s.length
    }
    return out
  }
  let ident = (syllable: string) => syllable
  let del = (_: string) => ""
  let epenthesise = (syllable: string) => "t" + syllable
  let syllables = syllabify(unifeat.phonesToFeatures(output))
  let opss: ((s: string) => string)[][] = sequence(
    syllables.map(syll => (syll[0]["cons"] ? [ident] : [ident, del, epenthesise]))
  )
  // TODO: Hacky that the inner algorithm is in syllables but the outer is in strings. It was just easier to test, I bet.
  let syllables2 = recreateSyllables(syllables)
  return opss.map(ops =>
    zipWith(ops, syllables2, (op, syll) => op(syll))
      .flat()
      .join("")
  )
}
/**
 * It's a parser!
 * 
 * Here is the ancient comment explaining its states:
    state C  -> emit C; go {C(.) V}
    state V  -> emit V; go {V(.) CC CV(.) C$}
    state CC -> emit C.C; go {C(.) V}
    state CV -> emit CV; go {V(.) CC CV(.) C$}
    state C$ -> emit C; go {}
 */
type SyllableState = "C" | "V" | "CC" | "CV" | "C$"
export function syllabify(phs: Phoneme[]): Phoneme[][] {
  let prev: Phoneme = {}
  let it = phs[Symbol.iterator]()
  let result = it.next()
  if (result.done) {
    return []
  }
  let ph: Phoneme = result.value
  let acc: Phoneme[] = []
  let syllables: Phoneme[][] = []
  let state = (ph["cons"] ? "C" : "V") as SyllableState
  while (!result.done) {
    switch (state) {
      case "C":
        acc.push(ph)
        advanceCons()
        break
      case "V":
        acc.push(ph)
        advanceVowel()
        break
      case "CC":
        acc.push(prev)
        makeSyllable()
        acc.push(ph)
        advanceCons()
        break
      case "CV":
        acc.push(prev, ph)
        advanceVowel()
        break
    }
  }
  if (acc.length) syllables.push(acc)
  return syllables

  function makeSyllable(): void {
    syllables.push(acc)
    acc = []
  }
  function advanceCons(): void {
    result = it.next()
    if (result.done) {
      // TODO: return from the whole function and break the loop
    } else ph = result.value
    if (ph["cons"]) {
      makeSyllable()
      state = "C"
    } else {
      state = "V"
    }
  }
  function advanceVowel(): void {
    result = it.next()
    if (result.done) {
      // TODO: return from the whole function and break the loop
    } else ph = result.value
    if (ph["cons"]) {
      prev = ph
      result = it.next()
      if (result.done) {
        acc.push(prev)
        // TODO: return from the whole function and break the loop
      } else ph = result.value
      if (ph["cons"]) {
        state = "CC"
      } else {
        makeSyllable()
        state = "CV"
      }
    } else {
      prev = {}
      makeSyllable()
      state = "V"
    }
  }
}
