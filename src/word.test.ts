import { suite, test } from "node:test"
import { meterPattern, meterUnparsed, testall } from "./util/testing.ts"
import { Word, parseTrochaic, parseProduction, parseInterpretive, underlyingMeter, underlyingSegments } from "./word.ts"
import {
  footBin,
  mainLeft,
  parseFoot,
  allFeetRight,
  footNonFinal,
  allFeetLeft,
  mainRight,
  iambic,
} from "./constraint.ts"
import { deepEqual as equal, strictEqual as eq } from "node:assert"
import type { StressMark } from "./types.ts"
testall("word.Word", {
  toStringEmpty() {
    eq(new Word([]).toString(), "")
  },
  toStringV() {
    eq(new Word([{ segment: "v", input: { segment: "v" } }]).toString(), "v")
  },
  toStringA() {
    eq(new Word([{ segment: "v" }]).toString(), "a")
  },
  toStringT() {
    eq(new Word([{ segment: "c" }]).toString(), "t")
  },
})
// NOTE: parseTrochaic isn't correct,
// but it's good enough to produce syllable structure in testing.
parseTrochaicAll([
  [".", "."],
  ["'.", "('.)"],
  ["'_", "('_)"],
  ["_", "_"],
  [".'.", ".('.)"],
  ["'_.", "('_.)"],
  [".'_", ".('_)"],
  ["'._", "('._)"],
  ["_'.", "_('.)"],
  ["'_'_", "('_)('_)"],
  ["'__", "('_)_"],
  ["_'_", "_('_)"],
  [".'..", ".('..)"],
  ["..'.", "..('.)"],
  ["'....", "('..).."],
  ["'.....", "('..)..."],
  ["..'..", "..('..)"],
  [".'..'..", ".('..)('..)"],
  ["'...'..", "('..).('..)"],
  ["'....'.", "('..)..('.)"],
  ["'......", "('..)...."],
  [".....'.", ".....('.)"],
  // Garawa examples from Learnability in OT
  ["'..", "('..)"],
  ["'...", "('..)."],
  ["'..'..", "('..)('..)"],
  ["'...'..", "('..).('..)"],
  ["'..'..'..", "('..)('..)('..)"],
  ["'...'..'..", "('..).('..)('..)"],
])
parseProductionAll(
  [
    ["", ""],
    [".", "('.)"],
    ["..", "('..)"],
    ["...", "('..)."],
    ["....", "('..)(`..)"],
    [".....", "('..).(`..)"],
    ["......", "('..)(`..)(`..)"],
    [".......", "('..).(`..)(`..)"],
  ],
  [footBin, mainLeft, parseFoot, allFeetRight, footNonFinal, allFeetLeft, mainRight, iambic]
)
parseInterpretiveAll(
  [
    ["", ""],
    ["'.", "('.)"],
    ["'..", "('..)"],
    ["'...", "('..)."],
    ["'..`..", "('..)(`..)"],
    ["'...`..", "('..).(`..)"],
    ["'..`..`..", "('..)(`..)(`..)"],
    ["'...`..`..", "('..).(`..)(`..)"],
    ["._'..", ".(_'.)."],
  ],
  [footBin, mainLeft, parseFoot, allFeetRight, footNonFinal, allFeetLeft, mainRight, iambic]
)
underlyingMeterAll([
  ["", ""],
  [".", "."],
  ["('.)", "."],
  ["..", ".."],
  ["('..)", ".."],
  ["('..).", "..."],
  ["('..)(`.)", "..."],
  ["('..)(`_)", ".._"],
])
underlyingSegmentsAll([
  ["", ""],
  ["('v.)", "v"],
  ["v.", "v"],
  ["('cv.)", "cv"],
  ["cv.", "cv"],
  ["('cvc.)", "cvc"],
  ["cvt.", "cv"],
  ["cat.", "c"],
  ["tat", ""],
  ["cvcvcv", "cvcvcv"],
  ["cv.cv.cv.", "cvcvcv"],
])
function parseTrochaicAll(patterns: [string, string][]): void {
  suite("word.parseTrochaic", () => {
    for (let [overt, word] of patterns) {
      test(`${overt} => ${word}`, () => {
        const actual = parseTrochaic(meterUnparsed(overt))
        equal(actual, meterPattern(word), `expected: ${word} -- received: ${actual}`)
      })
    }
  })
}
function parseProductionAll(patterns: Array<[string, string]>, hierarchy: StressMark[]): void {
  suite("word.parseProduction", () => {
    for (let [underlying, word] of patterns) {
      test(`${underlying} => ${word}`, () => {
        const actual = parseProduction(meterUnparsed(underlying), hierarchy)
        equal(actual, meterPattern(word), `expected: ${word} -- received: ${actual}`)
      })
    }
  })
}
function parseInterpretiveAll(patterns: Array<[string, string]>, hierarchy: StressMark[]): void {
  suite("word.parseInterpretive", () => {
    for (let [underlying, word] of patterns) {
      test(`${underlying} => ${word}`, () => {
        const actual = parseInterpretive(meterUnparsed(underlying), hierarchy)
        equal(actual, meterPattern(word), `expected: ${word} -- received: ${actual}`)
      })
    }
  })
}
function underlyingMeterAll(patterns: [string, string][]): void {
  suite("word.underlyingMeter", () => {
    for (let [parsed, underlying] of patterns) {
      test(`${parsed} => ${underlying}`, () => {
        let actual = new Word(underlyingMeter(meterPattern(parsed)))
        let expected = meterPattern(underlying)
        equal(actual, expected, `expected: ${expected} -- received: ${actual}`)
      })
    }
  })
}
function underlyingSegmentsAll(patterns: [string, string][]): void {
  suite("word.underlyingSegments", () => {
    for (let [parsed, underlying] of patterns) {
      test(`${parsed} => ${underlying}`, () => {
        let actual = new Word(underlyingSegments(meterPattern(parsed)))
        let expected = meterPattern(underlying)
        equal(actual, expected, `expected: ${expected} -- received: ${actual}`)
      })
    }
  })
}
