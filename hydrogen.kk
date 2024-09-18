module hydrogen
import std/os/env
import std/os/file
import std/os/path
import types
import map
import sexp
import rcd
import list
// TODO: Write a real Map I guess
// TODO: Hydrogen is older, or different, than some of the CSV files I have. The one that works with it is Korean.csv
//  (however, it only uses the first row of constraints)
fun bcd(columns: list<column>)
  columns.map(fn (col) col.violations.map(show).join()).unlines()
fun lfcd(columns: list<column>)
  columns.map(fn (col) col.violations.map(show).join()).unlines()
fun gla(columns: list<column>)
  columns.map(fn (col) col.violations.map(show).join()).unlines()
val methods = [
  ("rcd", rcd),
  // ("bcd", bcd),
  // ("lfcd", lfcd),
  // ("gla", gla)
]
// TODO: These constraints aren't actually used because RCD et al used pre-evaluated tableaux
// that must be provided in the data file.
pub val idasp = Constraint("Ident (asp)", fn (input, output) 0)
pub val idvoice = Constraint("Ident (voice)", fn (input, output) 0)
pub val idasp/v = Constraint("Ident (asp)/_V", fn (input, output) 0)
pub val idvoice/v = Constraint("Ident (voice)/_V", fn (input, output) 0)
pub val no-pvmvpv = Constraint("*[+v][-v][+v]", fn (input, output) 0)
pub val no-dh = Constraint("*dh", fn (input, output) 0)
pub val no-voiceobs = Constraint("*[-son/+voice]", fn (input, output) 0)
pub val no-asp = Constraint("*aspiration", fn (input, output) 0)
val constraints: map<string, constraint> = [
  ("Ident (asp)", idasp),
  ("Ident (voice)", idvoice),
  ("Ident (asp)/_V", idasp/v),
  ("Ident (voice)/_V", idvoice/v),
  ("*[+v][-v][+v]", no-pvmvpv),
  ("*dh", no-dh),
  ("*[-son/+voice]", no-voiceobs),
  ("*aspiration", no-asp),
]
fun span-all(l : list<a>, predicate: a -> e bool) : e list<list<a>>
  fun span-acc(xs, acc, group)
    match xs
      Cons(x,xx) -> if predicate(x) 
                      then span-acc(xx, Cons(group.reverse,acc), [x]) 
                      else span-acc(xx, acc, Cons(x,group))
      Nil -> Cons(group.reverse, acc).reverse
  span-acc(l, [], [])
fun isMoreSpecific(title1: string, title2: string)
  title1 != title2 && title1.contains(title2)

fun title-to-column(titles : list<string>)
  val columns = titles.map fn (title)
    match constraints.assoc(title)
      Just(constraint) -> constraint
      Nothing -> throw("Exception in title-to-column: '" ++ title ++ "' is not a valid constraint")
  columns
fun specificityAll(titles: list<string>)
  // TODO: Call this separately for lfcd
  titles.filter-map fn (title)
    match (constraints.find(fn ((k,_)) isMoreSpecific(k, title)), constraints.assoc(title))
      (Just((_,general)), Just(specific)) -> Just ((general, specific))
      _ -> Nothing
fun parse-violation(vln : string) : exn int
  match vln.trim
    "" -> 0
    v -> match v.parse-int
           Just(n) -> n
           Nothing -> throw("Violation must be a number or blank.")
pub fun abs-to-relative(tableau : list<list<string>>) : exn list<list<int>>
  val violations = tableau.map fn (line) line.drop(2).map(parse-violation)
  val (winners, rivals) = violations.partition fn (line) line.head.default(0) > 0
  val winner = winners.head.unjust.drop(1)
  rivals.map(fn (rival) zipwith(rival.drop(1), winner, fn (r,w) r - w))
pub fun read-csv(filename : string) : <console/console,div,fsys,exn> list<column>
  // TODO: Might need to special-case GLA when that's ready
  val contents = filename.path.read-text-file
  val csv : csv = contents.lines.map(fn(x) { x.split(",") }).init
  match csv.span-all(fn (line) { line.head.default("") != "" })
    Cons(titles, tableaux) -> 
      val constraints = title-to-column(titles.head.default([]).drop(3))
      println(tableaux)
      val columns = tableaux.flatmap(abs-to-relative).transpose
      // TODO: the last entry is [] but shouldn't have been parsed
      // println(tableaux.flatmap(abs-to-relative))
      zipwith(constraints, columns, Column)
    Nil -> throw("Bad table format")
pub fun read-sexp(filename: string): <pure, fsys> list<column>
  fun readConstraint(k: sexp): exn int
    match k
      Atom(Int(i)) -> i
      _ -> throw("Bad table format")
  fun readColumn(k: constraint, col: sexp): exn column
    match col
      List(violations) -> Column(k, violations.map(readConstraint))
      _ -> throw("Bad table format")
  match sexp/read(filename.path.read-text-file)
   List(columns) -> zipwith(constraints.map fn ((_,k)) k, columns, readColumn)
   Atom(_) -> throw("Bad table format")
fun write-text(contents : string, filename : string) : <fsys,exn> ()
  write-text-file(filename.path, contents)
pub fun main()
  println("Hydrogen port")
  val args: list<string> = get-args()
  args.foreach(println)
  val method = rcd
  val infile = args.head.default("ot_learning/Korean.csv")
  val outfile = "test.csv"
  write-text(method(read-csv(infile)).show, outfile)
