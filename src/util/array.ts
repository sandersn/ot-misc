export function partition<T>(l: T[], f: (x: T) => boolean): [T[], T[]] {
    let yes = []
    let no = []
    for (let x of l) {
        if (f(x)) {
            yes.push(x)
        } else {
            no.push(x)
        }
    }
    return [yes, no]
}
export function zip<T, U>(l1: T[], l2: U[]): Array<[T, U]> {
    let out = []
    for (let i = 0; i < l1.length; i++) {
        out.push([l1[i], l2[i]] as [T, U])
    }
    return out
}
export function zipWith<T, U, V>(l1: T[], l2: U[], f: (a: T, b: U) => V): V[] {
    let out = []
    for (let i = 0; i < l1.length; i++) {
        out.push(f(l1[i], l2[i]))
    }
    return out
}
export function transpose<T>(l: T[][]): T[][] {
    if (l.length == 0) {
        return []
    }
    let table: T[][] = []
    for (let i = 0; i < l[0].length; i++) {
        table.push([])
    }
    for (let row of l) {
        for (let i = 0; i < row.length; i++) {
            table[i].push(row[i])
        }
    }
    return table
}
export function filterProxy<T, U>(l: T[], proxy: U[], f: (x: U) => boolean): T[] {
    let out = []
    for (let i = 0; i < l.length; i++) {
        if (f(proxy[i])) {
            out.push(l[i])
        }
    }
    return out
}
/** pick indices *in the order presented* in `indices` */
export function pickIndices<T>(l: T[], indices: number[]): T[] {
    let out = []
    for (let i of indices) {
        out.push(l[i])
    }
    return out
}

export function sequence<T>(ls: T[][]): T[][] {
    if (ls.length == 0) {
        return [[]]
    } else {
        let [head, ...tail] = ls
        let rests = sequence(tail)
        let acc = []
        for (let x of head) {
            for (let rest of rests) {
                acc.push([x, ...rest])
            }
        }
        return acc
    }
}

export function count<T>(l: T[], f: (x: T) => boolean): number {
    let i = 0
    for (let x of l) {
        if (f(x)) {
            i++
        }
    }
    return i
}
