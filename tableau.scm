(require (lib "all.ss" "util"))
(load "otutil.scm")
(load "constraints.scm")
;;; tableau ;;;
(def (sort-candidates! results)
  (until (nil-cdr? results)
   (set! results (lset-difference equal? results (worst-candidates! results))))
  (car results))
(def (worst-candidates! results)
  (let* ((indices (map [! position "" _ :test-not string=?] results))
         (worst (plateau (sort+ (remove #f (zip indices results) :key car)
                               < :key car)
                         :key car)))
    (*->*! worst (= (len worst) (len results)))))
(def (*->*! results all?)
  (let* ((lens (for (index row) results (len (ref row index))))
         (n (if all? (apply min lens) 0)))
    (map (\\ ((index row) len)
      ; row[i] = "*" * (n+1) + "!" + "*" * (len(star)-n+1)
              (unless (and all? (= n len))
                (set! (ref row index) (add (make-str #\* (add1 n))
                                           "!"
                                           (make-str #\* (- len (add1 n)))))
                row))
          results lens)))
(def (plateau l &key (key identity))
  (take-while [! eq? (key _) (key (first l))] l))
(def (violation i o cs)
  (for c cs
    (make-str #\* (if (memq c faith)
                      (c i o)
                      (c o)))))
(def (tableau input os cs) "I heart short names. o=output, c=constraint"
  (let* ((vs (map [! violation input _ cs] os))
         (winner (sort-candidates! vs)))
    (echos "\\begin{figure}{(?)}

\\begin{tabular}{|ll||" : (make-str "c|" (len cs)) : "} \\hline" :n
           "Input: & \\textipa{/" : input : "/}"
           :\{ "&" (constraintnames cs) :\}
           "\\\\ \\hline \\hline" :n
           :\{ (for (o v number) (zip os vs (map [! as <char> _]
                                                 (iota (len os) 97)))
                 (echos number : "." (if (eq? v winner) "$\\surd$" "")
                        "& \\textipa{[" : o : "]}" :\{ "& " v :\}))
               "\\\\ \\hline" :n :\}
           "\\end{tabular}
\\end{figure}" :n)))
