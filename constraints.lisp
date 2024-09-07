;;; features ;;;
(defvar *features* (read-file "features.sexp")) ;NOTE:I ought to revise
; this to use the shorter input versions (like S for esh)
(defvar *vowels* "aiueo@")
(defun feat-value (c name) "str|char*name->value"
  (cdr (assq name (cdr (assoc (string c) *features* :test #'string=)))))
(defun equal-feature? (f)
  #'(lambda (c1 c2) (eq (feat-value c1 f) (feat-value c2 f))))
(defun feat=val? (f val)
  #'(lambda (c) (eq val (feat-value c f))))
;;; mark ;;;
;; Note: constraints should return the number of times they're violated,
;; with a minimum of zero. Current code crashes if given negative numbers.
;; Markedness constraints look only at the output (or input), while
;; Faithfulness constraints compare the input and output
(defun *unvc-obs (w) "what the name says"
  (count-if #[and (eq '- (feat-value _ 'voice))
                  (eq '- (feat-value _ 'contin))]
            w))
(defun ICC (f w) "feature*word->bool
Make sure consonant clusters all have feature f"
  (count-if-not #[all (equal-feature? f) (string->list _)] (clusterify w)))
(def icc-vc (cur #'ICC 'voice))
(def icc-cont (cur #'ICC 'contin))
(def icc-place (cur #'ICC 'place))
(def syllabify (cur #'split #\.))
(def ignore-syllables (cur #'remove #\.))
(def clusterify (compose (cur #'split-seq *vowels*) #'ignore-syllables))
(defun no-coda (w) "no consonants as the last element of the syllable"
  (count-if (feat=val? 'cons '+) (syllabify w) :key #[elt _ (1- (len _))]))
(defun *complex (w) "no complex margins"
  (count-if #[some #[> (len _) 1] (split-seq *vowels* _)] (syllabify w)))
(defun *trimoraic (w) "Mora count may not be correct for all languages"
  (max 0 (sum (for syll (syllabify w)
                (- (len (drop-while (feat=val? 'cons '+) syll)) 2)))))
(defun *gem (w) "no two identical adjacent segments"
  (count-if (compose #'all-equal? #'string->list)
            (filter #[> (len _ ) 1] (clusterify w))))
(defun *.VC (w) "no onset-less syllables"
  (count-if (feat=val? 'cons '-) (syllabify w) :key #[elt _ 0]))
(defun *long-vowel (w) "no two adjacent vowels"
  (count-if #[> (len _) 1] (split "t" (remove #\. w)
                                  :test (equal-feature? 'cons))))
;;; faith ;;;
(defun max-io (i o)
  "these two definitions of course gloss over alignment in saying that
  foo->oof doesn't violate max OR dep"
  (max 0 (- (len i) (len o))))
(defun max-mora (i o) (if (string= i o) 1 0)) ;; hokey hack!
(defun DEP (f i o)
  (max 0 (- (funcall f o) (funcall f i))))
(def dep-io (cur #'DEP #'len))
(flet ((count-cv (s)  ; I still don't trust this much.
         (count "CV" (window (gmap #[if (eq '+ (feat-value _ 'cons)) #\C #\V]
                                   s)
                             2) :test #'string=)))
  (def dep-cv (cur #'DEP #'count-cv)))
(def dep-P (cur #'DEP (cur #'count #\P)))
(defun linearity (i o) "NB This doesn't provide the right number of violations"
  (if (and (not (string= i o))
           (string= (sort (copy-seq i) #'char<) (sort (copy-seq o) #'char<)))
      1 0))
(def id-everything #'string=) ; Mostly Harmless
(defun ID (x i o) "doesn't account for misalignment" ; This works but is ugly!
  (count-if-not (uncurry (equal-feature? x))         ; ugly I say!
                (zip (string->list i) (string->list o))))
(def id-vc (cur #'ID 'voice))
(def id-cont (cur #'ID 'contin))
(def id-place (cur #'ID 'place))
; of course max and dep being violated raises hairy issues of phoneme alignment
; which I will not entertain yet. (probably through levenshtein distance)
;;; constraint access and formatting ;;;
(def closure->name (compose #'cadr #'assq))
(defvar faithnames `((,#'max-io "Max")
                     (,#'max-mora "Max-Mora")
                     (,#'dep-io "Dep")
                     (,#'dep-P "Dep-\\textglotstop")
                     (,#'dep-cv "Dep-CV")
                     (,#'id-everything "ID")
                     (,#'id-vc "ID[vc]")
                     (,#'id-cont "ID[cont]")
                     (,#'id-place "ID[place]")
                     (,#'linearity "Linearity")))
(defvar marknames `((,#'*unvc-obs "*unvc-obs")
                    (,#'icc-vc "ICC[vc]")
                    (,#'icc-cont "ICC[cont]")
                    (,#'icc-place "ICC[place]")
                    (,#'no-coda "NoCoda")
                    (,#'*complex "*Complex")
                    (,#'*trimoraic "*$\\sigma_{\\mu\\mu\\mu}$")
                    (,#'*long-vowel "*Long-Vowel")
                    (,#'*.VC "*[$_\\sigma$ V")
                    (,#'*gem "*Gem")))
(defvar constraintnames (append faithnames marknames))
(defvar faith (gmap #'first faithnames))
(defvar mark (gmap #'first marknames))
;;; utils ;;;
(defun split-seq (splits l)
  "[a]*[a]->[[a]] (instead of split, which is a*[a]->[[a]])
This definition looks inefficient and hackish and confusing. Not util-ready"
  (split splits l :test (flip #'find))) ;short tho
(defun string->list (s)
  "bleh. needed because apply in uncurry in all can't destructure strings, but
can destructure lists. I want my money back.
Also, if this is endemic, it might be nice to make ->list a generic function"
  (loop for c across s collect c))
