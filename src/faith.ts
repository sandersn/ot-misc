function unalignedChars(
  input: string,
  output: string,
  operation: "del" | "ins"
): Array<[number, string]> {}
function powerset<T>(xs: T[]): T[][] {
  // lol copilot!
  return xs.reduce((sets, x) => sets.concat(sets.map((set) => [...set, x])), [
    [],
  ] as T[][]);
}
function rebuild(output: string, cs: Array<[number, string]>): string {
  // lol copilot!
  let result = "";
  for (let i = 0; i < output.length; i++) {
    if (cs.includes(output[i])) {
      result += output[i];
    }
  }
  return result;
}
export function maxRepair(input: string, output: string): Array<string> {
  // TODO: 'del' is a member of a union ok
  return powerset(unalignedChars(input, output, "del")).map((cs) =>
    rebuild(output, cs)
  );
}
