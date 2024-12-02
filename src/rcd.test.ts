import { testall, meterUnparsed } from "./util/testing.ts"
import { strictEqual as eq, deepEqual as equal } from "node:assert"
import { rcd, ripcd } from "./rcd.ts"
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
import { footBin, mainLeft, parse, allFeetRight, footNonFinal, allFeetLeft, mainRight, iambic, wsp, nonFinal, wordFootLeft, wordFootRight } from "./mark.ts"
testall("RCD", {
  rcdBasic() {
    equal(rcd(readJsonViolations(fs.readFileSync("ot_learning/pseudo-korean.json", "utf8"))), [
      [idasp, idvoice, idasp_v, idvoice_v, noDh],
      [nopvmvpv, noVoiceobs, noAsp],
    ])
  },
  ripcdLearnabilityInOTChapter4() {
    equal(ripcd(meterUnparsed("...'.."), [allFeetLeft, allFeetRight,iambic,mainRight,footNonFinal, footBin, mainLeft, parse, wsp, nonFinal, wordFootLeft, wordFootRight]), [])
  }
})
