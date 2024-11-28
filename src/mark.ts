import * as unifeat from "./unifeat.ts"
import { Mark, ProsodicWord, isFoot, isSyllable } from "./types.ts"
import type { Phoneme, StressMark, Syllable, Foot } from "./types.ts"
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
/**
 * NOTE: Empty strings return a sentinel head (no stress at all).
 * NOTE: I'm pretty sure stress parsing is actually ambiguous, perhaps only two-way: between trochaic and iambic.
 * Since I'm working with a trochaic language for now, I'm just going to write a deterministic trochaic parser.
 * A good example ambiguous input is .'.., which could parse as (.'.). or .('..). This parser always produces the latter.
 */
export function parseTrochaic(overt: Syllable[]): ProsodicWord {
  let sentinelHead: Foot = { s1: { weight: "l", stress: undefined }, s2: undefined }
  if (overt.length === 0) {
    return ProsodicWord(sentinelHead, [])
  }
  let feet: (Foot | Syllable)[] = []
  let prev: Syllable | undefined
  function push(s: Syllable | Foot, next: Syllable | undefined) {
    feet.push(s)
    prev = next
  }
  for (const s of overt) {
    if (!prev) {
      // x -> prev = x
      prev = s
    } else if (prev.stress === "unstressed") {
      // ll  -> push l, prev =  l
      // hl  -> push h, prev =  l
      // l'l -> push l, prev = 'l
      // h'l -> push h, prev = 'l
      // lh  -> push l, prev =  l
      // hh  -> push h, prev =  h
      // l'h -> push l, prev = 'h
      // h'h -> push h, prev = 'h
      push(prev, s)
    } else if (s.stress === "unstressed" && !(prev.weight === "h" && s.weight === "h")) {
      // 'll -> push ('ll), prev = undefined
      // 'hl -> push ('hl), prev = undefined
      // 'lh -> push ('lh), prev = undefined
      push({ s1: prev, s2: s }, undefined)
    } else {
      // 'hh  -> push ('h), prev =  h

      // 'l'l -> push ('l), prev = 'l
      // 'h'l -> push ('h), prev = 'l
      // 'l'h -> push ('l), prev = 'h
      // 'h'h -> push ('h), prev = 'h
      push({ s1: prev }, s)
    }
  }
  if (prev) {
    feet.push(prev.stress === "unstressed" ? prev : { s1: prev })
  }
  return ProsodicWord(feet?.find(isFoot) ?? sentinelHead, feet)
}
export let footBin: StressMark = {
  kind: "mark",
  name: "FootBin",
  evaluate(overt) {
    return count(overt.feet, sf => isFoot(sf) && sf.s2 === undefined && sf.s1.weight === "l")
  },
}
export let wsp: StressMark = {
  kind: "mark",
  name: "WSP",
  evaluate(overt) {
    return count(overt.syllables(), s => s.weight === "h" && s.stress === "unstressed")
  },
}
export let parse: StressMark = {
  kind: "mark",
  name: "Parse",
  evaluate(overt) {
    return count(overt.feet, isSyllable)
  },
}
export let allFeetLeft: StressMark = {
  kind: "mark",
  name: "AllFeetLeft",
  evaluate(overt) {
    return alignFeetToWord("l", overt, isFoot)
  },
}
export let allFeetRight: StressMark = {
  kind: "mark",
  name: "AllFeetRight",
  evaluate(overt) {
    return alignFeetToWord("r", overt, isFoot)
  },
}
export let mainLeft: StressMark = {
  kind: "mark",
  name: "MainLeft",
  evaluate(overt) {
    return alignFeetToWord("l", overt, isHeadFoot)
  },
}
export let mainRight: StressMark = {
  kind: "mark",
  name: "MainRight",
  evaluate(overt) {
    return alignFeetToWord("r", overt, isHeadFoot)
  },
}
export let wordFootLeft: StressMark = {
  kind: "mark",
  name: "WordFootLeft",
  evaluate(overt) {
    return overt.feet.length === 0 || isFoot(overt.feet[0]) ? 0 : 1
  },
}
export let wordFootRight: StressMark = {
  kind: "mark",
  name: "WordFootRight",
  evaluate(overt) {
    return overt.feet.length === 0 || isFoot(overt.feet.at(-1)!) ? 0 : 1
  },
}
export let iambic: StressMark = {
  kind: "mark",
  name: "Iambic",
  evaluate(overt) {
    return count(overt.feet, sf => isFoot(sf) && sf.s1.stress !== "unstressed" && !!sf.s2)
  },
}
export let footNonFinal: StressMark = {
  kind: "mark",
  name: "FootNonFinal",
  evaluate(overt) {
    return count(overt.feet, sf => isFoot(sf) && (sf.s1.stress === "unstressed" || !sf.s2))
  },
}
export let nonFinal: StressMark = {
  kind: "mark",
  name: "NonFinal",
  evaluate(overt) {
    return overt.feet.length > 0 && isFoot(overt.feet.at(-1)!) ? 1 : 0
  },
}
function isHeadFoot(sf: Syllable | Foot): sf is Foot {
  return isFoot(sf) && (sf.s1.stress === "primary" || sf.s2?.stress === "primary")
}
function alignFeetToWord(
  direction: "l" | "r",
  word: ProsodicWord,
  predicate: (sf: Syllable | Foot) => boolean
): number {
  let i = 0
  let len = word.length()
  let totalMisalignment = 0
  for (let foot of word.feet) {
    if (direction === "l") {
      if (predicate(foot)) {
        totalMisalignment += i
      }
      i += footSize(foot)
    } else {
      i += footSize(foot)
      if (predicate(foot)) {
        totalMisalignment += len - i
      }
    }
  }
  return totalMisalignment
}
function footSize(sf: Syllable | Foot) {
  return isFoot(sf) && sf.s2 ? 2 : 1
}
