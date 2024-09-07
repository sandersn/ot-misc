(require (lib "all.ss" "util"))
(load "otutil.scm")
;;; code ;;;
;; Note: c is a candidate's violations, row also includes the name
;; tab is a tableau (list of candidates)
;; tabs is a list of tableaux

;; simple wrappers
(def title car)
(def violations cdr)
(def superset (cur every >=))
(def sameset (cur every =))
(def non-zero? (compose not zero?))
(def worst-vln (cur position-if non-zero?))
(def vlns (cur positions non-zero?))
;; macro :: table->(list table) in row major format
(defsubst (with-columns (cols table) e es ...)
  (map unzip (with (cols (unzip table)) e es ...)))
;; common code
#|(def (loses? n cs) "Does candidate n lose among the candidates?"
     ;TODO:Use a modification of winner (below) instead for correctness.
  (bind worst (worst-vln (ref cs n))
    (some [! > (worst-vln _) worst] (remove-n cs n)))) |#
(def (loses? n cs)
  (bind c (ref cs n)
    (let/cc return
      (foldl (fn (start-col tab)
               (let* ((worst (worst-candidates tab start-col))
                      (new (lset-difference equal? tab worst)))
                 (cond
                   ((memq c worst) (return #t))
                   ((nil-cdr? new) (return #f))
                   (else new))))
           cs
           (iota (len (car cs)))))))
(def (worst-candidates tab start)
  (bind worst (plateau (sort (remove #f (zip
                                         (map [! worst-vln _ :start start] tab)
                                         tab)
                                     :key car)
                             (keyed-test < car))
                       :key car)
    (remove-best worst (= (len worst) (len tab)))))
(def (remove-best results violation-on-all?) "(list (index * row)) -> (list (index * row))"
  (bind best (if violation-on-all?
                 (apply min (map (uncurry (flip ref)) results))
                 0)
    (map cadr (remove-if (\\ ((index row))
                           (= (ref row index) best))
                          results))))
(def (keyed-test test key)
  (fn (x y) (test (key x) (key y))))
(def (plateau l &key [key identity])
  (take-while [! eq? (key _) (key (first l))] l))

(def (unbounded tabs) "Remove all harmonically bounded candidates"
  (for tab tabs
    (remove-if (\\ (row)
                (some [! superset (violations row) (violations _)]
                      (except tab row)))
               tab)))
;;; third draft ;;;
(def (factorial/constraint l f)
  (cond
    ((null? l) '())
    ((nil-cdr? l) (if (f (car l) '()) '() (list l)))
    (else (mappend (\\ ((x rest))
                    (if (f x rest)
                        '()
                        (map (cur cons x) (factorial/constraint rest f))))
                   (round-robin l)))))
(def ((unused? rest) l) "are all the items in l still unused in rest?"
  (== l (lset-intersection eq? l rest)))
(def (factorial/winner winner tab othertab) "Memoisation slows things a bit"
     ;NB:There are still duplicate candidates generated if there are
     ; non-unique columns eg of all 0s or even both of (0 0 1 0).
     ; trimming these out *might* increase performance even more.
  (with-columns (cols othertab)
    (with (w         (map (cur ref cols) (vlns winner))
           ls (map [! map (cur ref cols) (vlns      _)] tab))
      (factorial/constraint
       cols (fn (x rest) (and (memq x w) (some (unused? rest) ls)))))))
(def (edges2 c hometab othertab)
  "Oddly, lifting the factorial/winner out HURTS performance on a small sample.
Likely because it only gets evaluated as needed otherwise."
  (display '|.|)
  (filter [! with (col-n (position _ othertab)
                   vs (violations _))
             (if (sameset c vs)
                 (none (cur loses? col-n)
                       (factorial/winner c
                                         (map violations hometab)
                                         (map violations othertab)))
                 (superset c vs))]
          othertab))
(def (t-order2 tabs) "Generates only winners to eliminate edges of
identical sets."
  (for (tab rest) (round-robin (unbounded tabs))
      (map (\\ (((name . c) rest-rows))
            `(,name ,(map title (mappend (cur edges2 c rest-rows) rest))))
           (round-robin tab))))
(def (make-tabs sets con) "Oh. That was easy."
  (for (input cands) sets
    (for name cands
      `(,name ,(map (fn (c name) (ot-eval c input name)) con cands)))))
#| (t-order2 (make-tabs '((cost-us (cost-us cos-t-us cos-tus))
                       (cost-me (cost-me cos-t-me cos-tmu))
                       (cost (cost cos-t)))
                     (list *- )) |#