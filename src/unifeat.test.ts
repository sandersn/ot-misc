import {testall} from './test'
import { strictEqual as eq, deepEqual as equal } from "node:assert";
import { phonemes } from './unifeat'
import {filterValues, collapsePairs} from './util/map'

let conss = filterValues(phonemes, phone => phone['cons'] === true)
let vowels = filterValues(phonemes, phone => phone['cons'] === false)
function duplicates() {
    // TODO: map keys aren't checked by deep equal in JS, so can't use them to deduplicate
    return Array.from( collapsePairs(Object.entries(phonemes).map(([k, v]) => [Object.entries(v), k] as [any, string])).values()).filter(cs => cs.length > 1)
}
testall({
    duplicates() { 
        equal(duplicates(), `k q
ç ʂ ʃ
ʋ ʙ
ɳ ɲ
ɑ a
ɢ g
ʈ c
ɭ ʎ
ɱ m
h χ ʰ
ə ɜ
ɻ j
ɰ ʀ
ɦ ʁ
ʝ ʐ ʒ
ɟ ɖ
ŋ ɴ
ʉ ʊ`.split('\n').map(s => s.split(' ')))
    }
})
