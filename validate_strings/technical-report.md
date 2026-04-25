# Technical Report: String Validation over an Automaton

## Introduction

This project implements in Racket the validation of input strings against a finite automaton. The program receives an automaton and a list of strings, and produces as output a list of boolean values indicating whether each string is accepted or rejected by the automaton.

## Proposed Solution

As stated above, my solution divides the problem into small linked functions: access to the automaton structure, transition lookup, recursive traversal of the input string, and validation of the final state. This decomposition keeps each part simple and testable.

The central idea is to process each string symbol by symbol from the initial state. For each symbol, the program searches for a matching transition from the current state; if no transition exists, the computation stops and the string is rejected. If all symbols are consumed, acceptance depends on whether the final state belongs to the automaton's set of accept states.

## Implemented Algorithms

**`get-transitions`**, **`get-initial-state`**, and **`get-accept-states`** extract the relevant automaton components using positional access over the list representation.

**`find-next-state`** recursively scans the transition list looking for a triple where the source state and input symbol match the current step. If no transition is found, it returns `#f` to indicate an invalid move.

**`is-accept-state`** recursively checks whether a state belongs to the accept-state list.

**`process-string`** is the core of the solution. It recursively consumes one symbol per call and advances to the next state using `find-next-state`. If any transition is missing, it returns `#f`; if the input is fully consumed, it returns the state reached at the end.

**`check-final-state`** evaluates the result of `process-string` and confirms whether the final state is an accept state.

**`validate-string`** combines `process-string` and `check-final-state` to validate one input string.

**`validate`** recursively applies `validate-string` over a list of strings and builds the output list of boolean results.

## Asymptotic Complexity

Let `n` be the length of one input string, `T` the number of transitions in the automaton, `A` the number of accept states, and `m` the number of input strings to validate.

`find-next-state` runs in O(T) in the worst case because it may traverse the entire transition list for one symbol.

`is-accept-state` runs in O(A) in the worst case because it may traverse the entire accept-state list.

`process-string` performs one transition lookup per input symbol, so its cost is O(n · T).

`check-final-state` calls `is-accept-state` once, so its cost is O(A).

`validate-string` executes `process-string` followed by `check-final-state`, resulting in O(n · T + A).

`validate` applies `validate-string` to `m` strings, giving a total complexity of O(m · (n · T + A)), where `n` is the average string length.

## Use of Generative AI

Generative AI was used as a support tool during the development of this project. Development was limited to the topics covered in class. The use of this tool represented a change in the way problems are solved, as it was possible to obtain clear explanations and detect errors efficiently.
