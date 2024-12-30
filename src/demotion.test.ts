import { testall, meterUnparsed } from "./util/testing.ts"
import { strictEqual as eq, deepEqual as equal } from "node:assert"
import * as demotion from "./demotion.ts"
import fs from "node:fs"
import {
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
import {
  footBin,
  mainLeft,
  parseFoot,
  allFeetRight,
  footNonFinal,
  allFeetLeft,
  mainRight,
  iambic,
  wsp,
  nonFinal,
  wordFootLeft,
  wordFootRight,
} from "./constraint.ts"
testall("Demotion", {
  rcdBasic() {
    equal(demotion.recursive(readJsonViolations(fs.readFileSync("ot_learning/pseudo-korean.json", "utf8"))), [
      [idasp, idvoice, idasp_v, idvoice_v, noDh],
      [nopvmvpv, noVoiceobs, noAsp],
    ])
  },
  ripcdLearnabilityInOTChapter4Success() {
    equal(
      demotion
        .errorDriven(meterUnparsed("...'.."), [
          allFeetLeft,
          allFeetRight,
          iambic,
          mainRight,
          footNonFinal,
          footBin,
          mainLeft,
          parseFoot,
          wsp,
          nonFinal,
          wordFootLeft,
          wordFootRight,
        ])
        .map(h => h.name),
      [
        "AllFeetRight",
        "AllFeetLeft",
        "MainRight",
        "FootNonFinal",
        "Iambic",
        "FootBin",
        "MainLeft",
        "Parse",
        "WSP",
        "NonFinal",
        "WordFootLeft",
        "WordFootRight",
      ]
    )
  },
  ripcdCh4Fail1() {
    equal(
      demotion
        .errorDriven(meterUnparsed(".'..`.."), [
          parseFoot,
          mainLeft,
          allFeetRight,
          iambic,
          footNonFinal,
          allFeetLeft,
          mainRight,
          footBin,
          wsp,
          nonFinal,
          wordFootLeft,
          wordFootRight,
        ])
        .map(h => h.name),
      [
        "Parse",
        "MainLeft",
        "AllFeetRight",
        "Iambic",
        "FootNonFinal",
        "AllFeetLeft",
        "MainRight",
        "FootBin",
        "WSP",
        "NonFinal",
        "WordFootLeft",
        "WordFootRight",
      ]
    )
  },
  ripcdCh4Fail2() {
    equal(
      demotion
        .errorDriven(meterUnparsed(".'_.."), [wsp, footBin, mainLeft, footNonFinal, parseFoot, wordFootRight, nonFinal])
        .map(h => h.name),
      ["WSP", "FootBin", "MainLeft", "FootNonFinal", "NonFinal", "Parse", "WordFootRight"]
    )
  },
})
