module sexp
import std/text/parse
import types
pub type atom
  Symbol(symbol: string)
  Int(i: int) 
  Bool(b: bool)
pub type sexp
  List(l: list<sexp>)
  Atom(a: atom)
pub fun atom/show(a: atom): string
  match a
    Symbol(s) -> s
    Int(i) -> i.show
    Bool(b) -> b.show
pub fun sexp/show(s: sexp): div string
  match s
    List(xs) -> "(" ++ xs.map(show).join(" ") ++ ")"
    Atom(a) -> show(a)

/**
 * 1. comments
 * 2. #t #f for bool
 * 3. symbols (following python identifier rules)
 * 4. positive and negative numbers
 * 5. proper lists (nested)
 * Not implemented: pairs or strings or top-level atoms
 */
pub fun read(s: string): <exn,div> sexp
  match s.slice.parse(parseToplevel)
    ParseError(msg, remnant) -> throw("parse error: '" ++ msg ++ "' at " ++ remnant.show)
    ParseOk(sexp, remnant) -> if (remnant.is-empty) then sexp else throw("didn't parse everything: " ++ remnant.show)
fun parseSexp(): <div,parse> sexp
  char('(')
  parseWhitespaceOrComment()
  val items = many
    val item = choose([parseSexp, parseAtom])
    parseWhitespaceOrComment()
    item
  char(')')
  List(items)
fun parseAtom(): parse sexp
  Atom(choose([parseSymbol, parseInt, parseBool]))
fun parseSymbol(): parse atom
  val c = alpha()
  val s = optional([],{ chars-are("alpha-num", is-alpha-num) }).string
  Symbol(c.string ++ s)
fun parseInt(): parse atom
  Int(pint())
fun parseBool(): parse atom
  char('#')
  val value = one-of("tf")
  Bool(if value == 't' then True else False)
fun parseWhitespaceOrComment(): parse ()
  whitespace0()
  optional(())
    char(';')
    many { none-of("\n") }
    char('\n')
    ()
  whitespace0()
  ()
fun parseToplevel(): <div,parse> sexp
  parseWhitespaceOrComment()
  val sexp = parseSexp()
  parseWhitespaceOrComment()
  eof()
  sexp


pub fun main()
  // val s = "((a 1 0 1 -1)\n; a comment\n(b 1 3 4 5))"
  val s = "((a 1 0 1 -1)\n; comment \n(b 1 3 4 5))"
  println(s.read.show)

