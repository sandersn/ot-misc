import { qw, testall, stressUnparsed } from "./util/testing.ts"
import { strictEqual as eq, deepEqual as equal, fail } from "node:assert"
import {
  absToRelative,
  readJsonViolations,
  idasp,
  idasp_v,
  idvoice,
  idvoice_v,
  noAsp,
  noDh,
  noVoiceobs,
  nopvmvpv,
} from "./hydrogen.ts"
import { rcd } from "./rcd.ts"
import { Mark, Faith } from "./types.ts"
import { parseTrochaic, Word } from "./word.ts"
import type { StressMark } from "./types.ts"
import fs from "node:fs"
import * as ot from "./ot.ts"
import * as faith from "./faith.ts"
import * as mark from "./mark.ts"
import { phonesToFeatures } from "./unifeat.ts"
testall("General OT tests", {
  absToRelative() {
    // abs is without titles right now
    let abs = [
      ["foo", "foo", "", "1", "", "2"],
      ["", "oof", "1", "", "", "1"],
      ["", "oaf", "", "2", "", ""],
    ]
    // This is the "backward language" so foo -> oof
    let rel = [
      [1, 0, 1],
      [2, 0, -1],
    ]
    equal(rel, absToRelative(abs))
  },
  readJson() {
    const j = JSON.parse(fs.readFileSync("ot_learning/pseudo-korean.json", "utf8"))
    eq(j.length, 8)
    for (let row of j) {
      eq(row.length, 105)
    }
  },
  rcdBasic() {
    equal(rcd(readJsonViolations(fs.readFileSync("ot_learning/pseudo-korean.json", "utf8"))), [
      [idasp, idvoice, idasp_v, idvoice_v, noDh],
      [nopvmvpv, noVoiceobs, noAsp],
    ])
  },
  eval() {
    eq(
      ot.evaluate(
        Mark("mark-length", s => s.length),
        ["hi"],
      ),
      2,
    )
    eq(
      ot.evaluate(
        Faith("faith-length", (x, y) => (x + y).length),
        ["hi", "there"],
      ),
      7,
    )
  },
  bounds1: () => eq(ot.simplyBounds([2, 0, 0, 0], [0, 0, 1, 1]), false),
  bounds2: () => eq(ot.simplyBounds([0, 0, 1, 2], [0, 0, 1, 1]), true),
  bounds3: () => eq(ot.simplyBounds([2, 0, 0, 0], [1, 0, 0, 1]), false),
  bounds4: () => eq(ot.simplyBounds([0, 0, 1, 1], [0, 0, 1, 1]), false),
  bounds5: () => eq(ot.simplyBounds([2, 0], [2, 0]), false),
  powerset1: () =>
    equal(faith.powerset("abc".split("")), [
      [],
      qw("a"),
      qw("b"),
      qw("a b"),
      qw("c"),
      qw("a c"),
      qw("b c"),
      qw("a b c"),
    ]),
  powerset0: () => equal(faith.powerset([]), [[]]),
  // My comments in ot-factorial say that the tinkomati example is from Axininca Campa, in McCarthy's Thematic Guide to OT.
  syllabify() {
    equal(mark.syllabify(phonesToFeatures("inkomai")), [
      [
        {
          ATR: true,
          approx: true,
          back: false,
          cons: false,
          contin: true,
          high: true,
          low: false,
          round: false,
          son: true,
        },
        {
          anterior: true,
          approx: false,
          cons: true,
          contin: false,
          nasal: true,
          place: "coronal",
          son: true,
          voice: true,
        },
      ],
      [
        { approx: false, back: true, cons: true, contin: false, place: "dorsal", son: false, voice: false },
        {
          ATR: true,
          approx: true,
          back: true,
          cons: false,
          contin: true,
          high: false,
          low: false,
          round: true,
          son: true,
        },
      ],
      [
        { approx: false, cons: true, contin: false, nasal: true, place: "labial", son: true, voice: true },
        {
          ATR: false,
          approx: true,
          back: false,
          cons: false,
          contin: true,
          high: false,
          low: true,
          round: false,
          son: true,
        },
      ],
      [
        {
          ATR: true,
          approx: true,
          back: false,
          cons: false,
          contin: true,
          high: true,
          low: false,
          round: false,
          son: true,
        },
      ],
    ])
  },
  maxRepair1: () => equal(faith.maxRepair("tinkomati", "inkomai"), qw("inkomai tinkomai inkomati tinkomati")),
  maxRepair2: () => equal(faith.maxRepair("inkomai", "komai"), qw("komai ikomai nkomai inkomai")),
  maxRepair3: () => equal(faith.maxRepair("inkomai", "komati"), qw("komati ikomati nkomati inkomati")),
  // TODO: I don't think this result is right. I need to re-read what MAX/repair is supposed to do.
  maxRepair4: () => equal(faith.maxRepair("inkomai", "ikomati"), qw("ikomati inkomati")),
  depRepair1: () => equal(faith.depRepair("inkomai", "komati"), qw("komati komai")),
  depRepair2: () => equal(faith.depRepair("inkomai", "inkomati"), qw("inkomati inkomai")),
  depRepair3: () => equal(faith.depRepair("inkomai", "tinkomati"), qw("tinkomati inkomati tinkomai inkomai")),
  depRepair4: () => equal(faith.depRepair("inkomai", "komai"), qw("komai")),
  depRepair5: () => equal(faith.depRepair("", "foo"), [...qw("foo oo fo o fo o f"), ""]),
  onset() {
    equal(mark.onsetRepair("inkomai"), qw("inkomai inkoma inkomati komai koma komati tinkomai tinkoma tinkomati"))
  },
  parseStressEmpty() {
    equal(parseTrochaic([]), { head: undefined, feet: [] })
  },
  parseEvalOneHeavy: markEval(mark.parse, "_", 1),
  parseEvalOneLight: markEval(mark.parse, ".", 1),
  parseEvalFive: markEval(mark.parse, "..'...", 3),
  parseEvalSix: markEval(mark.parse, "..'....", 4),
  footBinEvalEmpty() {
    equal(mark.footBin.evaluate(new Word([])), 0)
  },
  footBinEvalOneHeavy: markEval(mark.footBin, "_", 0),
  footBinEvalOneLight: markEval(mark.footBin, ".", 0),
  footBinEvalFive: markEval(mark.footBin, "..'...", 0),
  footBinEvalSix: markEval(mark.footBin, "..'....", 0),
  wspEvalEmpty: markEval(mark.wsp, "", 0),
  wspEvalHeavyPrimary: markEval(mark.wsp, "'_", 0),
  wspEvalHeavySecondary: markEval(mark.wsp, "`_", 0),
  wspEvalHeavyUnstressed: markEval(mark.wsp, "_", 1),
  wspEvalLightUnstressed: markEval(mark.wsp, ".", 0),
  wspEvalLightPrimary: markEval(mark.wsp, "'.", 0),
  wspEvalHeavyLight: markEval(mark.wsp, ".'_.", 0),
  wspEvalHeavyLightUnstressed: markEval(mark.wsp, "._.", 1),
  wspEvalMultipleHeavyUnstressed: markEval(mark.wsp, "__._.", 3),
  wspEvalMultipleHeavyMixed: markEval(mark.wsp, "__.`_.", 2),
  aflEvalEmpty: markEval(mark.allFeetLeft, "", 0),
  aflEvalOneUnstressed: markEval(mark.allFeetLeft, ".", 0),
  aflEvalOneLight: markEval(mark.allFeetLeft, "'.", 0),
  aflEvalOneHeavy: markEval(mark.allFeetLeft, "'_", 0),
  aflEvalTwo: markEval(mark.allFeetLeft, "'..", 0),
  aflEvalFourOneStress: markEval(mark.allFeetLeft, "..'..", 2),
  aflEvalFourTwoStress: markEval(mark.allFeetLeft, "'..'..", 2),
  aflEvalFiveTwoStressInitial: markEval(mark.allFeetLeft, "'...'..", 3),
  aflEvalFiveTwoStress: markEval(mark.allFeetLeft, ".'..'..", 4),
  afrEvalEmpty: markEval(mark.allFeetRight, "", 0),
  afrEvalOneUnstressed: markEval(mark.allFeetRight, ".", 0),
  afrEvalOneLight: markEval(mark.allFeetRight, "'.", 0),
  afrEvalOneHeavy: markEval(mark.allFeetRight, "'_", 0),
  afrEvalTwo: markEval(mark.allFeetRight, "'..", 0),
  afrEvalFourOneStress: markEval(mark.allFeetRight, "..'..", 0),
  afrEvalFourTwoStress: markEval(mark.allFeetRight, "'..'..", 2),
  afrEvalFiveTwoStressInitial: markEval(mark.allFeetRight, "'...'..", 3),
  afrEvalFiveTwoStress: markEval(mark.allFeetRight, ".'..'..", 2),
  mainLeftEvalEmpty: markEval(mark.mainLeft, "", 0),
  mainLeftEvalOneUnstressed: markEval(mark.mainLeft, ".", 0),
  mainLeftEvalOneLight: markEval(mark.mainLeft, "'.", 0),
  mainLeftEvalOneHeavy: markEval(mark.mainLeft, "'_", 0),
  mainLeftEvalTwo: markEval(mark.mainLeft, "'..", 0),
  mainLeftEvalFourOneStress: markEval(mark.mainLeft, "..'..", 2),
  mainLeftEvalFourTwoStress: markEval(mark.mainLeft, "'..'..", 2),
  mainLeftEvalFiveTwoStressInitial: markEval(mark.mainLeft, "'...`..", 0),
  mainLeftEvalFiveTwoStressSecondary: markEval(mark.mainLeft, "`...'..", 3),
  mainLeftEvalFiveTwoStressNonInitial: markEval(mark.mainLeft, ".'..`..", 1),
  mainLeftEvalFiveTwoStressNonInitialSecondary: markEval(mark.mainLeft, ".`..'..", 3),
  mainRightEvalEmpty: markEval(mark.mainRight, "", 0),
  mainRightEvalOneUnstressed: markEval(mark.mainRight, ".", 0),
  mainRightEvalOneLight: markEval(mark.mainRight, "'.", 0),
  mainRightEvalOneHeavy: markEval(mark.mainRight, "'_", 0),
  mainRightEvalTwo: markEval(mark.mainRight, "'..", 0),
  mainRightEvalFourOneStress: markEval(mark.mainRight, "..'..", 0),
  mainRightEvalFourTwoStress: markEval(mark.mainRight, "'..`..", 2),
  mainRightEvalFourTwoStressSecondary: markEval(mark.mainRight, "`..'..", 0),
  mainRightEvalFiveTwoStressInitial: markEval(mark.mainRight, "'...`..", 3),
  mainRightEvalFiveTwoStressNonInitial: markEval(mark.mainRight, ".'..`..", 2),
  mainRightEvalFiveTwoStressNonInitialSecondary: markEval(mark.mainRight, ".`..'..", 0),
  wflEvalEmpty: markEval(mark.wordFootLeft, "", 0),
  wflEvalOneUnstressed: markEval(mark.wordFootLeft, ".", 1),
  wflEvalOneStressed: markEval(mark.wordFootLeft, "'.", 0),
  wflEvalTwoNonInitial: markEval(mark.wordFootLeft, ".'.", 1),
  wflEvalTwoInitial: markEval(mark.wordFootLeft, "'..", 0),
  wflEvalFiveFinal: markEval(mark.wordFootLeft, "....'.", 1),
  wflEvalFiveTwoStressed: markEval(mark.wordFootLeft, ".'..'..", 1),
  wfrEvalEmpty: markEval(mark.wordFootRight, "", 0),
  wfrEvalOneUnstressed: markEval(mark.wordFootRight, ".", 1),
  wfrEvalOneStressed: markEval(mark.wordFootRight, "'.", 0),
  wfrEvalTwoNonInitial: markEval(mark.wordFootRight, ".'.", 0),
  wfrEvalTwoInitial: markEval(mark.wordFootRight, "'..", 0),
  wfrEvalFiveFinal: markEval(mark.wordFootRight, "....'.", 0),
  wfrEvalFiveTwoStressed: markEval(mark.wordFootRight, ".'..'..", 0),
  iambicEvalEmpty: markEval(mark.iambic, "", 0),
  iambicEvalOne: markEval(mark.iambic, ".", 0),
  iambicEvalTwoInitial: markEval(mark.iambic, "'..", 1),
  iambicEvalTwo: markEval(mark.iambic, ".'.", 0),
  iambicEvalFour: markEval(mark.iambic, "'..'..", 2),
  footNonFinalEvalEmpty: markEval(mark.footNonFinal, "", 0),
  footNonFinalEvalOne: markEval(mark.footNonFinal, ".", 0),
  footNonFinalEvalOneStress: markEval(mark.footNonFinal, "'.", 1),
  footNonFinalEvalTwoInitial: markEval(mark.footNonFinal, "'..", 0),
  footNonFinalEvalTwoFinal: markEval(mark.footNonFinal, ".'.", 1),
  footNonFinalEvalThree: markEval(mark.footNonFinal, "'..'.", 1),
  nonFinalEvalEmpty: markEval(mark.nonFinal, "", 0),
  nonFinalEvalOne: markEval(mark.nonFinal, ".", 0),
  nonFinalEvalOneStress: markEval(mark.nonFinal, "'.", 1),
  nonFinalEvalTwo: markEval(mark.nonFinal, "'..", 1),
  nonFinalEvalThreeInitial: markEval(mark.nonFinal, "'...", 0),
  nonFinalEvalThreeInitialSecondary: markEval(mark.nonFinal, "'..`.", 1),
})
function markEval(constraint: StressMark, overt: string, count: number): () => void {
  return () => equal(constraint.evaluate(parseTrochaic(stressUnparsed(overt))), count)
}
