import { testall } from "./util/testing";
import { zip } from "./util/array";
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
import { Mark, Faith, Tree } from "./types";
import fs from "node:fs";
import * as ot from "./ot";
import * as faith from "./faith";
import * as mark from "./mark";
import * as lev from "./lev";
import { phonemes, phonesToFeatures } from "./unifeat";
function qw(s: string): string[] {
  return s.split(/\s+/);
}
function* pairs(ss: string[]) {
  for (let s1 of ss) {
    for (let s2 of ss) {
      yield [s1, s2] as const;
    }
  }
}
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
  "featureDistance(a,e) is 0.5 + 0.5": () => eq(lev.featureDistance(phonemes["a"], phonemes["e"]), 1),
  "featureDistance(a,a) is 0": () => eq(lev.featureDistance(phonemes["a"], phonemes["a"]), 0),
  "feature levenshtein(ap,pbcdpe)"() {
    // minimum value to trigger bug was 1.5
    equal(lev.flevenshtein(phonesToFeatures("ap"), phonesToFeatures("pbcdpe"), 2.0), [
      [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
      [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 11.0],
      [4.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
    ]);
  },
  charLevenshtein() {
    equal(lev.levenshtein("ab_de=", "ab@d"), [
      [0, 1, 2, 3, 4],
      [1, 0, 1, 2, 3], // a
      [2, 1, 0, 1, 2], // b
      [3, 2, 1, 2, 3], // _
      [4, 3, 2, 3, 2], // d
      [5, 4, 3, 4, 3], // e
      [6, 5, 4, 5, 4], // =
      //  a  b  @  d
    ]);
  },
  levenshteinOptimalPath() {
    equal(
      lev.optimal([
        [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
        [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 11.0],
        [4.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
      ]),
      [
        ["delete", [0, 0]],
        ["substitute", [1, 0]],
        ["insert", [2, 1]],
        ["insert", [2, 2]],
        ["insert", [2, 3]],
        ["insert", [2, 4]],
        ["insert", [2, 5]],
      ]
    );
  },
  "optimal path is reflexive"() {
    for (let [s1, s2] of pairs(qw("i am the eggman you are a walrus googookachoo"))) {
      let onetwo = lev.optimal(lev.levenshtein(s1, s2));
      let twoone = lev
        .optimal(lev.levenshtein(s2, s1))
        .map(([op, [i, j]]) => [op === "insert" ? "delete" : op === "delete" ? "insert" : op, [j, i]] as const);
      equal(onetwo, twoone);
    }
  },
  levenshteinRealistic() {
    equal(lev.flevenshtein(phonesToFeatures("ət"), phonesToFeatures("tʃʊɪtʰ"), 3.286924), [
      [0.0, 3.286924, 6.573848, 9.860772, 13.147696, 16.43462, 19.721544],
      [3.286924, 6.573848, 9.860772, 7.573848, 10.860772, 14.147696, 17.43462],
      [6.573848, 3.286924, 6.573848, 9.860772, 13.147696, 10.860772, 14.147696],
    ]);
    equal(
      lev.optimal([
        [0.0, 3.286924, 6.5738479999999999, 9.8607720000000008, 13.147696, 16.434619999999999, 19.721544000000002],
        [
          3.286924, 6.5738479999999999, 9.8607720000000008, 7.5738479999999999, 10.860772000000001, 14.147696,
          17.434619999999999,
        ],
        [
          6.5738479999999999, 3.286924, 6.5738479999999999, 9.8607720000000008, 13.147696, 10.860772000000001,
          14.147696,
        ],
      ]),
      [
        ["insert", [0, 0]],
        ["insert", [0, 1]],
        ["substitute", [0, 2]],
        ["insert", [1, 3]],
        ["substitute", [1, 4]],
        ["insert", [2, 5]],
      ]
    );
  },
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
  genRepair() {
    equal(
      ot.genRepair("inkomai", [mark.onsetRepair], [faith.depRepair, faith.depInitRepair, faith.maxRepair]),
      new Set([
        "inkomai",
        "inkoma",
        "inkomati",
        "komai",
        "koma",
        "komati",
        "tinkomai",
        "tikoma",
        "nkomati",
        "nkomai",
        "tikomati",
        "ikomati",
        "tinkomati",
        "tinkoma",
        "tikomai",
        "ikoma",
        "ikomai",
        "nkoma",
      ])
    );
  },
  "evaluation of candidates generated by repair"() {
    let input = "inkomai";
    let winners = Array.from(
      ot.genRepair(input, [mark.onsetRepair], [faith.depRepair, faith.depInitRepair, faith.maxRepair])
    );
    let winnerProfiles = winners.map(output =>
      [mark.onset, faith.depIO, faith.depInitSigma, faith.maxIO].map(con => ot.evaluate(con, [input, output]))
    );
    equal(zip(winners, winnerProfiles), [
      ["inkomai", [2, 0, 0, 0]],
      ["inkoma", [1, 0, 0, 1]],
      ["inkomati", [1, 1, 0, 0]],
      ["komai", [1, 0, 0, 2]],
      ["koma", [0, 0, 0, 3]],
      ["komati", [0, 1, 0, 2]],
      ["tinkomai", [1, 1, 1, 0]],
      ["tinkoma", [0, 1, 1, 1]],
      ["tinkomati", [0, 2, 1, 0]],
      ["ikomai", [2, 0, 0, 1]],
      ["nkomai", [1, 0, 0, 1]],
      ["ikoma", [1, 0, 0, 2]],
      ["nkoma", [0, 0, 0, 2]],
      ["ikomati", [1, 1, 0, 1]],
      ["nkomati", [0, 1, 0, 1]],
      ["tikomai", [1, 1, 1, 1]],
      ["tikoma", [0, 1, 1, 2]],
      ["tikomati", [0, 2, 1, 1]],
    ]);
  },
  boundingTree() {
    let input = "inkomai";
    let winners = Array.from(
      ot.genRepair(input, [mark.onsetRepair], [faith.depRepair, faith.depInitRepair, faith.maxRepair])
    );
    let winnerProfiles = winners.map(output =>
      [mark.onset, faith.depIO, faith.depInitSigma, faith.maxIO].map(con => ot.evaluate(con, [input, output]))
    );
    let tree = ot.boundingTree(winnerProfiles);
    equal(
      tree,
      Tree(
        [1, 1, 1, 1],
        [
          Tree([1, 1, 1], [Tree([0, 3], [Tree([3]), Tree([0])]), Tree([1, 2], [Tree([3]), Tree([1])]), Tree([2, 1])]),
          Tree([1, 0, 1], [Tree([0, 3], [Tree([3]), Tree([0])]), Tree([1, 1], [Tree([3]), Tree([2])]), Tree([2, 0])]),
          Tree(
            [1, 1, 1],
            [
              Tree([1, 2], [Tree([3]), Tree([1])]),
              Tree([1, 1], [Tree([3]), Tree([2])]),
              Tree([2, 1], [Tree([1]), Tree([2])]),
            ]
          ),
          Tree([1, 1, 1], [Tree([2, 1]), Tree([2, 0]), Tree([2, 1], [Tree([1]), Tree([2])])]),
        ]
      )
    );
    eq(ot.isBounded([2, 0, 0, 0], tree), false);
    eq(ot.isBounded([0, 0, 0, 2], tree), false);
    let bounders = zip(winners, winnerProfiles).filter(([_, profile]) => !ot.isBounded(profile, tree));
    equal(bounders, [
      ["inkomai", [2, 0, 0, 0]],
      ["inkoma", [1, 0, 0, 1]],
      ["inkomati", [1, 1, 0, 0]],
      ["koma", [0, 0, 0, 3]],
      ["komati", [0, 1, 0, 2]],
      ["tinkomai", [1, 1, 1, 0]],
      ["tinkoma", [0, 1, 1, 1]],
      ["tinkomati", [0, 2, 1, 0]],
      ["nkomai", [1, 0, 0, 1]],
      ["nkoma", [0, 0, 0, 2]],
      ["ikomati", [1, 1, 0, 1]],
      ["nkomati", [0, 1, 0, 1]],
      ["tikomai", [1, 1, 1, 1]],
    ]);
    // a candidate set whose tree-bounded candidates are removed will produce the same bounding tree
    equal(ot.boundingTree(winnerProfiles.filter(profile => !ot.isBounded(profile, tree))), tree);
  },
  candidateTree() {
    equal(
      ot.candidateTree([
        ["cost][us", [1, 1, 0, 0, 0]],
        ["cos]t[us", [0, 1, 0, 0, 1]],
        ["cos][tus", [0, 0, 1, 0, 0]],
      ]),
      Tree(
        [
          [
            ["cost][us", [1, 1, 0, 0, 0]],
            ["cos]t[us", [0, 1, 0, 0, 1]],
            ["cos][tus", [0, 0, 1, 0, 0]],
          ],
          [1, 1, 1, 0, 1],
        ],
        [
          Tree(
            [
              [
                ["cos]t[us", [1, 0, 0, 1]],
                ["cos][tus", [0, 1, 0, 0]],
              ],
              [1, 1, 0, 1],
            ],
            [
              Tree([[["cos][tus", [1, 0, 0]]], []]),
              Tree([[["cos]t[us", [1, 0, 1]]], []]),
              Tree(
                [
                  [
                    ["cos]t[us", [1, 0, 1]],
                    ["cos][tus", [0, 1, 0]],
                  ],
                  [1, 1, 1],
                ],
                [
                  Tree([[["cos][tus", [1, 0]]], []]),
                  Tree([[["cos]t[us", [1, 1]]], []]),
                  Tree([[["cos][tus", [0, 1]]], []]),
                ],
              ),
              Tree([[["cos][tus", [0, 1, 0]]], []]),
            ],
          ),
          Tree([[["cos][tus", [0, 1, 0, 0]]], []]),
          Tree(
            [
              [
                ["cost][us", [1, 1, 0, 0]],
                ["cos]t[us", [0, 1, 0, 1]],
              ],
              [1, 1, 0, 1],
            ],
            [
              Tree([[["cos]t[us", [1, 0, 1]]], []]),
              Tree(
                [
                  [
                    ["cost][us", [1, 0, 0]],
                    ["cos]t[us", [0, 0, 1]],
                  ],
                  [1, 0, 1],
                ],
                [
                  Tree([[["cos]t[us", [0, 1]]], []]),
                  Tree(
                    [
                      [
                        ["cost][us", [1, 0]],
                        ["cos]t[us", [0, 1]],
                      ],
                      [1, 1],
                    ],
                    [Tree([[["cos]t[us", [1]]], []]), Tree([[["cost][us", [1]]], []])],
                  ),
                  Tree([[["cost][us", [1, 0]]], []]),
                ],
              ),
              Tree(
                [
                  [
                    ["cost][us", [1, 1, 0]],
                    ["cos]t[us", [0, 1, 1]],
                  ],
                  [1, 1, 1],
                ],
                [
                  Tree([[["cos]t[us", [1, 1]]], []]),
                  Tree(
                    [
                      [
                        ["cost][us", [1, 0]],
                        ["cos]t[us", [0, 1]],
                      ],
                      [1, 1],
                    ],
                    [Tree([[["cos]t[us", [1]]], []]), Tree([[["cost][us", [1]]], []])],
                  ),
                  Tree([[["cost][us", [1, 1]]], []]),
                ],
              ),
              Tree([[["cost][us", [1, 1, 0]]], []]),
            ],
          ),
          Tree(
            [
              [
                ["cost][us", [1, 1, 0, 0]],
                ["cos]t[us", [0, 1, 0, 1]],
                ["cos][tus", [0, 0, 1, 0]],
              ],
              [1, 1, 1, 1],
            ],
            [
              Tree(
                [
                  [
                    ["cos]t[us", [1, 0, 1]],
                    ["cos][tus", [0, 1, 0]],
                  ],
                  [1, 1, 1],
                ],
                [
                  Tree([[["cos][tus", [1, 0]]], []]),
                  Tree([[["cos]t[us", [1, 1]]], []]),
                  Tree([[["cos][tus", [0, 1]]], []]),
                ]
              ),
              Tree([[["cos][tus", [0, 1, 0]]], []]),
              Tree(
                [
                  [
                    ["cost][us", [1, 1, 0]],
                    ["cos]t[us", [0, 1, 1]],
                  ],
                  [1, 1, 1],
                ],
                [
                  Tree([[["cos]t[us", [1, 1]]], []]),
                  Tree(
                    [
                      [
                        ["cost][us", [1, 0]],
                        ["cos]t[us", [0, 1]],
                      ],
                      [1, 1],
                    ],
                    [Tree([[["cos]t[us", [1]]], []]), Tree([[["cost][us", [1]]], []])]
                  ),
                  Tree([[["cost][us", [1, 1]]], []]),
                ]
              ),
              Tree(
                [
                  [
                    ["cost][us", [1, 1, 0]],
                    ["cos][tus", [0, 0, 1]],
                  ],
                  [1, 1, 1],
                ],
                [
                  Tree([[["cos][tus", [0, 1]]], []]),
                  Tree([[["cos][tus", [0, 1]]], []]),
                  Tree([[["cost][us", [1, 1]]], []]),
                ]
              ),
            ]
          ),
          Tree(
            [
              [
                ["cost][us", [1, 1, 0, 0]],
                ["cos][tus", [0, 0, 1, 0]],
              ],
              [1, 1, 1, 0],
            ],
            [
              Tree([[["cos][tus", [0, 1, 0]]], []]),
              Tree([[["cos][tus", [0, 1, 0]]], []]),
              Tree([[["cost][us", [1, 1, 0]]], []]),
              Tree(
                [
                  [
                    ["cost][us", [1, 1, 0]],
                    ["cos][tus", [0, 0, 1]],
                  ],
                  [1, 1, 1],
                ],
                [
                  Tree([[["cos][tus", [0, 1]]], []]),
                  Tree([[["cos][tus", [0, 1]]], []]),
                  Tree([[["cost][us", [1, 1]]], []]),
                ]
              ),
            ]
          ),
        ],
      )
    );
  },
});
