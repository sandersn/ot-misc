module rcd
import types
import list
fun tied(violations: list<int>): bool
  violations.all fn(v) v == 0

fun add-stratum(columns: columnar, constraints: strata): strata
  Cons(columns.map(fn (c) c.constraint), constraints)
fun violations-rows(table: columnar): div list<list<int>>
  table.map(violations).transpose
fun filter-proxy(l: list<a>, proxy: list<b>, f: b -> bool): list<a>
  zip(l,proxy).filter(fn ((_,p)) f(p)).map(fn ((x,_)) x)
fun always-zip(l1: list<a>, l2: list<list<b>>, ?(==): (b, b) -> bool): list<(a,list<b>)>
  if l2 == []
    then l1.map(fn (x) (x, []))
    else zip(l1, l2)
fun filter-demote-by-promote-rows(promote: columnar, demote: columnar): <div,console/console> columnar
  val hierarchy = demote.map(constraint)
  println(hierarchy)
  println(violations-rows(demote))
  println(violations-rows(promote))
  println(violations-rows(demote).filter-proxy(violations-rows(promote), tied))
  val filteredColumns = violations-rows(demote).filter-proxy(violations-rows(promote), tied).transpose
  always-zip(hierarchy, filteredColumns).map(fn ((a,b)) Column(a,b))
pub fun rcd(columns: list<column>): <div,console/console> list<list<constraint>>
  val (demote, promote) = columns.partition(fn (c) c.violations.any(fn (v) v < 0))
  println((promote.map(constraint), demote.map(constraint)))
  if promote == [] || demote == []
    then add-stratum(columns, [])
    else add-stratum(promote, rcd(filter-demote-by-promote-rows(promote, demote)))
