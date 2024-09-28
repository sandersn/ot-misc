import { levenshtein, optimal, type Operation } from "./lev";
/**
 * Generate a list of edits that will work on `output`, based on the edit operations needed to turn `input` into `output`.
 * MAX constraints only turn deletes into inserts, and DEP constraints only turn inserts into deletes.
 */
function unalignedChars(input: string, output: string, operation: "insert"): Array<number>;
function unalignedChars(input: string, output: string, operation: "delete"): Array<[number, string]>;
function unalignedChars(input: string, output: string, operation: Operation): Array<[number, string]> | Array<number> {
  let edits = [];
  let offset = 0;
  for (let [op, [src, _]] of optimal(levenshtein(input, output))) {
    if (op === "delete") {
      if (operation === "delete") {
        edits.push([src + offset, input[src]] as const);
      }
      offset--;
    } else if (op === "insert") {
      if (operation === "insert") {
        edits.push(src + offset);
      }
      offset++;
    }
  }
  return edits as number[] | [number, string][];
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
/** Insert a subset of levenshtein inserts that mapped an input string into an output string. */
function undoDeletes(s: string, edits: Array<[number, string]>): string {
  if (edits.length === 0) {
    return s;
  }
  let i = 0;
  let edit = 0;
  let [n, add] = edits[edit];
  let out = "";
  for (let c of s) {
    while (i === n) {
      out += add;
      edit++;
      if (edit === edits.length) {
        return out + s.slice(i);
      }
      [n, add] = edits[edit];
    }
    out += c;
    i++;
  }
  return out;
}
function undoInserts(s: string, edits: number[]): string {
  let i = 0;
  let edit = 0;
  let out = "";
  for (let c of s) {
    if (i === edits[edit]) {
      edit++;
    } else {
      out += c;
    }
    i++;
  }
  return out;
}
// TODO: I need to re-read some basic OT literature to remember why MAX and DEP only pay attention to delete/insert
export function maxRepair(input: string, output: string): Array<string> {
  return powerset(unalignedChars(input, output, "delete")).map(cs => undoDeletes(output, cs));
}
export function depRepair(input: string, output: string): Array<string> {
  return powerset(unalignedChars(input, output, "insert")).map(inserts => undoInserts(output, inserts));
}
export function depInitRepair(input: string, output: string): Array<string> {
  return optimal(levenshtein(input, output))[0][0] == "insert" ? [output.slice(1)] : [];
}
