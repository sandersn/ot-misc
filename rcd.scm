;;; rcd.scm --- Recursive constraint demotion
(require (lib "all.ss" "util"))
;; utils
(require (lib "trace.ss"))
; this is the largest number of macros I've written in a long time
(defsubst (trace-lambda name args body ...)
  (let ((name (lambda args body ...)))
    (trace name)
    name))
(defsubst (def-traced (name args ...) body ...)
  (begin
    (def (name args ...) body ...)
    (trace name)))
(def (traced f)
  (trace-lambda traced args (apply f args)))
(defsubst (debug x) ; fancier formatting later (eg (display 'x ': x))
  (begin
    (display x) (newline)
    x))
(def (max-by f l &key (test >))
  (let loop ((best (car l)) (best-val (f (car l))) (l (cdr l)))
    (match l
      (() best)
      ((x . xs) (bind val (f x)
                  (if (test val best-val)
                      (loop x val xs)
                      (loop best best-val xs)))))))
(def (plateau l &key [key identity])
  (take-while [! eq? (key _) (key (first l))] l))
(def (filter/proxy f proxy l)
  (reverse (let loop ((proxy proxy) (l l) (acc ()))
             (cond
               ((null? proxy) acc)
               ((f (car proxy)) (loop (cdr proxy) (cdr l) (cons (car l) acc)))
               (else (loop (cdr proxy) (cdr l) acc))))))
(def (concat ls) (foldr append '() ls)) ; this wasn't defined..oops
(def (bin-key f key)
  (lambda (one two) (f (key one) (key two))))
;; to be moved to the OT lib
(def (mark? c)
  (== 1 (procedure-arity c)))
(def (ot-eval c input output)
  (if (mark? c)
      (c output)
      (c input output)))
;;; code (common)
;; NOTE: It turns out that null? promote and null? demote mean different
;; things. One means success and the other failure. I can't remember which,
;; but it is labelled clearly in Hayes' code (and papers).
(def (rcd-table cands constraints input)
  (for c constraints
    (cons c (for (w l) cands
              (- (ot-eval c l input) (ot-eval c w input))))))
(def win-fav? (cur some positive?)) ; TODO:Make sure this doesn't break rcd/bcd
(def inactive? (cur every zero?))
(def lose-disfav? (cur none negative?))
(def (add-stratum promote rest)
  (cons (map car promote) rest))
(def (filter-rows promote demote)
  "Keep the rows in demote that are inactive (empty) in promote"
  (bind (titles . rows) (unzip demote)
    (unzip (cons titles
                 (filter/proxy inactive? (cdr (unzip promote)) rows)))))
;; column faked-record code
(def col-marked? (compose mark? car))
(def col-active? (compose win-fav? cdr))
;;; rcd code -- Tesar & Smolensky 1993 or so
(def (rcd cols)
  (bind (promote demote) (bifilter (compose lose-disfav? cdr) cols)
    (if (or (null? promote) (null? demote))
        (add-stratum cols '())
        (add-stratum promote (rcd (filter-rows promote demote))))))
;;; bcd code -- Prince & Tesar 2001
(def (bcd cols &opt (speculative? #f) (prev #f) (acc '()))
  (with (acc (if prev (add-stratum prev acc) acc)
         cols (if prev (filter-rows prev cols) cols))
    (bind (promote demote) (bifilter (compose lose-disfav? cdr) cols)
      (if (null? promote)
          (reverse (add-stratum demote acc)) ;crshhh heh eheh
          (bind (m f) (bifilter col-marked? promote)
            (cond
              ((pair? m) (bcd (add f demote) speculative? m acc))
              ((null? demote) (reverse (add-stratum promote acc)))
              ;"continue BCD forward until a faithfulness must be placed"
              (speculative? (reverse acc))
              ((some col-active? promote)
               (bind x (min-subset (filter col-active? promote) cols)
                 (bcd (add demote (lset-difference (bin-key eq? car) promote x))
                      #f x acc)))
              (else (bcd demote #f promote acc))))))))
(def (min-subset actives cols)
   "except we would really really like this whole mess to be lazy
or at least eager to quit, because there is massive work going on"
  (best-set (find-if pair? (for i (iota (len cols) 1)
                             (filter [! frees-mark? _ cols]
                                     (subsets actives i))))
            cols))
(def (best-set sets cols)
  ":test >= favours the later constraint when picking among equally good ones,
to match OTSoft. This is not strictly
necessary, but makes it a lot easier to compare test results"
  (if (nil-cdr? sets)
      (car sets)
      (max-by [! count-if mark? (concat (bcd (filter-rows _ cols) #t))] sets
              :test >=)))
(def (frees-mark? set cols)
  (some (\\ ((title . col)) (and (mark? title) (win-fav? col)))
        (filter-rows set cols)))
;;; lfcd (from Hayes 2001)
(def (lfcd cols specificity)
  (bind (promote demote) (favour cols (compose lose-disfav? cdr)
                                       col-marked?
                                       col-active?
                                       (cur specific? cols specificity)
                                       (cur autonomous? cols))
    (if (or (null? promote) (null? demote))
       (add-stratum cols '())
       (add-stratum promote (lfcd (filter-rows promote demote) specificity)))))
(def (favour cols . prins)
  (letrec ((loop (\\ (cols (prin . ps))
                  (if (null? ps) ; special-case the last one by allowing it to
                      (prin cols) ; classify all the remaining columns
                      (bind (pass fail) (bifilter prin cols)
                        (cond                        ; #$@$# special cases!
                          ((and (eq? prin col-active?) (null? pass)) fail)
                          ((null? pass) (loop fail ps))
                           ; second clause special-cases col-marked?. UGH.
                          ((or (nil-cdr? pass) (eq? prin col-marked?)) pass)
                          (else (loop pass ps)))))))
         (promote (loop cols prins)))
    (list promote (lset-difference (bin-key eq? car) cols promote))))
(def (specific? cols specificity col)
  (aif (ref specificity (car col) (thunk #f))
       (member _ (map car cols))
       _))
(def most-helpers (cur count-if positive?))
(def (autonomous? cols rest)
  (bind rows (unzip (map cdr cols))
    ;a lot of this prevarication seems unnecessary. rewrite!
    ; the problem is that I zip up a bunch of temporary structure that carries
        ; information but is must ultimately be stripped away. so i'm keying
        ; into all this structure to avoid throwing any of it away.
    (map car (plateau (sort (for col rest
                              (cons col (max-by most-helpers
                                                (filter/proxy positive?
                                                              (cdr col)
                                                              rows)
                                                :test <)))
                            (bin-key < (compose most-helpers cdr)))
                      :key cdr))))
;;; GLA (Boersma primarily) ;;;
(gla (map [! cons _ 100]
          '(onset *complex-onset *syll#?C *coda *?coda max-? max-V
                  linearity id-io-syllabic max-oo? dep? id-br-syllabic
                  max-br *low-glide align-stemL-syllL contiguity id-io-low
                  id-br-long))
     tabs
     '((7000 2 10)
       (7000 0.2 2)
       (7000 0.2 0.2)))
;TODO:Random should pull from a normal distro, not a uniform one
(def (gla con tabs schedule)
  (foldl (fn (sch con) (gla* con tabs . sch)) con schedule))
(def (gla* con tabs n plasticity noise)
  (dotimes (i n)
    (with (tab (random-choice tabs)
           neo (perturb con noise))
      (with (possible (winner (unzip (map cadr (sort (zip neo
                                                          (cdr (unzip tab)))
                                                     (bin-key > cdar)))))
             actual (cdr (random-choice (filter car tab))))
        (unless (memq actual possible)
          (set! con (correct neo (map - (car possible) actual) plasticity))))))
  con)
(def (correct con w/l/d plasticity)
  (map (\\ ((c . score) direction)
        (cons c (+ score (* (sgn direction) plasticity))))
       con w/l/d))
(def (sgn n) "I bet this is defined and I just don't know the name"
  (cond ((< n 0) -1)
        ((= n 0) 0)
        (else 1)))
(def (perturb con noise)
  (map (\\ ((c . score)) (cons c (+ score (* noise (+ (random) -0.5))))) con))
'((id-br-long . 13861.084940840672)
 (*low-glide . 4891.343646625345)
 (contiguity . 4618.215541365377)
 (id-io-low . 2466.9513330199147)
 (align-stemL-syllL . 1909.1072719795256)
 (*syll#?C . 125.43703329598425)
 (onset . 123.13229291190832)
 (max-V . -69.78994684184264)
 (max-oo? . -163.9453896442951)
 (linearity . -704.7369508499343)
 (id-br-syllabic . -1092.0271041594613)
 (*?coda . -1139.1550533610484)
 (max-br . -1730.3742442767264)
 (dep? . -2180.8463197794717)
 (max-? . -2529.1529347516107)
 (*complex-onset . -3782.078298905986)
 (id-io-syllabic . -4710.988136070451)
 (*coda . -13639.194562283246))
'((onset . 123.13229291190832)
 (*complex-onset . -3782.078298905986)
 (*syll#?C . 125.43703329598425)
 (*coda . -13639.194562283246)
 (*?coda . -1139.1550533610484)
 (max-? . -2529.1529347516107)
 (max-V . -69.78994684184264)
 (linearity . -704.7369508499343)
 (id-io-syllabic . -4710.988136070451)
 (max-oo? . -163.9453896442951)
 (dep? . -2180.8463197794717)
 (id-br-syllabic . -1092.0271041594613)
 (max-br . -1730.3742442767264)
 (*low-glide . 4891.343646625345)
 (align-stemL-syllL . 1909.1072719795256)
 (contiguity . 4618.215541365377)
 (id-io-low . 2466.9513330199147)
 (id-br-long . 13861.084940840672))
; TODO:I updated keywords to be white instead of bold.
; The new version of Aquamacs installs its own SLIME, which will clobber
; the interaction customisation I made. But it was buggy. Save the changes anyw
; they changed C-n and C-p BACK to next-line/previous-line while this version
; uses visual-line-down/visual-line-up. I sort of prefer the classic way, but
; I'd like to be able to switch back and forth.
;;; scribbles from Prince 2002
(def (data->comparative winner tab) "convert absolute violations to W/L/blank"
  (map [! map - winner _] tab))
(def (comparative->display tab) "display with nice W/L/-"
  (for row tab
    (for vln row
      (case (sgn vln)
        ((1) 'W)
        ((-1) 'L)
        ((0) '-)))))
#|
'(((W - - - L) ; cost-us wins
  (W W L - -))
 ((L - - - W) ; cos-t-us wins
  (- W L - W))
 ((- L W - L) ;cos-tus wins
  (L L W - -)))
(((W - - - L) ;cost-me
  (- - L - -))
 ((L - - - W) ;cos-t-me
  (L - L - W))
 ((W - W - L) ;cos-tme
  (- - W - -)))
(((W - - L L)) ;cost
 ((L - - W W))) ;cos-t
((((cost-us (W - - - L)
            (W W L - -)) ; fuse= W W L _ L
   ((cost-me (W - - - L)
             (- - L - -)) ; fuse=W _ L _ L (link created by cost-us > cost-me?)
    (cost (W - - L L)))) ; fuse=W _ _ L L ..they are no way related...
  ((cos-t-us (L - - - W) ;fuse=L W L _ W
             (- W L - W))
   ((cos-t-me (L - - - W) ;fase=L _ L _ W (link created by cos-t-us > cos-t-me)
              (L - L - W))))
  ((cos-tus (- L W - L) ;cos-tus wins
           (L L W - -)) ;fuse=L L W _ L .. apparently cost-tus > nil
   ()))
 (((cost-me (W - - - L) ;cost-me
            (- - L - -))    ; fuse=W _ L _ L
   ((cost (W - - L L))))) ; fuse=W _ _ L L .. no relation
 :
 (((cost (W - - L L)) ())))
;so really map data->comparative over round-robin tabs produces the same
; when comparing sameset rows. Because you just get a row of - - - - - that
;contributes nothing. So.
; the problem now is that I can't figure out why you'd add one but not the
; other. Fusing doesn't seem to be the answer. Maybe some kind of ranking
; argument? Will this make some variant of factorial typology still more
; efficient?
; I might be able to find something by looking in the comparative system
; at why some other constraints don't gain any edges.
;---here are some other patterns---
'((cost-us ((- W - - -) ;cost-me  O <--hmmm
           (W W - - L) ;cos t me X
           (- W L - -)) ;cos tme X
          ((- W - - -) ;cost  O <-- does not contain any Ls
           (W W - L L)));cos t X
 (cos-t-us ((L W - - W) ;cost me  O <-- still no Ls
            (- W - - -) ;cos t me X
            (L W L - W));cos tme  X
           ((L W - - W)  ;cost  X
            (- W - L -)));cos t X
 (cos-tus ((L - W - -) ; X
           (- - W - L) ; X
           (L - - - -)); X
          ((L - W - -) ; X
           (- - W L L)));X
 (cost-me ((- L - - -) ; cost us  X
           (W L - - L) ; cos t us X
           (W - L - -)); cos tus  X
          ((- - - - -) ; cost  O
           (W - - L L)));cos t X
 (cos-t-me ((L L - - W) ; X
            (- L - - -) ; X
            (- - L - W)); X
           ((L - - - W) ; X
            (- - - L -)));X
 (cos-tme ((- L W - -) ; cos-tme is harmonically bounded by cost-me
           (W L W - L)
           (W - - - -)); should link to cos-tus
          ((- - W - -) ; should link to cost
           (W - W L L)))
 (cost ((- L - - -) ; cost us X
        (W L - - L) ; cos t us X
        (W - L - -)) ; cos tus X
       ((- - - - -) ; cost me O :(
        (W - - - L) ; cos t me X
        (- - L - -))); cos tme X <-- does an all-L line indicate boundedness?
 (cos-t ((L L - W W) ; X
         (- L - W -) ; X
         (- - L W W)); X
        ((L - - W W) ; X
         (- - - W -) ; cos-t-me O
         (L - L W W)))); X
'(((cost-us   1 1 0 0 0)
  (cos-t-us  0 1 0 0 1)
  (cos-tus   0 0 1 0 0))
 ((cost-me   1 0 0 0 0)
  (cos-t-me  0 0 0 0 1)
  (cos-tme   1 0 1 0 0))
 ((cost      1 0 0 0 0)
  (cos-t     0 0 0 1 1)))
|#