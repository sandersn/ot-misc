import { qw, testall } from "./util/testing";
import assert, { strictEqual as eq, deepEqual as equal, fail } from "node:assert";
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
} from "./hydrogen";
import { rcd } from "./rcd";
import { Mark, Faith, Tree, Syllable, Foot, ProsodicWord, Stress, isFoot } from "./types";
import fs from "node:fs";
import * as ot from "./ot";
import * as faith from "./faith";
import * as mark from "./mark";
import { phonesToFeatures } from "./unifeat";
testall("General OT tests", {
  absToRelative() {
    // abs is without titles right now
    let abs = [
      ["foo", "foo", "", "1", "", "2"],
      ["", "oof", "1", "", "", "1"],
      ["", "oaf", "", "2", "", ""],
    ];
    // This is the "backward language" so foo -> oof
    let rel = [
      [1, 0, 1],
      [2, 0, -1],
    ];
    equal(rel, absToRelative(abs));
  },
  readJson() {
    const j = JSON.parse(fs.readFileSync("ot_learning/pseudo-korean.json", "utf8"));
    eq(j.length, 8);
    for (let row of j) {
      eq(row.length, 105);
    }
  },
  rcdBasic() {
    equal(rcd(readJsonViolations(fs.readFileSync("ot_learning/pseudo-korean.json", "utf8"))), [
      [idasp, idvoice, idasp_v, idvoice_v, noDh],
      [nopvmvpv, noVoiceobs, noAsp],
    ]);
  },
  eval() {
    eq(
      ot.evaluate(
        Mark("mark-length", s => s.length),
        ["hi"],
      ),
      2,
    );
    eq(
      ot.evaluate(
        Faith("faith-length", (x, y) => (x + y).length),
        ["hi", "there"],
      ),
      7,
    );
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
    ]);
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
    equal(mark.onsetRepair("inkomai"), qw("inkomai inkoma inkomati komai koma komati tinkomai tinkoma tinkomati"));
  },
  footBinEvaluateEmpty() {
    // let head: Foot = { s1: { stress: "primary", weight: 'l' }, s2: { stress: "unstressed", weight: 'l' } };
    equal(mark.footBin.evaluate([]), 0);
  },
  footBinParseEmpty() {
    equal(mark.footBin.parse([]), { head: { s1: { stress: undefined, weight: "l" }, s2: undefined }, feet: [] });
  },
  footBinParseOneLight() {
    equal(mark.footBin.parse(stressOvert("'.")), {
      head: { s1: { stress: undefined, weight: "l" }, s2: undefined },
      feet: [{ stress: "primary", weight: "l" }],
    });
  },
  footBinParseOneHeavy: markFootBinParse("'_", "('_)"),
  footBinParseTwo: markFootBinParse("'..", "('..)"),
  footBinParseThree: markFootBinParse("'...", "('..)."),
  footBinParseFour: markFootBinParse("'....", "('..)(..)"),
  footBinParseFive: markFootBinParse("'.....", "('..)(..)."),
  footBinParseSix: markFootBinParse("'......", "('..)(..)(..)"),
  footBinParseSixStressFinal: markFootBinParse(".....'.", "(..)(..)(.'.)"),
  footBinEvaluateOneHeavy: markFootBinEval("_", 0),
  footBinEvaluateOneLight: markFootBinEval(".", 1),
  footBinEvaluateFive: markFootBinEval("..'...", 1),
  footBinEvaluateSix: markFootBinEval("..'....", 0),
  markWspEvaluateEmpty: markWspEval("", 0),
  markWspEvaluateHeavyPrimary: markWspEval("'_", 0),
  markWspEvaluateHeavySecondary: markWspEval("`_", 0),
  markWspEvaluateHeavyUnstressed: markWspEval("_", 1),
  markWspEvaluateLightUnstressed: markWspEval(".", 0),
  markWspEvaluateLightPrimary: markWspEval("'.", 0),
  markWspEvaluateHeavyLight: markWspEval(".'_.", 0),
  markWspEvaluateHeavyLightUnstressed: markWspEval("._.", 1),
  markWspEvaluateMultipleHeavyUnstressed: markWspEval("__._.", 3),
  markWspEvaluateMultipleHeavyMixed: markWspEval("__.`_.", 2),
});
// TODO: Can probably abstract these over constraints (as long as they never use `this`)
function markFootBinParse(overt: string, word: string): () => void {
  return () => equal(mark.footBin.parse(stressOvert(overt)), prosodicWord(word));
}
function markFootBinEval(overt: string, count: number): () => void {
  return () => equal(mark.footBin.evaluate(stressOvert(overt)), count);
}
function markWspEval(overt: string, count: number): () => void {
  return () => equal(mark.wsp.evaluate(stressOvert(overt)), count);
}
function stressOvert(stress: string): Syllable[] {
  assert(stress.indexOf("(") === -1 && stress.indexOf(")") === -1, "stressOvert only works on overt stress patterns");
  return stressPattern(stress) as Syllable[];
}
function prosodicWord(stress: string): ProsodicWord {
  let feet = stressPattern(stress);
  // TODO: This will need to allow manual specification of the head's index eventually
  let head = feet.find(isFoot) || fail("no feet in prosodic word");
  return { head, feet };
}
/** ('..)
 * . light
 * _ heavy
 * ' primary stress
 * , secondary stress
 * ( start of foot
 * ) end of foot
 */
function stressPattern(stress: string): (Syllable | Foot)[] {
  let nextStress: Stress = "unstressed";
  let foot: Syllable[] | undefined;
  let syllables: (Syllable | Foot)[] = [];
  for (let i = 0; i < stress.length; i++) {
    switch (stress[i]) {
      case "'":
        nextStress = "primary";
        break;
      case "`":
        nextStress = "secondary";
        break;
      case ".":
      case "_":
        (foot ? foot : syllables).push({ stress: nextStress, weight: stress[i] === "." ? "l" : "h" });
        nextStress = "unstressed";
        break;
      case "(":
        assert(!foot, "open parenthesis inside unclosed open parenthesis");
        foot = [];
        break;
      case ")":
        assert(foot, "close parenthesis without open parenthesis");
        if (foot.length === 1) {
          syllables.push({ s1: foot[0] });
        } else if (foot.length === 2) {
          syllables.push({ s1: foot[0], s2: foot[1] });
        } else {
          fail("foot too long" + foot.length);
        }
        foot = undefined;
        break;
    }
  }
  return syllables;
}
