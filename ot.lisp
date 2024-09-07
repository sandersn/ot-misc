(require 'util) (use-package :util)
(load "constraints.lisp")
(defun ot (i o faith mark) "as of yet just gives violations and repairs"
  (list (remove-if #[funcall _ i o] faith)       ; demote
        (filter #[when (funcall _ i) (not (funcall _ o))] mark))) ; promote
(defun sort-candidates (results)
  (loop while (cdr results)
       do (setf results (set-difference results (worst-candidates results)))
       finally (return (car results))))
(defun worst-candidates (results)
  (let* ((indices (gmap #[position "" _ :test-not #'string=] results))
         (worst (plateau (sort (remove nil (zip indices results) :key #'car)
                               #'< :key #'car)
                         :key #'car)))
    (*->*! worst (= (len worst) (len results)))))
(defun *->*! (results all?)
  (let* ((lens (for (index row) results (len (elt row index))))
         (n (if all? (apply #'min lens) 0)))
    (gmap (\\ ((index row) len)
      ; row[i] = "*" * (n+1) + "!" + "*" * (len(star)-n+1)
              (unless (and all? (= n len))
                (setf (elt row index) (strcat (make-str #\* (1+ n))
                                              "!"
                                              (make-str #\* (- len (1+ n)))))
                row))
          results lens)))
(defun plateau (l &key (key #'identity))
  (take-while #[eq (funcall key _) (funcall key (first l))] l))
(defun violation (i o cs)
  (for c cs
    (make-str #\* (if (memq c faith)
                      (funcall c i o)
                      (funcall c o)))))
(defun tableau (input os cs) "I heart short names. o=output, c=constraint"
  (let* ((vs (gmap #[violation input _ cs] os))
         (winner (sort-candidates vs)))
    (format nil
"\\begin{tabular}{|ll||~a} \\hline
  Input: & \\textipa{/~a/} ~{& ~a ~} \\\\ \\hline \\hline
~{ ~a
~} \\end{tabular}"
            (make-str "c|" (len cs))
            input
            (gmap #[closure->name _ constraintnames] cs)
            (for (o v number) (zip os vs (gmap #'code-char (iota (len os) 97)))
              (format nil "~a.~a & \\textipa{[~a]} ~{& ~a ~} \\\\ \\hline"
                      number (if (eq v winner) " $\\surd$" "") o v)))))
;;; utils ;;;
(declaim (inline strcat))
(defun strcat (&rest ss) ; many names in Common Lisp are outright ridiculous
  (apply #'concatenate 'string ss)) ; and should be permanently aliased.
(defun make-str (init size)
  (if (characterp init)
      (make-string size :initial-element init)
      (apply #'strcat (times init size)))) ; still likely inefficient
