import { qw, testall } from "./util/testing.ts"
import { strictEqual as eq, deepEqual as equal, fail } from "node:assert"
import { phonemes, phonesToFeatures } from "./unifeat.ts"
import * as lev from "./lev.ts"
function* pairs(ss: string[]) {
  for (let s1 of ss) {
    for (let s2 of ss) {
      yield [s1, s2] as const
    }
  }
}
testall("Feature distance", {
  "featureDistance(a,e) is 0.5 + 0.5": () => eq(lev.featureDistance(phonemes["a"], phonemes["e"]), 1),
  "featureDistance(a,a) is 0": () => eq(lev.featureDistance(phonemes["a"], phonemes["a"]), 0),
  "feature levenshtein(ap,pbcdpe)"() {
    // minimum value to trigger bug was 1.5
    equal(lev.flevenshtein(phonesToFeatures("ap"), phonesToFeatures("pbcdpe"), 2.0), [
      [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
      [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 11.0],
      [4.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
    ])
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
    ])
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
      ],
    )
  },
  "optimal path is reflexive"() {
    for (let [s1, s2] of pairs(qw("i am the eggman you are a walrus googookachoo"))) {
      let onetwo = lev.optimal(lev.levenshtein(s1, s2))
      let twoone = lev
        .optimal(lev.levenshtein(s2, s1))
        .map(([op, [i, j]]) => [op === "insert" ? "delete" : op === "delete" ? "insert" : op, [j, i]] as const)
      equal(onetwo, twoone)
    }
  },
  levenshteinRealistic() {
    equal(lev.flevenshtein(phonesToFeatures("ət"), phonesToFeatures("tʃʊɪtʰ"), 3.286924), [
      [0.0, 3.286924, 6.573848, 9.860772, 13.147696, 16.43462, 19.721544],
      [3.286924, 6.573848, 9.860772, 7.573848, 10.860772, 14.147696, 17.43462],
      [6.573848, 3.286924, 6.573848, 9.860772, 13.147696, 10.860772, 14.147696],
    ])
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
      ],
    )
  },
})
