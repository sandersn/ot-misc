import { suite, test } from "node:test"
import { meterPattern, meterUnparsed } from "./util/testing.ts"
import { Word, parseTrochaic, parseProduction, parseInterpretive } from "./word.ts"
import { footBin, mainLeft, parse, allFeetRight, footNonFinal, allFeetLeft, mainRight, iambic } from "./mark.ts"
import { deepEqual as equal } from "node:assert"
import type { StressMark } from "./types.ts"
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
  // TODO: Way more tests needed about here
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
    [".", "('.)`"],
    ["..", "('..)"],
    ["...", "('..)."],
    ["....", "('..)(`..)"],
    [".....", "('..).(`..)"],
    ["......", "('..)(`..)(`..)"],
    [".......", "('..).(`..)(`..)"],
  ],
  [footBin, mainLeft, parse, allFeetRight, footNonFinal, allFeetLeft, mainRight, iambic]
)
parseInterpretiveAll(
  [["._'..", ".(_'.)."]],
  [footBin, mainLeft, parse, allFeetRight, footNonFinal, allFeetLeft, mainRight, iambic]
)
function parseTrochaicAll(patterns: [string, string][]): void {
  suite("word.parseTrochaic", () => {
    for (let [overt, word] of patterns) {
      test(`${overt} => ${word}`, () => {
        const actual = parseTrochaic(meterUnparsed(overt))
        equal(actual, prosodicWord(word), `expected: ${word} -- received: ${actual}`)
      })
    }
  })
}
function parseProductionAll(patterns: Array<[string, string]>, hierarchy: StressMark[]): void {
  suite("word.parseProduction", () => {
    for (let [underlying, word] of patterns) {
      test(`${underlying} => ${word}`, () => {
        const actual = parseProduction(meterUnparsed(underlying), hierarchy)
        equal(actual, prosodicWord(word), `expected: ${word} -- received: ${actual}`)
      })
    }
  })
}
function parseInterpretiveAll(patterns: Array<[string, string]>, hierarchy: StressMark[]): void {
  suite("word.parseInterpretive", () => {
    for (let [underlying, word] of patterns) {
      test(`${underlying} => ${word}`, () => {
        const actual = parseInterpretive(meterUnparsed(underlying), hierarchy)
        equal(actual, prosodicWord(word), `expected: ${word} -- received: ${actual}`)
      })
    }
  })
}
function prosodicWord(stress: string): Word {
  return new Word(meterPattern(stress))
}
