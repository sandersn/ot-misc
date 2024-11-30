import type { StressMark, Foot, Syllable, Word } from "./types.ts"
export function empty(): Word {
  return { head: undefined, feet: [] }
}
export function isFoot(s: Foot | Syllable): s is Foot {
  return "s1" in s
}
export function isSyllable(s: Foot | Syllable): s is Syllable {
  return "weight" in s
}
export function syllables(word: Word) {
  let ss = []
  for (const foot of word.feet) {
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
export function length(word: Word) {
  let len = 0
  for (const foot of word.feet) {
    if (isSyllable(foot)) {
      len++
    } else {
      len += foot.s2 ? 2 : 1
    }
  }
  return len
}
export function formatWord(pw: Word): string {
  return pw.feet
    .map(s => (isFoot(s) ? "(" + formatSyllable(s.s1) + (s.s2 ? formatSyllable(s.s2) : "") + ")" : formatSyllable(s)))
    .join("")
}
function formatSyllable(s: Syllable): string {
  return (s.stress === "primary" ? "'" : s.stress === "secondary" ? "`" : "") + (s.weight === "l" ? "." : "_")
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
export function parseProduction(underlying: Syllable[], hierarchy: StressMark[]): Word {
  let prev = [empty()]
  for (let s of underlying) {
    prev = [
      // NoM is "for descriptions that lack a main stress", whereas M is for ones that have it.
      // That means that
      // (1) M needs to filter its output by having a main stress
      // (2) No M needs to filter its output by not having a main stress
      // (3) M F1 S and M F2 need to filter input for not having a main stress (if F2 would add a stress)
      evaluate(
        prev.map(pw => append(pw, s)).filter(w => !w.head),
        hierarchy
      ), // NoM NoF
      evaluate(
        prev.map(pw => append(pw, { s1: s })).filter(w => !w.head),
        hierarchy
      ), // NoM F1 NoS
      evaluate(
        prev.map(pw => append(pw, { s1: { ...s, stress: "secondary" } })).filter(w => !w.head),
        hierarchy
      ), // NoM F1 S
      evaluate(prev.map(appendToLastFoot(s, "secondary")).filter(w => w && !w.head) as Word[], hierarchy), // NoM F2

      evaluate(
        prev.map(pw => append(pw, s)).filter(w => w.head),
        hierarchy
      ), // M NoF
      evaluate(
        prev.map(pw => append(pw, { s1: s })).filter(w => w.head),
        hierarchy
      ), // M F1 NoS
      evaluate(
        prev.map(pw => append(pw, { s1: { ...s, stress: "primary" } })).filter(w => w.head),
        hierarchy
      ), // M F1 S
      evaluate(prev.map(appendToLastFoot(s, "primary")).filter(w => w && w.head) as Word[], hierarchy), // M F2
    ].filter(w => !!w)
    console.log(prev.map(formatWord))
  }
  // TODO: check whether ALL winning candidates must have a head; I can't remember
  let next = prev.filter(w => w.head)
  return evaluate(next.length ? next : prev, hierarchy) ?? empty()
}
function append(word: Word, foot: Foot | Syllable): Word {
  let feet = [...word.feet, foot]
  return { head: findHead(feet), feet }
}
function appendToLastFoot(foot: Syllable, stress: "primary" | "secondary"): (word: Word) => Word | undefined {
  return word => {
    if (word.feet.length === 0) {
      return undefined
    }
    let last = word.feet.at(-1)
    if (!(last && isFoot(last) && !last.s2)) {
      return undefined
    }
    let feet = word.feet.slice(0, -1)
    feet.push({ ...last, s2: last.s1.stress === "unstressed" ? { ...foot, stress } : foot })
    return { head: findHead(feet), feet }
  }
}
/**
 * NOTE: Empty strings return an undefined head.
 * NOTE: This isn't generally correct, but it fits the Garawa example
 */
export function parseTrochaic(overt: Syllable[]): Word {
  if (overt.length === 0) {
    return { head: undefined, feet: [] }
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
  return { head: findHead(feet), feet }
}
export function findHead(feet: Array<Foot | Syllable>): Foot | undefined {
  return feet.find(f => isFoot(f) && (f.s1.stress === "primary" || f.s2?.stress === "primary")) as Foot
}
