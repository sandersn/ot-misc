OT
--
There are four files:
ot.scm - Simple OT learning
  Using the simplified explanation in Kager, which converges
  recursively on the ranking instead of using dynamic
  programming. This is slower, and each iteration of the convergence
  algorithm must examine all potential outputs forms, but it seems to
  work fine on the the two examples I tried.
  Also, GEN is badly faked. Next I'm planning to read some of the original
  sources and implement the dynamic programming algorithm along with a
  real GEN.
tableau.scm - LaTeX formatting of tableaux
  Given an input form, potential output forms, and a constraint
  ranking, tableau will return a properly formatted LaTeX table with
  violations and the winner marked. Right now ordering must be
  absolute; you have to change the columns to dotted afterwards.
constraints.scm - constraints
  Markedness constraints take a string and return an integer
    indicating the number of violations.
  Faithfulness constraints take two strings, input and output and
    return an integer indicating the number of violations.
  It should be easy to write your own. Note that some of the
  constraints are horrible hacks that only worked for the homework
  problems in the 642. That's why some of the tests fail.
plus
testot.scm - unit tests for most of the code (some of the utilities
were copied from Common Lisp where they were already tested)

The easiest way to make sure the code works is to do
ot$ swindle
> (load "testot.scm")
An impressive array of passing tests (mostly of constraints) will scroll
past. The tableau formatting and constraint-rank learning algorithms
have only a couple of tests at the bottom.

Reading the tests is also the best way to find out how to use the code.

Requirements:
Swindle - in /Applications/PLT Scheme v301/bin/swindle
scmutil.zip - from http://www.sandersn.com/scmutil.zip
              Unzip and drop into ~/Library/PLT Scheme/301/collects
(Note to self: util must also include arc.ss, which at this point
means the easiest way will be to zip the directories

NOTE:The current version is written in Scheme. Older Common Lisp and
Python versions are present in the zip file, and updating them to
match the current version would be trivial since the Scheme code uses
libraries very close to
Common Lisp. (Well, maybe not so trivial for Python until you rewrite
the Common Lisp sequence functions)
