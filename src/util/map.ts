export function except() {}
export function collapsePairs<T, U>(kvs: Array<[T, U]>): Map<T, U[]> {
  let map: Map<T, U[]> = new Map()
  for (const [k, v] of kvs) {
    let l = map.get(k)
    if (l) {
      l.push(v)
    } else {
      map.set(k, [v])
    }
  }
  return map
}
export function extract() {}
export function filterValues<V>(m: Record<string, V>, f: (v: V) => boolean): Record<string, V> {
  let out: Record<string, V> = {}
  for (let [k, v] of Object.entries(m)) {
    if (f(v)) {
      out[k] = v
    }
  }
  return out
}
export function map() {}
export function zipwithValues<T, U, V>(
  m1: Record<string, T>,
  m2: Record<string, U>,
  f: (t: T, u: U) => V,
): Record<string, V> {
  let out: Record<string, V> = {}
  for (let [k, v1] of Object.entries(m1)) {
    if (k in m2) out[k] = f(v1, m2[k])
  }
  return out
}
