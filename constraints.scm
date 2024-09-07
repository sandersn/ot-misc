(require (lib "all.ss" "util"))
(load "otutil.scm")
;;; features ;;;
(def *features* (read-file "features.sexp"))
(def *vowels* "aiueo@") ; oops, should be (filter vowel? *features*)
(def (feat-value c name)
  (aif (assoc (as <string> c) *features*)
       (aif (assq name (cdr _))
            (cdr _) _)
       _))
(def ((equal-feature? f) c1 c2)
  (eq? (feat-value c1 f) (feat-value c2 f)))
(def ((feat=val? f val) c)
  (eq? val (feat-value c f)))
(def vowel? (feat=val? 'cons '-))
(def cns? (feat=val? 'cons '+))
(def syllabify (cur split #\.))
(def ignore-syllables (cur remove #\.))
(def ignore-stress (cur remove #\'))
(def clusterify (add (cur split-seq *vowels*) ignore-syllables))
;;; mark ;;;
(def (*unvc-obs w)
  (count-if [! and (eq? '- (feat-value _ 'voice))
                   (eq? '- (feat-value _ 'contin))]
            w))
(def ((ICC f) w)
  (count-if-not [! (binary->n-ary (equal-feature? f)) (as <list> _)]
                (clusterify w)))
  ;[! all (equal-feature? f) (as <list> _)] (clusterify w)))
(def icc-vc (ICC 'voice))
(def icc-cont (ICC 'contin))
(def icc-place (ICC 'place))
(def (onset w)
  (count-if vowel? (syllabify w) :key [! ref _ 0]))
(def *.VC onset) ; another name for it?..
(def (no-coda w)
  (count-if cns? (syllabify w) :key [! ref _ (sub1 (len _))]))
(def (*complex w) "no complex margins"
  (count-if [! some [! > (len _) 1] (split-seq *vowels* _)] (syllabify w)))
(def (*trimoraic w)
  (max 0 (sum (for syll (syllabify w)
                (- (len (drop-while cns? syll)) 2)))))
(def (*cor-cor w)
  (count-if (\\ ((x y))
             (== 'coronal (feat-value x 'place) (feat-value y 'place)))
            (window (as <list> w) 2)))
(def (*gem w)
  (count-if (add all-equal? (cur as <list>))
            (filter [! > (len _) 1] (clusterify w))))
(def (*long-vowel w) ; "t" isn't special, just needed something [+cons]
  (count-if [! > (len _) 1] (split "t" (ignore-syllables w)
                                 :test (equal-feature? 'cons))))
(def (son-seq<en> w)
  (letrec ((son-seq '(("aiueoAIU@" . 4); Dan Friedman told me never to do this
                      ("jwrl" . 3) ; (put a data structure into a letrec)
                      ;("rl" . 3) ; also this data structure requires the
                      ("nmN" . 2) ; weird (find ... :test find) code below
                      ("fvszTDSZ" . 1) ; ..kind of annoying since I never
                      ("pbtdkg" . 0))) ; overloaded assoc to take keywords
           (onset-coda (fn (s) (bind chunks (clusterify s)
                                 (list (first chunks) (last chunks)))))
           (son (fn (c) (cdr (find c son-seq :key car :test find))))
           (sonority-ok? (fn (s onset?)
                           (if (< (len s) 2)
                               #t
                               (apply (if onset? < >)
                                      (map son (as <list> s)))))))
    (bind (onsets codas) (unzip (map onset-coda (syllabify w)))
      (+ (count-if-not [! sonority-ok? _ #t] onsets)
         (count-if-not [! sonority-ok? _ #f] codas)))))
(def (stress-to-weight w) ; yes, this one is fake
  (sum (for s (syllabify w)
         (if (and (find #\' s) (vowel? (ref s (sub1 (len s)))))
             1
             0))))
;;; faith ;;;
(def (levenshtein s1 s2) "this is a fairly efficient scheme definition
  but it is mightily confusing since it constructs a backward, upside down
  table. BUT the final result can be read off as (caar table).
  I say 'fairly' because the iteration would be better if lazy (at least zip) "
  (letrec ((delete (fn (_) 1))
           (subst (fn (c1 c2) (if (== c1 c2) 0 2)))
           (insert (fn (_) 1))
           (s1-list (as <list> s1)) ; sops to typing and efficiency x-x
           (s2-list (as <list> s2)))
    (foldl (\\ ((c1 i) table)
            (cons (foldl (\\ ((c2 (sub del)) row)
                          (cons (min (+ (delete c1) del)
                                     (+ (subst c1 c2) sub)
                                     (+ (insert c2) (car row))) row))
                         (list (add1 i))
                         (zip s2-list (window (reverse (car table)) 2)))
                  table))
           (list (reverse (iota (add1 (len s2)))))
           (enumerate s1-list))))
(def (optimal table)
  "Optimal returns a list of dels,subs,ins, but maybe should return a list of
the path it took instead. I'm not sure.
I think doing so would make it much easier to turn this into a general
alignment tool. I'm not sure how to annotate it: just '(ins del sub sub sub) ?
But this may not cut it if I introduce feature structure."
  (let loop ((table table) (dels 0) (subs 0) (ins 0))
    (cond ; match is BORKEN. Or something.
      ((and (nil-cdr? table) (nil-cdr? (car table)))
       (list dels subs ins))
      ((nil-cdr? table) ; all the rest are inserts, so add them before the end
       (list dels subs (+ ins (sub1 (len (car table))))))
      ((nil-cdr? (car table)) ; all the rest are deletes
       (list (+ dels (sub1 (len table))) subs ins))
      (else (with (delt (caadr table)
                    subst (cadadr table)
                    inst (cadar table))
           (cond-of (min delt subst inst)
             ((cur = delt) (loop (cdr table) (add1 dels) subs ins))
             ((cur = subst) (loop (map cdr (cdr table)) dels (add1 subs) ins))
             ((cur = inst) (loop (map cdr table) dels subs (add1 ins)))))))))
(def (optimal2 table)
  "Optimal returns a list of actions it took, but it really needs to include
the indices or the characters or both (or feature structure?)"
  (let loop ((table table) (acc ()))
    (cond ; match is BORKEN. Or something.
      ((and (nil-cdr? table) (nil-cdr? (car table))) acc)
      ((nil-cdr? table) ; all the rest are inserts, so add them before the end
       (append (times 'ins (sub1 (len (car table)))) acc))
      ((nil-cdr? (car table)) ; all the rest are deletes
       (append (times 'del (sub (len table))) acc))
      (else (with (delt (caadr table)
                    subst (cadadr table)
                    inst (cadar table))
           (cond-of (min delt subst inst)
             ((cur = delt) (loop (cdr table) (cons 'del acc))
             ((cur = subst) (loop (map cdr (cdr table)) (cons 'sub acc)))
             ((cur = inst) (loop (map cdr table) (cons 'ins acc))))))))))
(def max-io (compose car optimal levenshtein))
(def dep-io (compose caddr optimal levenshtein))
(def (max-mora i o) (if (string=? i o) 1 0)) ; hokey hack!
(def ((DEP f) i o)
  (max 0 (- (f o) (f i))))
;(def dep-io (DEP len))
(def dep-cv
  (bind count-cv
      (fn (s)
        (count "CV" (window (map [! if (cns? _) #\C #\V] s) 2) :test string=?))
    (DEP count-cv)))
(def dep-P (DEP (cur count #\P)))
(def (linearity i o)
  (if (and (not (string=? i o))
           (equal? (sort (as <list> i) char<?) (sort (as <list> o) char<?)))
      1 0))
(def id-everything string=?)
(def ((ID x) i o)
  (count-if-not (uncurry (equal-feature? x))
                (zip (as <list> i) (as <list>  o))))
(def id-vc (ID 'voice))
(def id-cont (ID 'contin))
(def id-place (ID 'place))
(def id-son (ID 'son))
(def id-cons (ID 'cons))
;;; necessary (for now) cruft
(def closure->name (add cadr assq))
(def faithnames `((,max-io "Max")
                  (,max-mora "Max-Mora")
                  (,dep-io "Dep")
                  (,dep-P "Dep-\\textglotstop")
                  (,dep-cv "Dep-CV")
                  (,id-everything "ID")
                  (,id-vc "ID[vc]")
                  (,id-cont "ID[cont]")
                  (,id-place "ID[place]")
                  (,id-cons "ID[cons]")
                  (,id-son "ID[son]")
                  (,linearity "Linearity")))
(def marknames `((,*unvc-obs "*unvc-obs")
                 (,icc-vc "ICC[vc]")
                 (,icc-cont "ICC[cont]")
                 (,icc-place "ICC[place]")
                 (,no-coda "NoCoda")
                 (,*complex "*Complex")
                 (,*trimoraic "*$\\sigma_{\\mu\\mu\\mu}$")
                 (,*long-vowel "*Long-Vowel")
                 (,*.VC "*[$_\\sigma$ V")
                 (,onset "Onset")
                 (,*gem "*Gem")
                 (,son-seq<en> "Son-Seq<En>")
                 (,*cor-cor "*[cor][cor]")
                 (,stress-to-weight "Stress-to-Weight")))
(def constraints (append faithnames marknames))
(def constraintname [! closure->name _ constraints])
(def constraintnames (cur map constraintname))
(def faith (map first faithnames))
(def mark (map first marknames))
(def faith? (isin faith))
(def (run cs i o)
  (for c cs
    (if (faith? c)
        (c i o)
        (c o))))
