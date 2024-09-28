import assert from "assert";
import { Constraint, Erc } from "./types";
export function evaluate(constraint: Constraint, input: string[]): number {
  switch (constraint.kind) {
    case "faith":
      assert(input.length === 2);
      return constraint.eval(input[0], input[1]);
    case "mark":
      assert(input.length === 1);
      return constraint.eval(input[0]);
  }
}
function markToERC(candidates: number[], bounds: number[]): Erc[] {
  return candidates.map((c, i) => (c < bounds[i] ? "l" : c > bounds[i] ? "w" : "="));
}
/**
 * 1. There must be at least one winner in the candidate.
 * 2. There must be no losers; otherwise this candidate is worse than the bound.
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

export function genRepair(input: string, marks: Array<(output: string) => string[]>, faiths: Array<(input: string, output: string) => string[]>): Set<string> {
  let outputs = new Set([input])
  while (true) {
    let sizeBefore = outputs.size
    for (const mark of marks) {
      for (const output of outputs) {
        for (const newo of mark(output)) {
          outputs.add(newo)
        }
      }
    }
    for (const faith of faiths) {
      for (const output of outputs) {
        for (const newo of faith(input, output)) {
          outputs.add(newo)
        }
      }
    }
    if (sizeBefore === outputs.size) {
      break
    }
  }
  return outputs
}
