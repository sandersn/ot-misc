import { Word, isFoot, isSyllable } from "./word.ts"
import type { StressMark, Syllable, Foot } from "./types.ts"
import { count } from "./util/array.ts"
export let footBin: StressMark = {
  kind: "mark",
  name: "FootBin",
  evaluate(overt) {
    return count(overt.feet, sf => isFoot(sf) && sf.s2 === undefined && sf.s1.weight === ".")
  },
}
export let wsp: StressMark = {
  kind: "mark",
  name: "WSP",
  evaluate(overt) {
    return count(overt.syllables(), s => s.weight === "_" && !s.stress)
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
    return count(overt.feet, sf => isFoot(sf) && !!sf.s1.stress && !!sf.s2)
  },
}
export let footNonFinal: StressMark = {
  kind: "mark",
  name: "FootNonFinal",
  evaluate(overt) {
    return count(overt.feet, sf => isFoot(sf) && (!sf.s1.stress || !sf.s2))
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
  return isFoot(sf) && (sf.s1.stress === "'" || sf.s2?.stress === "'")
}
function alignFeetToWord(direction: "l" | "r", word: Word, predicate: (sf: Syllable | Foot) => boolean): number {
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
