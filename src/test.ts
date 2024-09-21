import { strictEqual as eq, deepEqual as equal } from "node:assert";
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
import { Mark, Faith } from "./types";
import fs from "node:fs";
import * as ot from "./ot";
import * as faith from "./faith";
import * as unifeat from './unifeat'
export function testall(testo: Record<string, () => void>) {
  for (let [name, f] of Object.entries(testo)) {
    test(name, f);
  }
}
function qw(s: string): string[] {
  return s.split(/\s+/);
}
testall({
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
  testAllMethods() {
    equal(rcd(readJsonViolations(fs.readFileSync("ot_learning/pseudo-korean.json", "utf8"))), [
      [idasp, idvoice, idasp_v, idvoice_v, noDh],
      [nopvmvpv, noVoiceobs, noAsp],
    ]);
  },
  testEval() {
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
  testBounds1: () => eq(ot.simplyBounds([2, 0, 0, 0], [0, 0, 1, 1]), false),
  testBounds2: () => eq(ot.simplyBounds([0, 0, 1, 2], [0, 0, 1, 1]), true),
  testBounds3: () => eq(ot.simplyBounds([2, 0, 0, 0], [1, 0, 0, 1]), false),
  testBounds4: () => eq(ot.simplyBounds([0, 0, 1, 1], [0, 0, 1, 1]), false),
  testBounds5: () => eq(ot.simplyBounds([2, 0], [2, 0]), false),
  powerset1: () => equal(faith.powerset("abc".split('')), [[], qw("a"), qw("b"), qw("a b"), qw("c"), qw("a c"), qw("b c"), qw("a b c")]),
  powerset0: () => equal(faith.powerset([]), [[]]),
  // TODO: lev and unifeat should be done before faith and mark.
  // maxRepair1: () => equal(faith.maxRepair("tinkomati", "inkomai"), qw("inkomai tinkomai inkomati tinkomati")),
  // maxRepair2: () => equal(faith.maxRepair("inkomai", "komai"), qw("ikomai nkomai inkomai komai")),
  // maxRepair3: () => equal(faith.maxRepair("inkomai", "komati"), qw("ikomati nkomati inkomati komati")),
  // maxRepair4: () => equal(faith.maxRepair("inkomai", "ikomati"), qw("ikomati inkomati")),
//     testLev(): () => {
//         // minimum value to trigger bug was 1.5
//         equal(lev.flevenshtein(unifeat.unify('ap'),unifeat.unify('pbcdpe'),2.0),
//              [[0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
//               [2.0, 4.0, 6.0, 8.0,10.0, 12.0, 12.0],
//               [4.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0]])
//         equal(lev.optimal([[0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
//                           [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 12.0],
//                           [4.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0]]),
//              [('delete', (0, 0)),
//               ('substitute', (1, 0)),
//               ('insert', (2, 1)),
//               ('insert', (2, 2)),
//               ('insert', (2, 3)),
//               ('insert', (2, 4)),
//               ('insert', (2, 5))])
//         // TODO: Fails! Need to write lev.Change.__eq__
//         // except this will probably break align.py again
// //         test(lev.enviro("ap", "pbcdpe", 2.0),
// //              [lev.Del (0, 'a', ("#", 'p')),
// //               lev.Sub (1, ('p','p'), ("#", 'a')),
// //               lev.Ins (2, 'b', ('p', "#")),
// //               lev.Ins (2, 'c', ('p', "#")),
// //               lev.Ins (2, 'd', ('p', "#")),
// //               lev.Ins (2, 'p', ('p', "#")),
// //               lev.Ins (2, 'e', ('p', "#"))])
//         test(lev.flevenshtein(
            
//             unifeat.unify(['\xc9\x99', 't']),
//             unifeat.unify(['t', '\xca\x83', '\xca\x8a', '\xc9\xaa', 't', '\xca\xb0']),
//             3.286924),
//              [[0.0,      3.286924, 6.573848, 9.860772, 13.147696, 16.43462, 19.721544],
//               [3.286924, 6.573848, 9.860772, 8.573848, 11.860772, 15.147696, 18.43462],
//               [6.573848, 3.286924, 6.573848, 9.860772, 13.147696, 11.860772, 15.147696]])
//         test(lev.optimal([[0.0, 3.286924, 6.5738479999999999, 9.8607720000000008, 13.147696, 16.434619999999999, 19.721544000000002], [3.286924, 6.5738479999999999, 9.8607720000000008, 8.5738479999999999, 11.860772000000001, 15.147696, 18.434619999999999], [6.5738479999999999, 3.286924, 6.5738479999999999, 9.8607720000000008, 13.147696, 11.860772000000001, 15.147696]]),
//              [('insert', (0, 0)),
//               ('insert', (0, 1)),
//               ('substitute', (0, 2)),
//               ('insert', (1, 3)),
//               ('substitute', (1, 4)),
//               ('insert', (2, 5))])
//              }
});
