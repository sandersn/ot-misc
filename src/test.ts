import { qw, testall } from "./util/testing.ts"
import { strictEqual as eq, deepEqual as equal } from "node:assert"
import { absToRelative } from "./hydrogen.ts"
import { Mark, Faith } from "./types.ts"
import fs from "node:fs"
import * as ot from "./ot.ts"
import * as faith from "./faith.ts"
import * as mark from "./mark.ts"
import { phonesToFeatures } from "./phone.ts"
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
  eval() {
    eq(
      ot.evaluate(
        Mark("mark-length", s => s.length),
        ["hi"]
      ),
      2
    )
    eq(
      ot.evaluate(
        Faith("faith-length", (x, y) => (x + y).length),
        ["hi", "there"]
      ),
      7
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
})
