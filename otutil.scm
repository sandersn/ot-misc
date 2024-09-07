(require (lib "all.ss" "util"))
(def (all-equal? l) ; or (def all-equal? (binary->n-ary equal?))
  (every (uncurry equal?) (window l 2))) ; or (def all-equal? (cur apply ==))
(def ((binary->n-ary test?) l) "NB doesn't produce (test? . l) but (test? l)"
  (every (uncurry test?) (window l 2)))
(def (bin-key f key)
  (lambda (one two) (f (key one) (key two))))
;; winner evaluation
(def (winner cs)
  (let/ec return
    (foldl (fn (start-col tab)
             (bind new (lset-difference equal? tab
                                        (worst-candidates tab start-col))
               (if (or (null? new) (nil-cdr? new))
                   (return new)
                   new)))
           cs
           (iota (len (car cs))))))
(def worst-vln (cur position-if non-zero?))
(def (worst-candidates tab start)
  (bind worst (plateau (sort (remove #f (zip
                                         (map [! worst-vln _ :start start] tab)
                                         tab)
                                     :key car)
                             (bin-key < car))
                       :key car)
    (remove-best worst (= (len worst) (len tab)))))
(def (remove-best results violation-on-all?) "(list (index * row)) -> (list (index * row))"
  (bind best (if violation-on-all?
                 (apply min (map (uncurry (flip ref)) results))
                 0)
    (map cadr (remove-if (\\ ((index row))
                           (= (ref row index) best))
                          results))))
(def (plateau l &key [key identity])
  (take-while [! eq? (key _) (key (first l))] l))
;;
(def (except l . xs) ; TODO:Should be generic over hashes (if it's not already)
  (foldl (fn (l x) (remove l x :count 1)) l xs))
(def (remove-n l n) "list*int->list--Remove just index n from l efficiently"
  (let loop ((l l) (i 0))
    (match l
      (() ())
      ((x . xs) (if (= i n)
                    xs
                    (cons x (loop xs (add1 i))))))))
(def (positions f l) "I though this would be a foldl of position, but it's not"
  (let loop ((start 0))
    (aif (position-if f l :start start)
         (cons _ (loop (add1 _)))
         '())))
(def (round-robin l) "Capture the x/(except x l) pattern"
  (let loop ((l l) (acc ()))
    (match l
      (() ())
      ((x . xs) (cons (list x (append acc xs)) (loop xs (cons x acc)))))))
(def (subsets l n)
  "(list a) -> (list (list a)) -- All order-independent subsets of l of
length n. Don't pass n=0; you'll get extraneous results, not ()"
  (cond
    ((< (len l) n) '())
    ((= 1 n) (map list l))
    ((nil-cdr? l) (list l))
    (else (append (map (cur cons (car l)) (subsets (cdr l) (sub1 n)))
                  (subsets (cdr l) n)))))
;;
(def (split-at n l)
  (list (subseq l 0 n) (subseq l n)))
(def (split x l &key (test eq?) (from-end #f))
  "a*(list a)->(list (list a))--split a l by item x inside it
uses position, not search, so it's not [a]*[a]->[[a]]
another possibiility would be (map [! position _ l] xs) in order to ape Python"
  (aif (and l (position x l :test test :from-end from-end))
       (bind (first rest) (split-at _ l)
         (cons first (split x (drop rest 1) :test test :from-end from-end)))
       (list l)))
(def (split-seq splits l)
  "[a]*[a]->[[a]] (instead of split, which is a*[a]->[[a]])
This definition looks inefficient and hackish and confusing. Not util-ready"
  (split splits l :test (flip find))) ;short tho
(def sum (cur apply +))
;;
(def (== . xs)
  (if (null? xs)
      #t
      (let ((base (car xs)))
        (let loop ((xs (cdr xs)))
          (match xs
            (() #t)
            ((x . xs) (and (equals? base x) (loop xs))))))))
(def /= (negate ==))
(def neq? (negate eq?))
(def nequal? (negate equal?))
(def nequals? (negate equals?))
(def none (negate some))
;;
(def (times x n)
  (list-of x (dummy <- n)))
(defgeneric (sort+ l > &key (key #f)))
(defmethod (sort+ (l <list>) > &key (key #f))
  (if key
      (sort l (fn (x y) (> (key x) (key y))))
      (sort l >)))
(defmethod (sort+ (s <string>) > &key (key #f))
  (if key
      (sort (as <list> s) (fn (x y) (> (key x) (key y))))
      (sort (as <list> s) >)))
;(def strcat (cur apply add))
(def (make-str init size)
  (if (char? init)
      (make-string size init)
      (apply add (times init size)))) ; still likely inefficient
