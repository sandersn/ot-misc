import assert from "assert";
import { Constraint } from "./types";
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
