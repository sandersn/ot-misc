import { testall } from "./util/testing";
import { strictEqual as eq, deepEqual as equal } from "node:assert";
import { phonemes } from "./unifeat";
import { collapsePairs } from "./util/map";

function duplicates() {
  // TODO: map keys aren't checked by deep equal in JS, so can't use them to deduplicate
  return Array.from(
    collapsePairs(
      Object.entries(phonemes).map(([k, v]) => [JSON.stringify(Object.entries(v)), k] as [any, string]),
    ).values(),
  ).filter(cs => cs.length > 1);
}
testall("Phoneme feature database tests", {
  duplicates() {
    equal(
      duplicates(),
      `ʈ c
ɖ ɟ
k q
g ɢ
m ɱ
ɳ ɲ
ŋ ɴ
ʙ ʋ
ʀ ɰ
ʃ ʂ ç
ʒ ʐ ʝ
χ h ʰ
ʁ ɦ
ɻ j
ɭ ʎ
a æ
ʊ ʉ
ə ɜ`
        .split("\n")
        .map(s => s.split(" ")),
    );
  },
});
