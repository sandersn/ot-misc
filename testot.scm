(load "constraints.scm")
(load "tableau.scm")
(load "ot.scm")
(load "rcd.scm")
(load "torder.scm")
;;; background stuff ;;;
(test 'split (split 2 '(1 2 3)) '((1) (3)))
(test 'split-nil (split 2 '( 3 4 5)) '((3 4 5)))
(test 'split-edges (split 2 '(2 1 2 1 2)) '(() (1) (1) ()))
(test 'split-testequal? (split 2 '(2 1 2 1 2) :test equal?) '(() (1) (1) ()))
(test 'split-test= (split 2 '(2 1 2 1 2) :test =) '(() (1) (1) ()))
(test 'split-test> (split 2 '(2 1 2 1 2) :test >) '((2) (2) (2)))
(test 'split-test-memq (split '(2) '(2 1 2 1 2) :test (flip memq)) '(() (1) (1) ()))
(test 'split-test-find (split '(2) '(2 1 2 1 2) :test (flip find)) '(() (1) (1) ()))
#|
emergence of the unmarked is just a split ranking between Faith-IO and
Faith-BR
this then means that reduplicants tend to have less marked structure since
Faith_BR are the ones ranked low
of course if you just have
/taga/
[tak-taga] means Markedness >> FaithIO,FaithBR
and overapplication is
FaithBR >> Mark
eg
/neyat/ -> [n~e~y~at]
with redup -> [~y~at-n~e~y~at]

|#
;;; features ;;;
(test 'feat-value-k1 (feat-value #\k 'cons) '+)
(test 'feat-value-k2 (feat-value #\k 'place) 'dorsal)
(test 'equal-feature?-k/p ((equal-feature? 'cons) #\k #\p) #t)
(test 'equal-feature?-k/p ( (equal-feature? 'place) #\k #\p) #f)
(test 'feat=val?-k+ ((feat=val? 'cons '+) #\k) #t)
(test 'feat=val?-k- ((feat=val? 'cons 'i) #\k) #f)
(test 'feat=val?-k-place ((feat=val? 'place 'dorsal) #\k) #t)
(test 'feat=val?-p-place ((feat=val? 'place 'dorsal) #\p) #f)
;;; mark ;;;
;; first, the utils
(test 'desyllabify (ignore-syllables "foo.bar.baz") "foobarbaz")
(test 'syllabify (syllabify "foo.bar.baz") '("foo" "bar" "baz"))
(test 'clusterify (clusterify "foobarbaz") '("f" "" "b" "rb" "z"))
(test 'clusterify-syllables (clusterify "foo.bar.baz") '("f" "" "b" "rb" "z"))
 ; the extra "" arises because of the long vowel, eg
(test 'clusterify-looong-vowel (clusterify "oooo") '("" "" "" "" ""))
 ; split-seq assumes short vowels and postulates a cluster of size zero in
 ; the middle of long vowels. Constraint code should word handle null strings.
 ; Or fix split-seq.
;; *unvc-obs
(test '*unvc-obs-fricative (*unvc-obs "foo") 0)
(test '*unvc-obs-vcobs (*unvc-obs "boo") 0)
(test '*unvc-obs-1 (*unvc-obs "poo") 1)
(test '*unvc-obs-2 (*unvc-obs "pot") 2)
(test '*unvc-obs-ignore-oorange (*unvc-obs "oo-sux") 0)
(test '*unvc-obs-ignore-space (*unvc-obs "oo sux") 0)
(test '*unvc-obs-ignore-syllable (*unvc-obs "oo.sux") 0)
;; ICC
(test 'icc-vc-mu (icc-vc "foo") 0)
(test 'icc-vc-african (icc-vc "bmako") 0)
(test 'icc-vc-stand-on-zanzibar (icc-vc "urbapt") 0) ;sucked. and was wrong.
(test 'icc-vc-homsar (icc-vc "homsar") 1)
(test 'icc-vc-syll-boundary-vcd (icc-vc "foo.bar") 0)
(test 'icc-vc-syll-boundary-vcls (icc-vc "foo.qux") 0)
(test 'icc-vc-syll-boundary-violation (icc-vc "bar.qux") 1)
(test 'icc-vc-massive (icc-vc "qxsrwerpty") 2)
(test 'icc-vc-more-massive (icc-vc "pgpoqxsrwerptyilkgm") 4)
(test 'icc-cont-mu (icc-cont "foo") 0)
(test 'icc-cont1 (icc-cont "pruv") 1)
(test 'icc-cont0 (icc-cont "fluvi@n") 0)
(test 'icc-place (icc-place "gruv") 1)
(test 'icc-place (icc-place "trov") 0)
;; onset
;(test 'onset-nil (onset "") 0) ;crashes, this is bad for the dynamic learner.
(test 'onset0 (onset "he.lo") 0) ; (other mark funcs will crash on this too)
(test 'onset1 (onset "e.lo") 1)
(test 'onset2 (onset "e.o") 2)
;; no-coda
(test 'no-coda0 (no-coda "foo") 0)
(test 'no-coda1 (no-coda "foobar") 1)
(test 'no-coda-syllable1 (no-coda "foo.bar") 1)
(test 'no-coda-still-only-1 (no-coda "foo.bard") 1)
(test 'no-coda-syllable2 (no-coda "foon.bar") 2)
;; *complex
(test '*complex0 (*complex "food") 0)
(test '*complex1 (*complex "bard") 1)
(test '*complex-syll0 (*complex "wom.bat") 0)
(test '*complex-bad-syllabification (*complex "wombat") 1)
;; trimoraic
(test '*trimoraic0 (*trimoraic "foo") 0)
(test '*trimoraic1 (*trimoraic "food") 1)
(test '*trimoraic-syll0 (*trimoraic "foo.bar") 0)
; note that final clusters get one mora per consonant. not sure this is correct
(test '*trimoraic-syll1 (*trimoraic "food.bard") 2)
(test '*trimoraic-cons (*trimoraic "asdfg") 3)
(test '*trimoraic-vw (*trimoraic "aaaaa") 3)
;; *cor-cor
(test '*cor-cor0 (*cor-cor "fjun") 0)
(test '*cor-cor1 (*cor-cor "tjun") 1)
(test '*cor-cor2 (*cor-cor "tjn") 2)
(test '*cor-cor-overdone (*cor-cor "ddd") 2)
;; *gem
(test '*gem0 (*gem "foo") 0)
(test '*gem-initial (*gem "ffoo") 1)
(test '*gem-medial (*gem "bokken") 1)
(test '*gem-medial-w/syllable (*gem "bok.ken") 1)
(test '*gem-final (*gem "bitt") 1)
(test '*gem-cons (*gem "dddd") 1) ; this is seen as one long geminate.
; this is not a geminate because two geminates together are not the same char
; since this articulation is impossible AFAIK I will not fix this test.
(test '*gem-cons (*gem "ddgg") 2)
(test '*gem-vc (*gem "ooo") 0)
;; *.VC
(test '*.VC0 (*.VC "foo") 0)
(test '*.VC1 (*.VC "abba") 1)
(test '*.VC1-syll (*.VC "ab.ba") 1)
(test '*.VC2 (*.VC "ab.ab") 2)
;; *long-vowel
(test '*long-vowel0 (*long-vowel "bar") 0)
(test '*long-vowel1 (*long-vowel "foo") 1)
(test '*long-vowel1 (*long-vowel "aaaa") 1) ; viewed as all one long vowel
; almost the same problem as *gem except this code is a little better
(test '*long-vowel2 (*long-vowel "aaoo") 2)
;;; faith ;;;
;; levenshtein distance
(test 'lev-simple-n (caar (levenshtein "art" "cat")) 2)
(test 'lev-simple-detail (levenshtein "art" "cat")
      '((2 3 4 3)
        (3 2 3 2)
        (2 1 2 1)
        (3 2 1 0)))
(test 'lev-same-n (caar (levenshtein "foo" "foo")) 0)
(test 'lev-same-detail (levenshtein "foo" "foo") '((0 1 2 3)
                                                   (1 0 1 2)
                                                   (2 1 0 1)
                                                   (3 2 1 0)))
(test 'lev-different (caar (levenshtein "abc" "sed")) 6)
(test 'lev-different (levenshtein "abc" "sed") '((6 5 4 3)
                                                 (5 4 3 2)
                                                 (4 3 2 1)
                                                 (3 2 1 0)))
(test 'lev-different-length (caar (levenshtein "woon" "rouen")) 5) ; Dave Barry
(test 'lev-different-length (levenshtein "woon" "rouen") '((5 6 5 4 5 4)
                                                           (6 5 4 3 4 3)
                                                           (5 4 3 2 3 2)
                                                           (6 5 4 3 2 1)
                                                           (5 4 3 2 1 0)))

;; max-io
(test 'max-io= (max-io "foo" "fo0") 0)
(test 'max-io/= (max-io "foo" "bar") 0)
(test 'max-io-shorter (max-io "foo" "fo") 1)
(test 'max-io-longer (max-io "foo" "fooo") 0)
(test 'max-io-nil-longer (max-io "" "fooo") 0)
(test 'max-io-nil-shorter (max-io "foo" "") 3)
(test 'max-io-nil-nil (max-io "" "") 0)
;; dep-io
(test 'dep-io= (dep-io "foo" "foo") 0)
(test 'dep-io/= (dep-io "foo" "bar") 0)
(test 'dep-io-shorter (dep-io "foo" "fo") 0)
(test 'dep-io-longer (dep-io "foo" "fooo") 1)
(test 'dep-io-nil-longer (dep-io "" "fooo") 4)
(test 'dep-io-nil-shorter (dep-io "foo" "") 0)
(test 'dep-io-nil-nil (dep-io "" "") 0)
;; dep-cv
(test 'dep-cv0 (dep-cv "bar" "bar") 0)
(test 'dep-cv1-redup (dep-cv "bar" "babar") 1)
(test 'dep-cv1-wtf (dep-cv "bar" "fubar") 1)
(test 'dep-cv0-not-cv (dep-cv "bar" "akbar") 0)
(test 'dep-cv1-extraneous (dep-cv "bar" "akabar") 1)
;; dep-P (P is the TIPA input symbol for glottal stop)
(test 'dep-P0 (dep-P "foo" "foo") 0)
(test 'dep-P1 (dep-P "foo" "fooP") 1)
(test 'dep-P0/max (dep-P "fooP" "foo") 0)
(test 'dep-P1 (dep-P "foo" "PPP") 3)
;; linearity
(test 'lin0 (linearity "foo" "foo") 0)
(test 'lin1 (linearity "foo" "oof") 1)
; should be detected by a proper algorithm eg levenshtein
(test 'lin2 (linearity "food" "ofdo") 2)
(test 'lin-all0 (linearity "ooo" "ooo") 0)
(test 'lin-mismatch (linearity "oo" "") 0)
(test 'lin-nil (linearity "" "") 0)
;; id-vc
(test 'id-vc0 (id-vc "foo" "foo") 0)
(test 'id-vc1 (id-vc "foo" "voo") 1)
(test 'id-vc-dvc1 (id-vc "voo" "foo") 1)
(test 'id-vc2 (id-vc "food" "voot") 2)
(test 'id-vc2-syll (id-vc "foo.bar" "voo.par") 2)
(test 'id-vc-mismatch-o (id-vc "foo" "vood") 1)
(test 'id-vc-mismatch-i (id-vc "foot" "voo") 1)
(test 'id-vc-align (id-vc "foo" "ofoo") 1)
(test 'id-vc-just (id-vc "foo" "too") 0)
;; id-cont (less testing here because the ID code is the same as id-vc)
(test 'id-cont0 (id-cont "foo" "foo") 0)
(test 'id-cont-just (id-cont "foo" "loo") 0)
(test 'id-cont1 (id-cont "foo" "poo") 1)
;; id-place
(test 'id-place0-just (id-place "foo" "voo") 0)
(test 'id-place1 (id-place "foo" "soo") 1)
;; id-everything is just string=. Not writing tests for that
;;; tableau ;;;
(test 'tableau-simple
      (tableau "foo" (list "food" "foon" "foo" "fo") (list max-io dep-io))
      "\\begin{figure}{(?)}

\\begin{tabular}{|ll||c|c|} \\hline
Input: & \\textipa{/foo/} & Max & Dep \\\\ \\hline \\hline
a.  & \\textipa{[food]} &   &  *! \\\\ \\hline
b.  & \\textipa{[foon]} &   &  *! \\\\ \\hline
c. $\\surd$ & \\textipa{[foo]} &   &   \\\\ \\hline
d.  & \\textipa{[fo]} &  *! &   \\\\ \\hline\n\\end{tabular}
\\end{figure}
")
;;; t-order ;;;
;; t-order utils
(test 'except (except '(1 2 3) 2) '(1 3))
(test 'except-miss (except '(1 2 3) 4) '(1 2 3))
(test 'remove-nil (except '() 4) '())

(test 'remove-n-1 (remove-n '(1 2 3) 1) '(1 3))
(test 'remove-n-0 (remove-n '(1 2 3) 0) '(2 3))
(test 'remove-n--1 (remove-n '(1 2 3) -1) '(1 2 3))
(test 'remove-n-oorange (remove-n '(1 2 3) 3) '(1 2 3))
(test 'remove-n-nil (remove-n '() 4) '())

(test 'superset (superset '(1 1 0 0 0) '(0 1 0 0 1)) #f)
(test 'superset-same (superset '(1 1 0 0 0) '(1 1 0 0 0)) #t)
(test 'superset-1s (superset '(1 0 1 0 0) '(0 0 1 0 0)) #t)
(test 'superset-1s-rev (superset '(0 0 0 1 0) '(0 0 0 1 1)) #f)

(test 'positions-medial (positions non-zero? '(0 0 1 0 0)) '(2))
(test 'positions-initial (positions non-zero? '(1 0 1 0 0)) '(0 2))
(test 'positions-final (positions non-zero? '(1 0 1 0 0 1)) '(0 2 5))
(test 'positions-empty (positions non-zero? '()) '())

(test 'round-robin (round-robin '(1 2 3 4))
      '((1 (2 3 4)) (2 (1 3 4)) (3 (2 1 4)) (4 (3 2 1))))

(bind x '((0 1 0 0 1)
          (0 0 1 0 0)
          (1 1 0 0 0))
;  (test 'wins-0 (wins? 0 x) #f)
;  (test 'wins-1 (wins? 1 x) #t)
;  (test 'wins-2 (wins? 2 x) #f)
;  (test 'wins-costme (wins? 0 '((0 0 0 1 0)
;                                (0 0 0 0 1))) #f)
;  (test 'wins-cost (wins? 0 '((0 0 0 1 0)
;                              (0 0 1 0 1))) #t)
  (test 'loses-0 (loses? 0 x) #t)
  (test 'loses-1 (loses? 1 x) #f)
  (test 'loses-2 (loses? 2 x) #t))
(test 'round-robin-nil (round-robin '()) '())
#|(bind x '((first row)
          (second row))
  (test 'fact (map unzip (factorial (unzip x))) '(((first row) (second row))
                                                  ((row first) (row second)))))
|#
(bind x '((0 1 0)
          (1 1 0)
          (0 0 1))
;  (test 'winner? (every (cur wins? 2) (factorial/winner (caddr x) x x)) #t)
  (test 'winners (factorial/winner (caddr x) x x) '(((0 1 0)
                                                     (1 1 0)
                                                     (0 0 1))
                                                    ((1 0 0)
                                                     (1 1 0)
                                                     (0 0 1))
                                                    ((1 0 0)
                                                     (1 0 1)
                                                     (0 1 0)))))
(bind skip '((0 1 1 0 0 1)
              (0 1 0 1 0 0))
  (test 'loses?-skip-0 (loses? 0 skip) #t)
  (test 'loses?-skip-1 (loses? 1 skip) #f)
  ; wins? fails because I haven't updated wins? to use the correct system
  ; and wins? is not used in my 3rd or 4th drafts of t-order.
  ;(test 'wins?-skip-0 (wins? 0 skip) #f)
  ;(test 'wins?-skip-1 (wins? 1 skip) #t)
  )
(test 'loses-index0 (loses? 0 '((0 0 0 1 0)
                                (1 0 0 0 1))) #f)
;; t-order proper
(def tabs '(((cost-us   1 1 0 0 0)
             (cos-t-us  0 1 0 0 1)
             (cos-tus   0 0 1 0 0))
            ((cost-me   1 0 0 0 0)
             (cos-t-me  0 0 0 0 1)
             (cos-tme   1 0 1 0 0))
            ((cost      1 0 0 0 0)
             (cos-t     0 0 0 1 1))))
(def answer '(((cost-us (cost-me cost))
               (cos-t-us (cos-t-me))
               (cos-tus ()))
              ((cost-me (cost))
               (cos-t-me ()))
              ((cost ())
               (cos-t (cos-t-me)))))
(test 'unbounded (unbounded tabs)
      '(((cost-us 1 1 0 0 0) (cos-t-us 0 1 0 0 1) (cos-tus 0 0 1 0 0))
        ((cost-me 1 0 0 0 0) (cos-t-me 0 0 0 0 1))
        ((cost 1 0 0 0 0) (cos-t 0 0 0 1 1))))
(test 't-order-third-draft (t-order2 tabs) answer)
(set! tabs '(((<po.lii><sei.ta>  1 0 1 1 1 2 0 0)
              (<po.lii>sei.ta    2 1 0 1 1 0 2 0)
              (<po.lii><se.ja>   1 0 1 1 1 2 0 1)
              (<po.lii>se.ja     1 0 0 1 2 0 2 1))
             ((<ka.me><lei.ta>   0 0 0 1 1 2 0 0)
              (<ka.me>lei.ta     1 1 0 1 1 0 2 0)
              (<ka.me><le.ja>    0 0 0 1 1 2 0 1)
              (<ka.me>le.ja      0 0 0 1 2 0 2 1))
             ((<kor.jaa><moi.ta> 1 0 1 1 1 2 0 0)
              (<kor.jaa>moi.ta   2 1 0 1 1 0 2 0)
              (<kor.jaa><mo.ja>  1 0 1 1 1 2 0 1)
              (<kor.jaa>mo.ja    1 0 0 2 2 0 2 1))
             ((<ka.me><roi.ta>   0 0 0 1 1 2 0 0)
              (<ka.me>roi.ta     1 1 0 1 1 0 2 0)
              (<ka.me><ro.ja>    0 0 0 1 1 2 0 1)
              (<ka.me>ro.ja      0 0 0 2 2 0 2 1))))
(set! tabs '(((<po.lii><sei.ta>  0 1 1 1 2 0 0)
              (<po.lii><se.ja>   0 1 1 1 2 0 1)
              (<po.lii>se.ja     0 0 1 2 0 2 1))
             ((<ka.me><lei.ta>   0 0 1 1 2 0 0)
              (<ka.me><le.ja>    0 0 1 1 2 0 1)
              (<ka.me>le.ja      0 0 1 2 0 2 1))
             ((<kor.jaa><moi.ta> 0 1 1 1 2 0 0)
              (<kor.jaa><mo.ja>  0 1 1 1 2 0 1)
              (<kor.jaa>mo.ja    0 0 2 2 0 2 1))
             ((<ka.me><roi.ta>   0 0 1 1 2 0 0)
              (<ka.me><ro.ja>    0 0 1 1 2 0 1)
              (<ka.me>ro.ja      0 0 2 2 0 2 1))))
(set! answer '(((<po.lii><sei.ta> (<ka.me><lei.ta> <kor.jaa><moi.ta> <ka.me><roi.ta>))
                (<po.lii>se.ja ()))
               ((<ka.me><lei.ta> (<ka.me><roi.ta>))
                (<ka.me>le.ja (<po.lii>se.ja)))
               ((<kor.jaa><moi.ta> (<ka.me><lei.ta> <ka.me><roi.ta>))
                (<kor.jaa>mo.ja (<ka.me>le.ja <po.lii>se.ja)))
               ((<ka.me><roi.ta> ())
                (<ka.me>ro.ja (<kor.jaa>mo.ja <ka.me>le.ja <po.lii>se.ja)))))
;(test 'more-complicated (t-order2 tabs) answer) ; hasn't run to completion yet
;;; rcd and bcd and lcfd ;;;
(letrec ((*low (lambda (o) (count #\a o)))
         (candidates '(("fo" "foo") ; blah blah bad practise, ugly; shut up k
                       ("fo" "fa")
                       ("fo" "f"))))
  (test 'fake/foo
        (rcd (rcd-table candidates (list max-io dep-io *low) "fo"))
        (list (list max-io dep-io *low))))
(letrec ((dep-init-sigma
          (lambda (i o)
            "I consider this pretty shady since it requires the input to be
syllabified"
            (if (== (car (syllabify i)) (subseq (car (syllabify o)) 1))
                1
                0))))
  (test 'dep-init-sigma (dep-init-sigma "oo.bar" "foo.bar") 1)
  (test 'McCarthy-Thematic-Guide-to-OT
        (rcd `((,max-io 0 1 0 1 1)
               (,dep-init-sigma 1 0 0 0 1)
               (,onset -1 -1 1 0 -1)
               (,dep-io 1 0 -1 -1 0)))
        (list (list dep-init-sigma max-io) (list onset) (list dep-io)))
  ; rcd-table fails miserably because of bad constraints
  ; I changed max-io and dep-io to use levenshtein optimal paths but it still
  ; fails. Must need to change others.
  (test 'rcd-table (rcd-table '(("in.ko.ma.ti" "tin.ko.ma.ti")
                                ("in.ko.ma.ti" "ko.ma.ti")
                                ("in.ko.ma.ti" "in.ko.ma.i")
                                ("in.ko.ma.ti" "in.ko.ma")
                                ("in.ko.ma.ti" "tin.ko.ma"))
                              (list dep-io dep-init-sigma onset max-io)
                              "in.ko.ma.i")
        `((,dep-io 1 0 -1 -1 0)
          (,dep-init-sigma 1 0 0 0 1)
          (,onset -1 -1 1 0 -1)
          (,max-io 0 1 0 1 1)))
  (test 'rcd-whole (rcd (rcd-table '(("in.ko.ma.ti" "tin.ko.ma.ti")
                                     ("in.ko.ma.ti" "ko.ma.ti")
                                     ("in.ko.ma.ti" "in.ko.ma.i")
                                     ("in.ko.ma.ti" "in.ko.ma")
                                     ("in.ko.ma.ti" "tin.ko.ma"))
                                   (list dep-io dep-init-sigma onset max-io)
                                   "in.ko.ma.i"))
        (list (list max-io dep-init-sigma) (list onset) (list dep-io)))
  (test 'bcd/McCarthy
        (bcd `((,max-io 0 1 0 1 1)
               (,dep-init-sigma 1 0 0 0 1)
               (,onset -1 -1 1 0 -1)
               (,dep-io 1 0 -1 -1 0)))
        ; I'm not sure this result is right
        (list (list max-io) (list dep-init-sigma) (list onset) (list dep-io)))
  (test 'lfcd/McCarthy
        (lfcd `((,max-io 0 1 0 1 1)
               (,dep-init-sigma 1 0 0 0 1)
               (,onset -1 -1 1 0 -1)
               (,dep-io 1 0 -1 -1 0))
              (make-hash '())) ; or this one.
        (list (list max-io) (list dep-init-sigma) (list onset) (list dep-io))))
(letrec ((id-asp (fn (i o)
                   (count-if (negate case=?)
                             (zip (as <list> i) (as <list> o)))))
         (id-asp/_v (fn (i o)
                      (count-if (\\ (((c1 v1) (c2 v2)))
                                 (and (not (case=? (list c1 c2)))
                                      (vowel? v1) (vowel? v2)))
                                (zip (window (as <list> i) 2)
                                     (window (as <list> o) 2)))))
         (id-vc (fn (i o)
                  (count-if (negate (uncurry char=?))
                            (zip (as <list> (map char-downcase i))
                                 (as <list> (map char-downcase o))))))
         (id-vc/_v
          (fn (i o)
            (count-if (\\ (((c1 v1) (c2 v2)))
                       (and (not (char=? c1 c2))
                            (vowel? v1) (vowel? v2)))
                      (zip (window (as <list> (map char-downcase i)) 2)
                           (window (as <list> (map char-downcase o)) 2)))))
         (*asp (fn (o) (count-if char-upper-case? o)))
         (*dh (fn (o) (count #\D o)))
         (*+v-v+v (fn (o)
                    (count-if (fn (s) (and (eq? #\t (ref s 1))
                                           (eq? #\a (ref s 0))
                                           (eq? #\a (ref s 2))))
                              (window (map char-downcase o) 3))))
         (*-son+vc (fn (o)
                     (count #\d (map char-downcase o))))
         (candidates '(("ta" "Ta" "da" "Da") ; here is the obligatory
                       ("Ta" "ta" "da" "Da") ; "Dan Friedman told me never
                       ("ada" "ata" "aTa" "aDa") ; to do this" comment.
                       ("aTa" "ata" "ada" "aDa")
                       ("at" "ad" "aT" "aD")
                       ("tada" "tata" "taTa" "taDa" "dada" "Tada" "Dada")
                       ("taTa" "tata" "tada" "taDa" "daTa" "DaTa" "TaTa")
                       ("Tada" "TaTa" "Tata" "TaDa" "tada" "dada" "Dada")
                       ("TaTa" "Tata" "Tada" "TaDa" "taTa" "daTa" "DaTa" "tata" "tada")
                       ("tat" "taT" "tad" "taD" "Tat" "dat" "Dat")
                       ("Tat" "Tad" "TaT" "TaD" "tat" "dat" "Dat")))
      (specificity (make-hash (list (cons id-vc/_v id-vc)
                                    (cons id-asp/_v id-asp))))
      (pseudo-korean (map cons (list id-asp id-vc id-asp/_v id-vc/_v
                                     *+v-v+v *dh *-son+vc *asp)
                          (read-file "ot_learning/pseudo-korean.sexp"))))
  (test 'rcd/Korean (time (rcd pseudo-korean))
        `((,*dh ,id-vc/_v ,id-asp/_v ,id-vc ,id-asp)
          (,*asp ,*-son+vc ,*+v-v+v)))
  (test 'bcd/Korean (time (bcd pseudo-korean)) `((,*dh)
                                          (,id-asp)
                                          (,*+v-v+v ,*asp)
                                          (,*-son+vc)
                                          (,id-vc ,id-asp/_v ,id-vc/_v)))
  (test 'lfcd/Korean (time (lfcd pseudo-korean specificity))
        (list (list *dh)
              (list id-asp/_v)
              (list *+v-v+v *asp)
              (list *-son+vc)
              (list id-asp id-vc id-vc/_v))))
#| This is not the Real Deal. This is the Square Deal.
 `((,*dh 0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 0 1 0 1 0 0 0 1 0 0 1 0 0 1 0 0 1 0 0 0 0 1 0 0 1 0 0 1 0 0 1)
                      (,*+v-v+v 0 0 0 0 0 0 1 1 0 0 -1 -1 0 0 0 1 1 0 0 0 0 0 -1 -1 0 0 0 1 1 0 0 0 0 0 -1 -1 0 0 0 0 -1 0 0 0 0 0 0 0 0 0 0 0 0)
                      (,*-son+vc 0 1 1 0 1 1 -1 -1 0 0 1 1 1 0 1 -1 -1 0 1 0 1 0 1 1 1 1 0 -1 -1 0 0 1 1 0 1 1 0 1 1 0 1 0 1 1 0 1 1 1 0 1 0 1 1)
                      (,*asp 1 0 1 -1 -1 0 0 1 1 -1 -1 0 0 1 1 0 1 1 0 1 1 -1 -1 0 0 1 1 1 0 1 -1 -1 0 -1 -1 0 -1 -1 0 -2 -2 1 0 1 1 0 1 0 1 1 -1 -1 0)
                      (,id-asp/_v 1 0 1 1 1 0 0 1 1 1 1 0 0 0 0 0 1 1 0 1 1 1 1 0 0 1 1 1 0 1 1 1 0 1 1 0 1 1 0 2 2 0 0 0 1 0 1 0 0 0 1 1 0)
                      (,id-asp 1 0 1 1 1 0 0 1 1 1 1 0 0 1 1 0 1 1 0 1 1 1 1 0 0 1 1 1 0 1 1 1 0 1 1 0 1 1 0 2 2 1 0 1 1 0 1 0 1 1 1 1 0)
                      (,id-vc/_v 0 1 1 0 1 1 1 1 0 0 1 1 0 0 0 1 1 0 1 0 1 0 1 1 1 1 0 1 1 0 0 1 1 0 1 1 0 1 1 0 1 0 0 0 0 1 1 0 0 0 0 1 1)
                      (,id-vc 0 1 1 0 1 1 1 1 0 0 1 1 1 0 1 1 1 0 1 0 1 0 1 1 1 1 0 1 1 0 0 1 1 0 1 1 0 1 1 0 1 0 1 1 0 1 1 1 0 1 0 1 1)) |#
;; TEMP generate violations for pseudo-korean test
#| (def (case=? cs)
  (eq? (char-lower-case? (ref cs 0)) (char-lower-case? (ref cs 1))))
(letrec 
  (unzip (cons '(*dh *+v-v+v *-son+vc *asp
                 id-asp/_v id-asp id-vc/_v id-vc)
       (forn tab candidates
         (bind abs (for cand tab
                     (map [! ot-eval _ (car tab) cand]
                          (list *dh *+v-v+v *-son+vc *asp          ; mark
                                id-asp/_v id-asp id-vc/_v id-vc))) ; faith
           (map [! map - _ (car abs)] (cdr abs))))))) |#