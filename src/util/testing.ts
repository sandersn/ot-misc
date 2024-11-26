import { suite, test } from 'node:test'
import assert, { deepEqual as equal, fail } from "node:assert"
import type { Stress, StressMark, Syllable, Foot } from '../types.ts'
export function testall(suiteName: string, testo: Record<string, () => void>) {
  suite(suiteName, () => {
    for (let [name, f] of Object.entries(testo)) {
      test(name, f)
    }
  })
}

export function qw(s: string): string[] {
  return s.split(/\s+/)
}
