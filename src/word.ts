import type { Constraint, Foot, Syllable, Segment, Stress } from "./types.ts"
/**
 * Additional rules not enforced by this type:
 * - Unfooted syllables must be unstressed.
 * - Each foot has exactly one head syllable, which is the only stressed one in that foot.
 * - Head foot's head syllable must have primary stress; other feet's head syllables must have secondary.
 * - All words must have a head.
 */
export class Word {
  head: Foot | undefined
  contents: (Foot | Syllable | Segment)[]
  constructor(contents: (Foot | Syllable | Segment)[]) {
    this.contents = contents
    this.head = findHead(this.feet())
  }
  // TODO: feet/syllables should probably be cached
  feet() {
    let ft = []
    for (const x of this.contents) {
      if (isFoot(x)) {
        ft.push(x)
      }
    }
    return ft
  }
  syllables() {
    let ss = []
    for (const x of this.contents) {
      if (isSyllable(x)) {
        ss.push(x)
      } else if (isFoot(x)) {
        ss.push(x.s1)
        if (x.s2) {
          ss.push(x.s2)
        }
      }
    }
    return ss
  }
  // TODO: This is really syllableLength (and if syllables is cached, might as well
  // rely on that instead)
  length() {
    let len = 0
    for (const x of this.contents) {
      if (isSegment(x)) {
      } else if (isSyllable(x)) {
        len++
      } else {
        len += x.s2 ? 2 : 1
      }
    }
    return len
  }
  toString() {
    return formatWord(this)
  }
  equal(other: Word): boolean {
    return (
      (this.head === other.head || equalFoot(this.head!, other.head!)) &&
      this.contents.length === other.contents.length &&
      this.contents.every((f, i) => equalFoot(f, other.contents[i]))
    )
  }
}
function equalFoot(f1: Foot | Syllable | Segment, f2: Foot | Syllable | Segment): boolean {
  if (isFoot(f1) && isFoot(f2)) {
    return equalSyllable(f1.s1, f2.s1) && (f1.s2 && f2.s2 ? equalSyllable(f1.s2!, f2.s2!) : !!f1.s2 === !!f2.s2)
  } else if (isSyllable(f1) && isSyllable(f2)) {
    return equalSyllable(f1, f2)
  } else if (isSegment(f1) && isSegment(f2)) {
    return equalSegment(f1, f2)
  }
  return false
}
function equalSyllable(s1: Syllable, s2: Syllable): boolean {
  return s1.stress === s2.stress && s1.weight === s2.weight
}
function equalSegment(s1: Segment, s2: Segment): boolean {
  return s1.segment === s2.segment && s1.input?.segment === s2.input?.segment
}
function findHead(feet: Array<Foot | Syllable>): Foot | undefined {
  return feet.find(f => isFoot(f) && (f.s1.stress === "'" || f.s2?.stress === "'")) as Foot
}
function append(word: Word, foot: Foot | Syllable): Word {
  return new Word([...word.contents, foot])
}
function empty(): Word {
  return new Word([])
}
function formatWord(pw: Word): string {
  return pw.contents
    .map(s =>
      isFoot(s)
        ? "(" + formatSyllable(s.s1) + (s.s2 ? formatSyllable(s.s2) : "") + ")"
        : isSegment(s)
          ? formatSegment(s)
          : formatSyllable(s),
    )
    .join("")
}
function formatSegment(s: Segment | undefined): string {
  if (!s) return ""
  if (s.segment === "c" && !s.input) return "t"
  if (s.segment === "v" && !s.input) return "a"
  return s.segment
}
function formatSyllable(s: Syllable): string {
  let segments = formatSegment(s.onset) + formatSegment(s.nucleus) + formatSegment(s.coda)
  return s.stress + segments + s.weight
}

export function isFoot(s: Foot | Syllable | Segment): s is Foot {
  return "s1" in s
}
export function isSyllable(s: Foot | Syllable | Segment): s is Syllable {
  return "weight" in s
}
export function isSegment(s: Foot | Syllable | Segment): s is Segment {
  return "segment" in s
}

/**
 * TODO: This should be in its own module eventually.
 * TODO: Look up the standard OT name for this
 */
function evaluate(candidates: Word[], hierarchy: Constraint[]): Word | undefined {
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
export function parseProductionSegment(syllables: Syllable[], hierarchy: Constraint[]): Word {
  let best = [empty()]
  let change = true
  while (!change) {
    best = [
      // O
      // N
      // D
    ]
  }
  for (let s of syllables.slice(1)) {
  }
  return empty()
}
/**
 * NOTE: maybe hierarchy should be Array<Set<Constraint>> eventually
 */
export function parseProduction(syllables: Syllable[], hierarchy: Constraint[]): Word {
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
export function parseInterpretive(syllables: Syllable[], hierarchy: Constraint[]): Word {
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
    if (word.contents.length === 0) {
      return undefined
    }
    let last = word.contents.at(-1)
    if (!(last && isFoot(last) && !last.s2)) {
      return undefined
    }
    let targetStress: Stress = last.s1.stress ? "" : word.head ? "`" : stress
    if (syllable.stress !== targetStress) {
      return undefined
    }
    let feet = word.contents.slice(0, -1)
    feet.push({ ...last, s2: syllable })
    return new Word(feet)
  }
}
function appendToLastFoot(syllable: Syllable, stress: "'" | "`"): (word: Word) => Word | undefined {
  return word => {
    if (word.contents.length === 0) {
      return undefined
    }
    let last = word.contents.at(-1)
    if (!(last && isFoot(last) && !last.s2)) {
      return undefined
    }
    stress = word.head ? "`" : stress
    let feet = word.contents.slice(0, -1)
    feet.push({ ...last, s2: !last.s1.stress ? { ...syllable, stress } : syllable })
    return new Word(feet)
  }
}
// NOTE: Annoyingly, a segmental underlying form doesn't have syllables.
// It requires parsing to produce them. However, the metrical constraints I have
// rely on syllables in the underlying form.
// Pretty sure this divide is baked into phonology, and part of why the two analysis are always so separated.
// So: constraint demotion on meter is going to need a different function to produce underlying form than
//     when running on segments.
export function underlyingMeter(w: Word): Syllable[] {
  let syllables: Syllable[] = []
  for (let x of w.contents) {
    if (isSegment(x)) {
    } else if (isSyllable(x)) {
      push(x)
    } else {
      push(x.s1)
      if (x.s2) {
        push(x.s2)
      }
    }
  }
  return syllables

  function push(s: Syllable) {
    syllables.push({ ...s, stress: "" })
  }
}
export function underlyingSegments(w: Word): Segment[] {
  let segments: Segment[] = []
  for (let x of w.contents) {
    if (isSegment(x)) {
      if (x.input) segments.push(x)
    } else if (isSyllable(x)) {
      push(x)
    } else {
      push(x.s1)
      if (x.s2) {
        push(x.s2)
      }
    }
  }
  return segments

  function push(s: Syllable) {
    if (s.onset && s.onset.input) segments.push(s.onset)
    if (s.nucleus && s.nucleus.input) segments.push(s.nucleus)
    if (s.coda && s.coda.input) segments.push(s.coda)
  }
}
/**
 * NOTE: Empty strings return an undefined head.
 * NOTE: This isn't generally correct, but it fits the Garawa example, so I'm using it for testing constraints
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
