function unalignedChars(input: string, output: string, operation: "del" | "ins"): Array<[number, string]> {
    // let chars = []
    // let offset = 0
    // for (let [type, [start, stop]] of optimal(levenshtein(input, output))) {
    //     if (type === operation && type === 'del') {
    //         chars.push([start + offset, input[start]])
    //     } else if (type === operation && type === 'ins') {
    //         chars.push([start + offset, -1])
    //     }
    //     if (type === 'del') {
    //         offset--
    //     } else if (type === 'ins') {
    //         offset ++
    //     }
    // }
    // return chars
    return []
}
/** 
 * Adapted straight from Python; it looks too clever for me, so I probably got it from a book.
 * As far as I can tell, the powerset is guaranteed to be of size 2 ** xs.length,
 * And the bit pattern of the index is the same as the set itself.
 * So for each bit pattern _i_, you check each bit at index _j_ of the list.
 * If it's 1, then you keep the element at index _j_.
 */
export function powerset<T>(xs: T[]): T[][] {
  let acc = [];
  for (let i = 0; i < 2 ** xs.length; i++) {
    acc.push(xs.filter((_, j) => (2 ** j) & i));
  }
  return acc;
}
/** Not even sure what's going on here. Looks like we're running a list of edits on a string. */
function rebuild(output: string, cs: Array<[number, string]>): string {
  cs.reverse()
  for (let [n, c] of cs) {
    output = output.slice(0, n) + c + output.slice(n)
  }
  return output
}
export function maxRepair(input: string, output: string): Array<string> {
  // TODO: 'del' is a member of a union ok
  return powerset(unalignedChars(input, output, "del")).map(cs => rebuild(output, cs));
}
