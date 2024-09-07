(require (lib "all.ss" "util"))
(load "otutil.scm")
(load "constraints.scm")
;;; ot ;;;
(def (ot i opt cs)
  (converge (fn (H)
              (foldl (fn (subopt H) (demote H (evalu i opt subopt cs)))
                     H
                     (gen i opt)))
            (list cs)))
(def (evalu i opt subopt cs)
  (map [! map third _]
       (bifilter (\\ ((w l n)) (> w l))
                 (filter (\\ ((w l _)) (/= w l))
                         (zip (run cs i opt) (run cs i subopt) cs)))))
(def demote
  (\\ (H (wins loses))
   (if (null?  loses) ; no ranking argument
       H              ; so no change
       (bind (above below )             ;find first loser in H
           (split-at (add1 (position-if (fn (cs) (any (isin loses) cs)) H))
                     H)
         (bind found-wins () ;     then demote all wins to just below it if
           (append (for cs above     ;   they are not already below it
                     (push-all! (lset-intersection eq? wins cs) found-wins)
                     (lset-difference eq? cs found-wins))
                   (list (append found-wins (if (null? below) () (car below))))
                   (if (null? below) () (cdr below))))))))
(def (gen i o) ; obviously a fake
  (cdr (assoc (list i o) '((("foon" "foo") . ("food"))))))
;;; all types of crazy crap ;;;
(def (parse-syll s)
  (letrec ((cons? (feat=val? 'cons '+))
           (onset (\\ ((c . cs) acc sigmas)
                   ((if (cons? c) onset nucleus)
                    cs (cons c acc) sigmas)))
           (nucleus (\\ (s acc sigmas)
                     (match s
                       (() (add-syll acc sigmas))
                       ((c . cs) (if (cons? c)
                                     (coda s acc sigmas)
                                     (nucleus cs (cons c acc) sigmas))))))
           (coda (\\ (s acc sigmas)
                  (match s
                    (() (add-syll acc sigmas))
                    (s (bind (c cs) (split-at
                                     (max 0 (- (position-if (negate cons?) s) 2))
                                     s)
                         (onset cs () (add-syll (append c acc) sigmas)))))))
           (add-syll (\\ (acc sigmas)
                    (cons (as <string> (reverse acc)) sigmas))))
    (trace onset nucleus coda)
    (begin0
        (reverse (onset (as <list> s) () ()))
      (untrace onset nucleus coda)
      )))
(def (tesar-parse s)
  (letrec ((cons? (feat=val? 'cons '+))
           (start (\\ (s acc sigmas)
                   (match s
                     (() ())
                     ((c . cs) ((if (cons? c) onset nucleus)
                                cs (cons c acc) sigmas)))))
           (onset (\\ ((c . cs) acc sigmas)
                   (nucleus cs (cons c acc) sigmas)))
           (nucleus (\\ (s acc sigmas)
                     (match s
                       (() (add-syll acc sigmas))
                       ((c) ((if (cons? c) coda nucleus)
                              () (cons c acc) sigmas))
                       ((c d . cs)
                        (cond
                          ((and (cons? c) (cons? d))
                           (coda (cons d cs) (cons c acc) sigmas))
                          ((cons? c)
                           (onset (cons c (cons d cs)) () (add-syll acc sigmas)))
                          (else (nucleus (cons d cs) (cons c acc) sigmas)))))))
           (coda (\\ (s acc sigmas)
                  (match s
                    (() (add-syll acc sigmas))
                    ((c . cs) ((if (cons? c) onset nucleus)
                               cs (list c) (add-syll acc sigmas))))))
           (add-syll (\\ (acc sigmas)
                    (cons (as <string> (reverse acc)) sigmas))))
;    (trace start onset nucleus coda)
    (begin0
        (reverse (start (as <list> s) () ()))
;      (untrace start onset nucleus coda)
      )))
(test 'tesar-parse
      (list (tesar-parse "fodbar")
            (tesar-parse "foobar")
            (tesar-parse "fobar")
            (tesar-parse "foba"))
      '(("fod" "bar")
        ("foo" "bar")
        ("fo" "bar")
        ("fo" "ba")))
(def (parser input cs states)
  (bind row (converge (fn (row) (map min (map harmony overparse-op row)))
                      (cons (cons 0 "") (map < overparses)))
    (for i input ; this is subtlely wrong in that for doesn't allow you to see
      ; the previous row, meaning that I may have to resurrent map/prev. x_x
      ; (in other words underparse-op parse-ops and overparse-op don't have
      ; enough information to currently work)
      (converge (fn (row) (map min (map harmony overparses row)))
                (for s states
                  (apply min (harmony underparse) (map harmony parse-ops)))))))