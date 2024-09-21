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
function testall(testo: Record<string, () => void>) {
  for (let [name, f] of Object.entries(testo)) {
    test(name, f);
  }
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
    const j = JSON.parse(
      fs.readFileSync("ot_learning/pseudo-korean.json", "utf8")
    );
    eq(j.length, 8);
    for (let row of j) {
      eq(row.length, 105);
    }
  },
  testAllMethods() {
    equal(
      rcd(
        readJsonViolations(
          fs.readFileSync("ot_learning/pseudo-korean.json", "utf8")
        )
      ),
      [
        [idasp, idvoice, idasp_v, idvoice_v, noDh],
        [nopvmvpv, noVoiceobs, noAsp],
      ]
    );
  },
  testEval() {
    eq(
      ot.evaluate(
        Mark("mark-length", (s) => s.length),
        ["hi"]
      ),
      2
    );
    eq(
      ot.evaluate(
        Faith("faith-length", (x, y) => (x + y).length),
        ["hi", "there"]
      ),
      7
    );
  },
  testBounds1: () => eq(ot.simplyBounds([2, 0, 0, 0], [0, 0, 1, 1]), false),
  testBounds2: () => eq(ot.simplyBounds([0, 0, 1, 2], [0, 0, 1, 1]), true),
  testBounds3: () => eq(ot.simplyBounds([2, 0, 0, 0], [1, 0, 0, 1]), false),
  testBounds4: () => eq(ot.simplyBounds([0, 0, 1, 1], [0, 0, 1, 1]), false),
  testBounds5: () => eq(ot.simplyBounds([2, 0], [2, 0]), false),
  maxRepair1: () =>
    equal(
      faith.maxRepair("tinkomati", "inkomai"),
      qw("inkomai tinkomai inkomati tinkomati")
    ),
  maxRepair2: () =>
    equal(
      faith.maxRepair("inkomai", "komai"),
      qw("ikomai nkomai inkomai komai")
    ),
  maxRepair3: () =>
    equal(
      faith.maxRepair("inkomai", "komati"),
      qw("ikomati nkomati inkomati komati")
    ),
  maxRepair4: () =>
    equal(faith.maxRepair("inkomai", "ikomati"), qw("ikomati inkomati")),
});
