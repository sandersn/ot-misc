import type { StressMark, Foot, Syllable, Stress } from "./types.ts"
/**
 * Additional rules not enforced by this type:
 * - Unfooted syllables must be unstressed.
 * - Each foot has exactly one head syllable, which is the only stressed one in that foot.
 * - Head foot's head syllable must have primary stress; other feet's head syllables must have secondary.
 * - All words must have a head.
 */
export class Word {
  head: Foot | undefined
  feet: (Foot | Syllable)[]
  constructor(feet: (Foot | Syllable)[]) {
    this.feet = feet
    this.head = findHead(feet)
  }
  syllables() {
    let ss = []
    for (const foot of this.feet) {
      if (isSyllable(foot)) {
        ss.push(foot)
      } else {
        ss.push(foot.s1)
        if (foot.s2) {
          ss.push(foot.s2)
        }
      }
    }
    return ss
  }
  length() {
    let len = 0
    for (const foot of this.feet) {
      if (isSyllable(foot)) {
        len++
      } else {
        len += foot.s2 ? 2 : 1
      }
    }
    return len
  }
  toString() {
    return formatWord(this)
  }
  equal(other: Word): boolean {
    return (
      this.head === other.head &&
      this.feet.length === other.feet.length &&
      this.feet.every((f, i) => equalFoot(f, other.feet[i]))
    )
  }
}
function equalFoot(f1: Foot | Syllable, f2: Foot | Syllable): boolean {
  if (isFoot(f1) && isFoot(f2)) {
    return equalSyllable(f1.s1, f2.s1) && (f1.s2 && f2.s2 ? equalSyllable(f1.s2!, f2.s2!) : !!f1.s2 === !!f2.s2)
  } else if (isSyllable(f1) && isSyllable(f2)) {
    return equalSyllable(f1, f2)
  }
  return false
}
function equalSyllable(s1: Syllable, s2: Syllable): boolean {
  return s1.stress === s2.stress && s1.weight === s2.weight
}
function findHead(feet: Array<Foot | Syllable>): Foot | undefined {
  return feet.find(f => isFoot(f) && (f.s1.stress === "'" || f.s2?.stress === "'")) as Foot
}
function append(word: Word, foot: Foot | Syllable): Word {
  return new Word([...word.feet, foot])
}
function empty(): Word {
  return new Word([])
}
function formatWord(pw: Word): string {
  return pw.feet
    .map(s => (isFoot(s) ? "(" + formatSyllable(s.s1) + (s.s2 ? formatSyllable(s.s2) : "") + ")" : formatSyllable(s)))
    .join("")
}
function formatSyllable(s: Syllable): string {
  return s.stress + s.weight
}

export function isFoot(s: Foot | Syllable): s is Foot {
  return "s1" in s
}
export function isSyllable(s: Foot | Syllable): s is Syllable {
  return "weight" in s
}

/**
 * TODO: This should be in its own module eventually.
 * TODO: Look up the standard OT name for this
 */
function evaluate(candidates: Word[], hierarchy: StressMark[]): Word | undefined {
  if (candidates.length === 0) {
    return undefined
  }
  if (candidates.length === 1) {
    return candidates[0]
  }
  for (let constraint of hierarchy) {
    let bounds = candidates.map(c => constraint.evaluate(c))
    let best = Math.min(...bounds)
    let next = candidates.filter((_, i) => bounds[i] === best)
    if (next.length === 0) break
    else candidates = next
  }
  return candidates[0]
}
/**
 * NOTE: maybe hierarchy should be Array<Set<Constraint>> eventually
 */
export function parseProduction(syllables: Syllable[], hierarchy: StressMark[]): Word {
  let best = [empty()]
  for (let s of syllables) {
    best = [
      // NoM is "for descriptions that lack a main stress", whereas M is for ones that have it.
      // That means that
      // (1) M needs to filter its output by having a main stress
      // (2) No M needs to filter its output by not having a main stress
      // (3) M F1 S and M F2 need to filter input for not having a main stress (if F2 would add a stress)
      best.map(pw => append(pw, s)).filter(w => !w.head), // NoM NoF
      best.map(pw => append(pw, { s1: s })).filter(w => !w.head), // NoM F1 NoS
      best.map(pw => append(pw, { s1: { ...s, stress: "`" } })).filter(w => !w.head), // NoM F1 S
      best.map(appendToLastFoot(s, "`")).filter(w => w && !w.head) as Word[], // NoM F2
      best.map(pw => append(pw, s)).filter(w => w.head), // M NoF
      best.map(pw => append(pw, { s1: s })).filter(w => w.head), // M F1 NoS
      best.map(pw => append(pw, { s1: { ...s, stress: pw.head ? "`" : "'" } })).filter(w => w.head), // M F1 S
      best.map(appendToLastFoot(s, "'")).filter(w => w && w.head) as Word[], // M F2
    ]
      .map(cands => evaluate(cands, hierarchy))
      .filter(w => !!w)
    // console.log(prev.map(formatWord))
  }
  return (
    evaluate(
      best.filter(w => w.head),
      hierarchy,
    ) ?? empty()
  )
}
export function parseInterpretive(syllables: Syllable[], hierarchy: StressMark[]): Word {
  let best = [empty()]
  for (let s of syllables) {
    best = [
      // NoM is "for descriptions that lack a main stress", whereas M is for ones that have it.
      // That means that
      // (1) M needs to filter its output by having a main stress
      // (2) No M needs to filter its output by not having a main stress
      // (3) M F1 S and M F2 need to filter input for not having a main stress (if F2 would add a stress)
      s.stress ? [] : best.map(pw => append(pw, s)).filter(w => !w.head), // NoM NoF
      s.stress ? [] : best.map(pw => append(pw, { s1: s })).filter(w => !w.head), // NoM F1 NoS
      s.stress === "`" ? best.map(pw => append(pw, { s1: s })).filter(w => !w.head) : [], // NoM F1 S
      s.stress === "`" ? (best.map(appendToLastFoot(s, "`")).filter(w => w && !w.head) as Word[]) : [], // NoM F2
      s.stress ? [] : best.map(pw => append(pw, s)).filter(w => w.head), // M NoF
      s.stress ? [] : best.map(pw => append(pw, { s1: s })).filter(w => w.head), // M F1 NoS
      best
        .map(pw => {
          let stress: Stress = pw.head ? "`" : "'"
          return s.stress === stress ? append(pw, { s1: s }) : undefined
        })
        .filter(w => w && w.head) as Word[], // M F1 S
      best.map(appendToLastFootMatch(s, "'")).filter(w => w && w.head) as Word[], // M F2
    ]
      .map(cands => evaluate(cands, hierarchy))
      .filter(w => !!w)
    // console.log(prev.map(formatWord))
  }
  return (
    evaluate(
      best.filter(w => w.head),
      hierarchy,
    ) ?? empty()
  )
}
function appendToLastFootMatch(syllable: Syllable, stress: "'" | "`"): (word: Word) => Word | undefined {
  return word => {
    if (word.feet.length === 0) {
      return undefined
    }
    let last = word.feet.at(-1)
    if (!(last && isFoot(last) && !last.s2)) {
      return undefined
    }
    let targetStress: Stress = last.s1.stress ? "" : word.head ? "`" : stress
    if (syllable.stress !== targetStress) {
      return undefined
    }
    let feet = word.feet.slice(0, -1)
    feet.push({ ...last, s2: syllable })
    return new Word(feet)
  }
}
function appendToLastFoot(syllable: Syllable, stress: "'" | "`"): (word: Word) => Word | undefined {
  return word => {
    if (word.feet.length === 0) {
      return undefined
    }
    let last = word.feet.at(-1)
    if (!(last && isFoot(last) && !last.s2)) {
      return undefined
    }
    stress = word.head ? "`" : stress
    let feet = word.feet.slice(0, -1)
    feet.push({ ...last, s2: !last.s1.stress ? { ...syllable, stress } : syllable })
    return new Word(feet)
  }
}
/**
 * This form only works on stress since that's what I have working. It's close to trivial.
 */
export function underlyingForm(w: Word): Syllable[] {
  // TODO: Also need to strip stress too
  let syllables: Syllable[] = []
  for (let foot of w.feet) {
    if (isSyllable(foot)) {
      push(foot)
    } else {
      push(foot.s1)
      if (foot.s2) {
        push(foot.s2)
      }
    }
  }
  return syllables

  function push(s: Syllable) {
    syllables.push({ ...s, stress: "" })
  }
}
/**
 * NOTE: Empty strings return an undefined head.
 * NOTE: This isn't generally correct, but it fits the Garawa example
 */
export function parseTrochaic(overt: Syllable[]): Word {
  if (overt.length === 0) {
    return new Word([])
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
    } else if (!prev.stress) {
      // ll  -> push l, prev =  l
      // hl  -> push h, prev =  l
      // l'l -> push l, prev = 'l
      // h'l -> push h, prev = 'l
      // lh  -> push l, prev =  l
      // hh  -> push h, prev =  h
      // l'h -> push l, prev = 'h
      // h'h -> push h, prev = 'h
      push(prev, s)
    } else if (!s.stress && !(prev.weight === "_" && s.weight === "_")) {
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
    feet.push(prev.stress ? { s1: prev } : prev)
  }
  return new Word(feet)
}
