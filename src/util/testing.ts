import { suite, test } from "node:test"
import assert, { deepEqual as equal, fail } from "node:assert"
import type { Stress, Syllable, Foot, Weight } from "../types.ts"
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
  return meterPattern(stress) as Syllable[]
}
/** ('..)
 * . light
 * _ heavy
 * ' primary stress
 * , secondary stress
 * ( start of foot
 * ) end of foot
 */
export function meterPattern(stress: string): (Syllable | Foot)[] {
  let nextStress: Stress = ""
  let foot: Syllable[] | undefined
  let syllables: (Syllable | Foot)[] = []
  for (let i = 0; i < stress.length; i++) {
    switch (stress[i]) {
      case "'":
        nextStress = "'"
        break
      case "`":
        nextStress = "`"
        break
      case ".":
      case "_":
        ;(foot ? foot : syllables).push({ stress: nextStress, weight: stress[i] as Weight })
        nextStress = ""
        break
      case "(":
        assert(!foot, "open parenthesis inside unclosed open parenthesis")
        foot = []
        break
      case ")":
        assert(foot, "close parenthesis without open parenthesis")
        if (foot.length === 1) {
          syllables.push({ s1: foot[0] })
        } else if (foot.length === 2) {
          syllables.push({ s1: foot[0], s2: foot[1] })
        } else {
          fail("foot too long" + foot.length)
        }
        foot = undefined
        break
    }
  }
  assert(!nextStress, "trailing stress mark")
  return syllables
}
