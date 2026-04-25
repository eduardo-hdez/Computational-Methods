#lang racket

#|
validate-strings.rkt
Author: Eduardo Hernández Alonso
|#

;; Gets the automaton transition list
(define get-transitions
  (lambda (automaton)
    (caddr automaton)))

;; Gets the automaton initial state
(define get-initial-state
  (lambda (automaton)
    (cadddr automaton)))

;; Gets the automaton accept-state list
(define get-accept-states
  (lambda (automaton)
    (car (cddddr automaton))))

;; Finds the next state from the current state and symbol
(define find-next-state
  (lambda (transitions state symbol)
    (cond
      ((null? transitions) #f)
      ((and (equal? (car (car transitions)) state)
            (equal? (cadr (car transitions)) symbol))
       (caddr (car transitions)))
      (else (find-next-state (cdr transitions) state symbol)))))

;; Checks whether a state belongs to the accept-state list
(define is-accept-state
  (lambda (state accept-states)
    (cond
      ((null? accept-states) #f)
      ((equal? state (car accept-states)) #t)
      (else (is-accept-state state (cdr accept-states))))))

;; Traverses the automaton with an input sequence.
;; Returns the final state or #f if there is no transition.
(define process-string
  (lambda (automaton current-state input)
    (cond
      ((null? input) current-state)
      ((equal? (find-next-state (get-transitions automaton) current-state (car input)) #f) #f)
      (else (process-string automaton
                          (find-next-state (get-transitions automaton) current-state (car input))
                          (cdr input))))))

;; Returns #t if the final state is an accept state.
;; Returns #f if it is not an accept state.
(define check-final-state
  (lambda (final-state accept-states)
    (cond
      ((equal? final-state #f) #f)
      (else (is-accept-state final-state accept-states)))))

;; Checks a single input sequence against the automaton
(define validate-string
  (lambda (automaton input)
    (check-final-state
     (process-string automaton (get-initial-state automaton) input)
     (get-accept-states automaton))))

;; Main: validates a list of input strings.
(define validate
  (lambda (automaton strings)
    (cond
      ((null? strings) '())
      (else (cons (validate-string automaton (car strings))
                (validate automaton (cdr strings)))))))