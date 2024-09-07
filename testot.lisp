;;; features ;;;
(test 'feat-value-k1 (feat-value #\k 'cons) '+)
(test 'feat-value-k2 (feat-value #\k 'place) 'dorsal)
(test 'equal-feature?-k/p (funcall (equal-feature? 'cons) #\k #\p) t)
(test 'equal-feature?-k/p (funcall (equal-feature? 'place) #\k #\p) nil)
(test 'feat=val?-k+ (funcall (feat=val? 'cons '+) #\k) t)
(test 'feat=val?-k- (funcall (feat=val? 'cons 'i) #\k) nil)
(test 'feat=val?-k-place (funcall (feat=val? 'place 'dorsal) #\k) t)
(test 'feat=val?-p-place (funcall (feat=val? 'place 'dorsal) #\p) nil)
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
;; no-coda
(test 'icc-no-coda0 (no-coda "foo") 0)
(test 'icc-no-coda1 (no-coda "foobar") 1)
(test 'icc-no-coda-syllable1 (no-coda "foo.bar") 1)
(test 'icc-no-coda-still-only-1 (no-coda "foo.bard") 1)
(test 'icc-no-coda-syllable2 (no-coda "foon.bar") 2)
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