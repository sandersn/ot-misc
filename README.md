OT
--

This is old OT code; it's when I first started writing code to model the things I was learning in class. I only have a separate README from the Scheme code, and I haven't copied over the darcs history, so the dates below are guessed from the last-edit timestamps in the filesystem.

## 2006 - Lisp

Very basic OT learning implementation, as far as I can tell. From skimming it, I see it has several missing dependencies.

- ot.lisp
- constraints.lisp
- testot.lisp

## 2006 - Scheme
There are four files:

### ot.scm - Simple OT learning:
  Using the simplified explanation in Kager, which converges
  recursively on the ranking instead of using dynamic
  programming. This is slower, and each iteration of the convergence
  algorithm must examine all potential outputs forms, but it seems to
  work fine on the the two examples I tried.
  Also, GEN is badly faked. Next I'm planning to read some of the original
  sources and implement the dynamic programming algorithm along with a
  real GEN.
### tableau.scm - LaTeX formatting of tableaux
  Given an input form, potential output forms, and a constraint
  ranking, tableau will return a properly formatted LaTeX table with
  violations and the winner marked. Right now ordering must be
  absolute; you have to change the columns to dotted afterwards.
#### constraints.scm - constraints
  Markedness constraints take a string and return an integer
    indicating the number of violations.
  Faithfulness constraints take two strings, input and output and
    return an integer indicating the number of violations.
  It should be easy to write your own. Note that some of the
  constraints are horrible hacks that only worked for the homework
  problems in the 642. That's why some of the tests fail.

plus
### testot.scm - unit tests for most of the code 
(some of the utilities were copied from Common Lisp where they were already tested)

The easiest way to make sure the code works is to do

```sh
ot$ swindle
> (load "testot.scm")
```

An impressive array of passing tests (mostly of constraints) will scroll
past. The tableau formatting and constraint-rank learning algorithms
have only a couple of tests at the bottom.

Reading the tests is also the best way to find out how to use the code.

Requirements:
- Swindle - in /Applications/PLT Scheme v301/bin/swindle
- scmutil.zip - from http://www.sandersn.com/scmutil.zip
              Unzip and drop into ~/Library/PLT Scheme/301/collects

(Note to self: util must also include arc.ss, which at this point
means the easiest way will be to zip the directories

NOTE:The current version is written in Scheme. Older Common Lisp and
Python versions are present in the zip file, and updating them to
match the current version would be trivial since the Scheme code uses
libraries very close to
Common Lisp. (Well, maybe not so trivial for Python until you rewrite
the Common Lisp sequence functions)

### 2024 Notes

I didn't find the contents of scmutil, but it seems to be largely a collection of aliases to make Scheme's syntax closer to Haskell's or Python's.

After the previous section was written, I proceeded to write two more files. I included them in this section because the time between them wasn't that great, and they're tested in testot.scm with everything else.

- rcd.scm - Recursive Constraint Demotion, plus variations
- torder.scm - T-Orders

## 2006 - Caml

I played around briefly with Caml and decided not to pursue it. Instead, I switched to Python, which I knew well already.

- rcd.ml - Recursive Constraint Demotion, part of it at least

## 2006 - Python

After the switch to Python, I called the suite of code I had written Hydrogen. I have no memory of why. Since I was back to writing Python, I included my personal utility library that I had been maintaining since 2004 or late 2003.

I have a snapshot of these files from October 2006, but the versions preserved here are the latest ones, some of which I kept editing all the way through 2008. Examples are rcd.py, torder.py and lev.py.

- hydrogen.py - import and run all the learning algorithms on test data
- ot_learning/ - The test data
- ot.py - building blocks for RCD and T-orders
- faith.py - faithfulness constraints
- mark.py - markedness constraints
- unifeat.py - map IPA to feature structure
- test_unifeat.py - tests for unifeat
- lev.py - levenshtein distance, *of course*
- sexp.py - an S-expression reader for Python

- rcd.py - Recursive Constraint Demotion
- bcd.py - Biased Constraint Demotion
- lfcd.py - Low-Faithfulness Constraint Demotion
- gla.py - Gradual Learning Algorithm

## 2007 - Python

- factorial.py - factorial typologies. See https://github.com/sandersn/ot-factorial
- torder.py - T-Orders

## 2007 - Caml

- constraints.ml
- features.ml
- lev.ml