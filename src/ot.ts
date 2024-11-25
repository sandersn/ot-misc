import assert from "assert";
import { Constraint, Erc, Tree } from "./types";
import { transpose, zip } from "./util/array";
/**
 * When evaluating a markedness constraint, you can pass either
 * (input, output) or just (output) as args.
 */
export function evaluate(constraint: Constraint, args: string[]): number {
  switch (constraint.kind) {
    case "faith":
      assert(args.length >= 2);
      return constraint.eval(args[0], args[1]);
    case "mark":
      assert(args.length >= 1);
      return constraint.eval(args.at(-1)!);
  }
}
function markToERC(candidates: number[], bounds: number[]): Erc[] {
  return candidates.map((c, i) => (c < bounds[i] ? "l" : c > bounds[i] ? "w" : "="));
}
/**
 * 1. There must be at least one winner in the candidate.
 * 2. There must be no losers; otherwise this candidate is worse than the bound.
 * TODO: Switch input to ERC[] or something more complex and ERC-based
 */
export function simplyBounds(candidates: number[], bounds: number[], anyWinner = false): boolean {
  const erc = markToERC(candidates, bounds);
  return erc.some(c => c === "w") && erc.every(c => c !== "l");
  /*
    ## Old code is more efficient, but harder to read: ##
    if (candidates.length !== bounds.length) {
        return false
    }
    for (let i = 0; i < candidates.length; i++) {
        if (bounds[i] > candidates[i]) {
            return false
        }
        if (bounds[i] < candidates[i]) {
            anyWinner = true
        }
    }
    return anyWinner;
    */
}

export function genRepair(
  input: string,
  marks: Array<(output: string) => string[]>,
  faiths: Array<(input: string, output: string) => string[]>,
): Set<string> {
  let outputs = new Set([input]);
  while (true) {
    let sizeBefore = outputs.size;
    for (const mark of marks) {
      for (const output of outputs) {
        for (const newo of mark(output)) {
          outputs.add(newo);
        }
      }
    }
    for (const faith of faiths) {
      for (const output of outputs) {
        for (const newo of faith(input, output)) {
          outputs.add(newo);
        }
      }
    }
    if (sizeBefore === outputs.size) {
      break;
    }
  }
  return outputs;
}
function boundingSet(col: number[]): { best: number; different: number } {
  let best = col[0];
  let worst = col[0];
  for (let c of col) {
    if (c < best) best = c;
    if (c > worst) worst = c;
  }
  return best === worst ? { best, different: 0 } : { best: best + 1, different: 1 };
}
function removen<T>(l: T[], i: number): T[] {
  return l.slice(0, i).concat(l.slice(i + 1));
}
function removeColumn(tab: number[][], i: number) {
  return transpose(removen(transpose(tab), i));
}
/** TODO: Better input type than number[][] probably
 * (probably a table of ERCs, which are then transposed around) */
export function boundingTree(tab: number[][]): Tree<number[]> {
  if (tab.length === 1) {
    return { value: tab[0], kids: [] };
  }
  if (tab[0].length === 1) {
    return { value: [boundingSet(tab.map(row => row[0])).best], kids: [] };
  }
  // TODO: Avoid transpose the same way I did elsewhere, earlier
  let bounder = transpose(tab).map(boundingSet);
  return {
    value: bounder.map(b => b.best),
    kids: bounder.map((b, i) =>
      boundingTree(
        removeColumn(
          tab.filter(row => row[i] === b.best - b.different),
          i,
        ),
      ),
    ),
  };
}
/**
 * A candidate is bounded if
 * (1) it is simply bounded by the current node's violation profile or
 * (2) if it is bounded by one of the current node's children for which its violations are less than
 * or equal to the current node's.
 */
export function isBounded(candidate: number[], tree: Tree<number[]>): boolean {
  let bound = tree.value;
  return (
    simplyBounds(candidate, bound) ||
    (!!tree.kids.length &&
      zip(candidate, bound).some(([cn, bn], i) => cn < bn && isBounded(removen(candidate, i), tree.kids[i])))
  );
}

// TODO: convert [string, number[]][] to Array<{ name: string, violations: number[] }> and compare to types in type.ts
export function candidateTree(tab: [string, number[]][]): Tree<[[string, number[]][], number[]]> {
  if (tab.length === 1) {
    // TODO: Python returns `tab[0]` for the value's name, which is ill-typed (I'm not sure this case is ever tested or even possible)
    return { value: [tab, []], kids: [] };
  }
  if (violations(tab[0]).length === 1) {
    return { value: [tab, [boundingSet(tab.map(row => violations(row)[0])).best]], kids: [] };
  }
  // TODO: Avoid transpose the same way I did elsewhere, earlier
  let bounder = transpose(tab.map(violations)).map(boundingSet);
  return {
    value: [tab, bounder.map(b => b.best)],
    kids: bounder.map((b, i) =>
      candidateTree(
        updateTuples(
          rows => removeColumn(rows, i),
          tab.filter(([_, row]) => row[i] === b.best - b.different),
        ),
      ),
    ),
  };
}
function violations(row: [string, number[]]) {
  return row[1];
}
function name(row: [string, number[]]) {
  return row[0];
}
function updateTuples(f: (rows: number[][]) => number[][], ts: [string, number[]][]): [string, number[]][] {
  return zip(ts.map(name), f(ts.map(violations)));
}
