import { absToRelative, readJsonViolations, idasp, idasp_v, idvoice, idvoice_v, noAsp, noDh, noVoiceobs, nopvmvpv } from "./hydrogen";
import { rcd } from './rcd'
import fs from "node:fs";
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
    expect(rel).toEqual(absToRelative(abs));
  },
  readJson() {
    const j = JSON.parse(
      fs.readFileSync("ot_learning/pseudo-korean.json", "utf8")
    );
    expect(j.length).toBe(8);
    for (let row of j) {
      expect(row.length).toBe(105);
    }
  },
  testAllMethods() {
    expect(
      rcd(readJsonViolations(fs.readFileSync("ot_learning/pseudo-korean.json", "utf8")))
    ).toStrictEqual([
      [idasp, idvoice, idasp_v, idvoice_v, noDh],
      [nopvmvpv, noVoiceobs, noAsp],
    ]);
  },
});
