import { suite, test } from "node:test"
import assert, { deepEqual as equal, fail } from "node:assert"
import type { Stress, Syllable, Foot, Weight, Segment } from "../types.ts"
import { Word } from "../word.ts"
export function testall(suiteName: string, testo: Record<string, () => void>) {
  suite(suiteName, () => {
    for (let [name, f] of Object.entries(testo)) {
      test(name, f)
    }
  })
}

export function qw(s: string): string[] {
  return s.split(/\s+/)
}

export function meterUnparsed(stress: string): Syllable[] {
  assert(stress.indexOf("(") === -1 && stress.indexOf(")") === -1, "stressOvert only works on unparsed stress patterns")
  return meterPattern(stress).syllables()
}
/** ('..)
 * . light
 * _ heavy
 * ' primary stress
 * , secondary stress
 * ( start of foot
 * ) end of foot
 */
export function meterPattern(stress: string): Word {
  let nextStress: Stress = ""
  let foot: Syllable[] | undefined
  let contents: (Syllable | Foot | Segment)[] = []
  let onset: Segment | undefined
  let nucleus: Segment | undefined
  let coda: Segment | undefined
  for (let i = 0; i < stress.length; i++) {
    let input: Segment | undefined = undefined
    switch (stress[i]) {
      case "c":
        input = { segment: "c" }
      // falls through
      case "t":
        if ((nucleus || onset) && !coda) {
          coda = { segment: "c", input }
          break
        }
        if ((nucleus || onset) && coda) {
          pushSegments()
        }
        onset = { segment: "c", input }
        break
      case "v":
        input = { segment: "v" }
      // falls through
      case "a":
        if (nucleus) {
          pushSegments()
        }
        nucleus = { segment: "v", input }
        break
      case "'":
        nextStress = "'"
        break
      case "`":
        nextStress = "`"
        break
      case ".":
      case "_":
        ;(foot ? foot : contents).push({
          stress: nextStress,
          weight: stress[i] as Weight,
          onset,
          nucleus,
          coda,
        })
        onset = nucleus = coda = undefined
        nextStress = ""
        break
      case "(":
        assert(!foot, "open parenthesis inside unclosed open parenthesis")
        foot = []
        break
      case ")":
        assert(foot, "close parenthesis without open parenthesis")
        if (foot.length === 1) {
          contents.push({ s1: foot[0] })
        } else if (foot.length === 2) {
          contents.push({ s1: foot[0], s2: foot[1] })
        } else {
          fail("foot too long" + foot.length)
        }
        foot = undefined
        break
    }
  }
  pushSegments()
  assert(!nextStress, "trailing stress mark")
  return new Word(contents)

  function pushSegments() {
    if (onset) contents.push(onset)
    if (nucleus) contents.push(nucleus)
    if (coda) contents.push(coda)
    onset = nucleus = coda = undefined
  }
}
