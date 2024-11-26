import * as unifeat from "./unifeat";
import { Phoneme, Mark, StressMark, Syllable, Foot, isSyllable, isFoot, ProsodicWord } from "./types";
import { zipWith, count, sequence } from "./util/array";
import { assert } from "node:console";

unifeat.phonemes;
export let onset = Mark("onset", (output: string) => {
  return count(syllabify(unifeat.phonesToFeatures(output)), syll => !syll[0]["cons"]);
});
export function onsetRepair(output: string): string[] {
  function recreateSyllables(syllables: Phoneme[][]): string[] {
    let i = 0;
    let out = [];
    for (let s of syllables) {
      out.push(output.slice(i, i + s.length));
      i += s.length;
    }
    return out;
  }
  let ident = (syllable: string) => syllable;
  let del = (_: string) => "";
  let epenthesise = (syllable: string) => "t" + syllable;
  let syllables = syllabify(unifeat.phonesToFeatures(output));
  let opss: ((s: string) => string)[][] = sequence(
    syllables.map(syll => (syll[0]["cons"] ? [ident] : [ident, del, epenthesise]))
  );
  // TODO: Hacky that the inner algorithm is in syllables but the outer is in strings. It was just easier to test, I bet.
  let syllables2 = recreateSyllables(syllables);
  return opss.map(ops =>
    zipWith(ops, syllables2, (op, syll) => op(syll))
      .flat()
      .join("")
  );
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
type SyllableState = "C" | "V" | "CC" | "CV" | "C$";
export function syllabify(phs: Phoneme[]): Phoneme[][] {
  let prev: Phoneme = {};
  let it = phs[Symbol.iterator]();
  let result = it.next();
  if (result.done) {
    return [];
  }
  let ph: Phoneme = result.value;
  let acc: Phoneme[] = [];
  let syllables: Phoneme[][] = [];
  let state = (ph["cons"] ? "C" : "V") as SyllableState;
  while (!result.done) {
    switch (state) {
      case "C":
        acc.push(ph);
        advanceCons();
        break;
      case "V":
        acc.push(ph);
        advanceVowel();
        break;
      case "CC":
        acc.push(prev);
        makeSyllable();
        acc.push(ph);
        advanceCons();
        break;
      case "CV":
        acc.push(prev, ph);
        advanceVowel();
        break;
    }
  }
  if (acc.length) syllables.push(acc);
  return syllables;

  function makeSyllable(): void {
    syllables.push(acc);
    acc = [];
  }
  function advanceCons(): void {
    result = it.next();
    if (result.done) {
      // TODO: return from the whole function and break the loop
    } else ph = result.value;
    if (ph["cons"]) {
      makeSyllable();
      state = "C";
    } else {
      state = "V";
    }
  }
  function advanceVowel(): void {
    result = it.next();
    if (result.done) {
      // TODO: return from the whole function and break the loop
    } else ph = result.value;
    if (ph["cons"]) {
      prev = ph;
      result = it.next();
      if (result.done) {
        acc.push(prev);
        // TODO: return from the whole function and break the loop
      } else ph = result.value;
      if (ph["cons"]) {
        state = "CC";
      } else {
        makeSyllable();
        state = "CV";
      }
    } else {
      prev = {};
      makeSyllable();
      state = "V";
    }
  }
}
/**
 * NOTE: Empty strings return a sentinel head (no stress at all).
 * TODO: I'm not certain that "unfooted" is the same as "degenerate foot", so maybe I should be generating degenerate feet instead.
 * NOTE: I'm pretty sure stress parsing is actually ambiguous, or at least requires lookahead, or *at least* requires a normal parser.
 * But it's *usually* a trochaic word, or at least a foot at the beginning of the word, which this parser should handle.
 * The bad input is .'.., which could parse as (.'.). or .('..). This parser always produces the former.
 */
export function parseStress(overt: Syllable[]): ProsodicWord {
  let sentinelHead: Foot = { s1: { weight: "l", stress: undefined }, s2: undefined };
  if (overt.length === 0) {
    return { head: sentinelHead, feet: [] };
  }
  let foot = { s1: undefined, s2: undefined };
  let feet: (Foot | Syllable)[] = [];
  let prev: Syllable | undefined;
  for (const s of overt) {
    if (s.weight === "l") {
      if (s.stress === "unstressed") {
        // l -> prev = l
        // ll -> push l, prev = l
        // hl -> push h, prev = l
        // 'll -> push ('ll), prev = undefined
        // 'hl -> push ('hl), prev = undefined
        if (!prev) {
          prev = s;
        } else if (prev.stress === "unstressed") {
          feet.push(prev);
          prev = s;
        } else {
          feet.push({ s1: prev, s2: s });
          prev = undefined;
        }
      } else {
        // 'l -> prev = 'l
        // l'l -> push (l'l), prev = undefined
        // h'l -> push (h'l), prev = undefined ??
        // 'l'l -> push ('l), prev = 'l
        // 'h'l -> push ('h), prev = 'l
        if (!prev) {
          prev = s;
        } else if (prev.stress === "unstressed") {
          feet.push({ s1: prev, s2: s });
          prev = undefined;
        } else {
          feet.push({ s1: prev });
          prev = s;
        }
      }
    } else if (s.weight === "h") {
      if (s.stress === "unstressed") {
        // h -> prev = h
        // lh -> push l, prev = h
        // hh -> push h, prev = h
        // 'lh -> push ('lh), prev = undefined ??
        // 'hh -> push ('h), prev = h (but prev =/= 'h)
        if (!prev) {
          prev = s;
        } else if (prev.stress === "unstressed") {
          feet.push(prev);
          prev = s;
        } else {
          if (prev.weight === "l") {
          feet.push({ s1: prev, s2: s });
          prev = undefined;
          } else {
            feet.push({ s1: prev })
            prev = s
          }
        }
      } else {
        // 'h -> prev = 'h
        // l'h -> push (l'h), prev = undefined
        // h'h -> push h, prev = 'h
        // 'l'h -> push ('l), prev = 'h
        // 'h'h -> push ('h), prev = 'h
        if (!prev) {
          prev = s
        } else if (prev.stress === "unstressed") {
          if (prev.weight === "l") {
            feet.push({ s1: prev, s2: s });
            prev = undefined;
          } else {
            feet.push(prev)
            prev = s
          }
        } else {
          feet.push({ s1: prev });
          prev = s;
        }
      }
      foot.s1;
    }
  }
  if (prev) {
    feet.push(prev.stress === "unstressed" ? prev : { s1: prev });
  }
  return { head: feet?.find(isFoot) ?? sentinelHead, feet };
}
export let footBin: StressMark = {
  kind: "mark",
  name: "FootBin",
  evaluate(overt) {
    return count(parseStress(overt).feet, sf => isFoot(sf) && sf.s2 === undefined && sf.s1.weight === "l");
  },
};
export let wsp: StressMark = {
  kind: "mark",
  name: "WSP",
  evaluate(overt) {
    return count(overt, s => s.weight === "h" && s.stress === "unstressed");
  },
};
export let parse: StressMark = {
  kind: "mark",
  name: "Parse",
  evaluate(overt) {
    return count(parseStress(overt).feet, isSyllable);
  },
};
export let allFeetLeft: StressMark = {
  kind: "mark",
  name: "AllFeetLeft",
  evaluate(overt) {
    let i = 0;
    let leftEdgeCount = 0;
    for (let sf of parseStress(overt).feet) {
      if (isFoot(sf)) {
        leftEdgeCount += i;
        i += sf.s2 ? 2 : 1;
      } else {
        i++;
      }
    }
    return leftEdgeCount;
  },
};
export let allFeetRight: StressMark = {
  kind: "mark",
  name: "AllFeetRight",
  evaluate(overt) {
    let i = 0;
    let rightEdgeCount = 0;
    for (let sf of parseStress(overt).feet) {
      if (isFoot(sf)) {
        i += sf.s2 ? 2 : 1;
        rightEdgeCount += overt.length - i;
      } else {
        i++;
      }
    }
    return count(parseStress(overt).feet, sf => isFoot(sf) && sf.s1.weight === "h");
  },
};
