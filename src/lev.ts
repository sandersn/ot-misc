import type { Phoneme } from "./types.ts"

export type Table = number[][]
export type Operation = "insert" | "delete" | "substitute"
function _levenshtein<T>(
  s1: T[],
  s2: T[],
  indel: number,
  del: (t: T) => number,
  insert: (t: T) => number,
  substitute: (t1: T, t2: T) => number,
): Table {
  let prev = []
  for (let i = 0; i < s2.length + 1; i++) {
    prev.push(indel * i)
  }
  let table = [prev]
  for (let i = 0; i < s1.length; i++) {
    let row = [indel * (i + 1)]
    for (let j = 0; j < s2.length; j++) {
      row.push(
        Math.min(prev[j + 1] + del(s1[i]), prev[j] + substitute(s1[i], s2[j]), row[row.length - 1] + insert(s2[j])),
      )
    }
    table.push(row)
    prev = row
  }
  return table
}
export function featureDistance(dst: Phoneme, src: Phoneme): number {
  let total = 0
  for (let d in dst) {
    if (d in src && (dst as any)[d] !== (src as any)[d]) {
      // Note: The Python code, incorrectly I believe, uses 1 here, because it
      // counts each shared feature with a different value *twice*, at 0.5 each.
      // I think 0.5 makes more sense, though.
      total += 0.5
    } else if (!(d in src)) {
      total += 1
    }
  }
  for (let s in src) {
    if (!(s in dst)) {
      total += 1
    }
  }
  return total
}
export function flevenshtein(dst: Phoneme[], src: Phoneme[], averageDistance: number): Table {
  return _levenshtein(
    dst,
    src,
    averageDistance,
    _ => averageDistance,
    _ => averageDistance,
    featureDistance,
  )
}
export function levenshtein(dst: string, src: string): Table {
  return _levenshtein<unknown>(
    dst as unknown as string[], // use a cast instead of string.split("")
    src as unknown as string[],
    1,
    _ => 1,
    _ => 1,
    (c1, c2) => (c1 === c2 ? 0 : 2),
  )
}
export function optimal(table: Table): Array<[Operation, [number, number]]> {
  let path: Array<[Operation, [number, number]]> = []
  let i = table.length - 1
  let j = table[0].length - 1
  while (i !== 0 || j !== 0) {
    let del = -1
    let ins = -1
    if (i === 0) {
      // no more s1, so remaining operations must be inserts of s2
      for (let k = j - 1; k >= 0; k--) {
        path.push(["insert", [0, k]])
      }
      break
    } else {
      del = table[i - 1][j]
    }
    if (j === 0) {
      // no more s1, so remaining operations must be inserts of s2
      for (let k = i - 1; k >= 0; k--) {
        path.push(["delete", [k, 0]])
      }
      break
    } else {
      ins = table[i][j - 1]
    }
    let sub = table[i - 1][j - 1]
    let best = Math.min(del, sub, ins)
    if (best === sub) {
      i--
      j--
      path.push(["substitute", [i, j]])
    } else if (best === del) {
      i--
      path.push(["delete", [i, j]])
    } else {
      j--
      path.push(["insert", [i, j]])
    }
  }
  return path.reverse()
}
