import { Column, Faith, Erc } from './types'
import { partition, zipWith } from './util/array'

export let idasp = Faith("Ident (asp)", () => 0)
export let idvoice = Faith("Ident (voice)", () => 0)
export let idasp_v = Faith("Ident (asp)/_V", () => 0)
export let idvoice_v = Faith("Ident (voice)/_V", () => 0)
export let nopvmvpv = Faith("*[+v][-v][+v]", () => 0)
export let noDh = Faith("*dh", () => 0)
export let noVoiceobs = Faith("*[-son/+voice]", () => 0)
export let noAsp = Faith("*aspiration", () => 0)
let constraints = {
  "Ident (asp)": idasp,
  "Ident (voice)": idvoice,
  "Ident (asp)/_V": idasp_v,
  "Ident (voice)/_V": idvoice_v,
  "*[+v][-v][+v]": nopvmvpv,
  "*dh": noDh,
  "*[-son/+voice]": noVoiceobs,
  "*aspiration": noAsp,
}
function parseViolation(vln: string): number {
    let v = vln.trim()
    return v == "" ? 0 : parseInt(v)
}
function cmp(a: number, b: number): Erc {
    if (a > b) {
        return 'w'
    } else if (a < b) {
        return 'l'
    } else {
        return '='
    }
}
export function absToERC(tableau: string[][]): Erc[][] {
    let violations = tableau.map(line => line.slice(2).map(parseViolation))
    let [winners, rivals] = partition(violations, line => line[0] > 0)
    let winner = winners[0].slice(1)
    return rivals.map(rival => zipWith(rival.slice(1), winner, cmp))
}
function relativeToERC(violation: number): Erc {
    if (violation > 0) {
        return 'w'
    } else if (violation < 0) {
        return 'l'
    } else {
        return '='
    }
}
export function absToRelative(tableau: string[][]): number[][] {
    let violations = tableau.map(line => line.slice(2).map(parseViolation))
    let [winners, rivals] = partition(violations, line => line[0] > 0)
    let winner = winners[0].slice(1)
    return rivals.map(rival => zipWith(rival.slice(1), winner, (r, w) => r - w))
}
export function readJsonViolations(json: string): Column[] {
    return zipWith(Object.values(constraints), JSON.parse(json) as number[][], (k,column) => Column(k, column.map(relativeToERC)))
}

