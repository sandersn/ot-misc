import { Word, isFoot, isSegment, isSyllable } from "./word.ts"
import type { Constraint, Syllable, Foot, Segment } from "./types.ts"
import { count } from "./util/array.ts"
export let footBin: Constraint = {
  name: "FootBin",
  evaluate(overt) {
    return count(overt.contents, sf => isFoot(sf) && sf.s2 === undefined && sf.s1.weight === ".")
  },
}
export let noCoda: Constraint = {
  name: "NoCoda",
  evaluate(overt) {
    return count(overt.syllables(), s => !!s.coda)
  },
}
export let onset: Constraint = {
  name: "Onset",
  evaluate(overt) {
    return count(overt.syllables(), s => !s.onset)
  },
}
export let fillOnset: Constraint = {
  name: "FillOnset",
  evaluate(overt) {
    return count(overt.syllables(), s => (s.onset ? !s.onset.input : false))
  },
}
export let fillNucleus: Constraint = {
  name: "FillNucleus",
  evaluate(overt) {
    return count(overt.syllables(), s => (s.nucleus ? !s.nucleus.input : false))
  },
}
// TODO: Should be unified with stress version of parse.
// this means that all segmental examples need to be correctly footed, which I'll do later
export let parseSyllable: Constraint = {
  name: "Parse",
  evaluate(overt) {
    return count(overt.contents, isSegment)
  },
}
export let wsp: Constraint = {
  name: "WSP",
  evaluate(overt) {
    return count(overt.syllables(), s => s.weight === "_" && !s.stress)
  },
}
export let parseFoot: Constraint = {
  name: "Parse",
  evaluate(overt) {
    return count(overt.contents, x => isSyllable(x) || isSegment(x))
  },
}
export let allFeetLeft: Constraint = {
  name: "AllFeetLeft",
  evaluate(overt) {
    return alignFeetToWord("l", overt, isFoot)
  },
}
export let allFeetRight: Constraint = {
  name: "AllFeetRight",
  evaluate(overt) {
    return alignFeetToWord("r", overt, isFoot)
  },
}
export let mainLeft: Constraint = {
  name: "MainLeft",
  evaluate(overt) {
    return alignFeetToWord("l", overt, isHeadFoot)
  },
}
export let mainRight: Constraint = {
  name: "MainRight",
  evaluate(overt) {
    return alignFeetToWord("r", overt, isHeadFoot)
  },
}
export let wordFootLeft: Constraint = {
  name: "WordFootLeft",
  evaluate(overt) {
    return overt.contents.length === 0 || isFoot(overt.contents[0]) ? 0 : 1
  },
}
export let wordFootRight: Constraint = {
  name: "WordFootRight",
  evaluate(overt) {
    return overt.contents.length === 0 || isFoot(overt.contents.at(-1)!) ? 0 : 1
  },
}
export let iambic: Constraint = {
  name: "Iambic",
  evaluate(overt) {
    return count(overt.contents, sf => isFoot(sf) && !!sf.s1.stress && !!sf.s2)
  },
}
export let footNonFinal: Constraint = {
  name: "FootNonFinal",
  evaluate(overt) {
    return count(overt.contents, sf => isFoot(sf) && (!sf.s1.stress || !sf.s2))
  },
}
export let nonFinal: Constraint = {
  name: "NonFinal",
  evaluate(overt) {
    return overt.contents.length > 0 && isFoot(overt.contents.at(-1)!) ? 1 : 0
  },
}
function isHeadFoot(sf: Syllable | Foot | Segment): sf is Foot {
  return isFoot(sf) && (sf.s1.stress === "'" || sf.s2?.stress === "'")
}
function alignFeetToWord(
  direction: "l" | "r",
  word: Word,
  predicate: (sf: Syllable | Foot | Segment) => boolean,
): number {
  let i = 0
  let len = word.length()
  let totalMisalignment = 0
  for (let foot of word.contents) {
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
function footSize(sf: Syllable | Foot | Segment) {
  return isFoot(sf) && sf.s2 ? 2 : 1
}
