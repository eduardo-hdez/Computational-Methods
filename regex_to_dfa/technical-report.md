# Technical Report: Regex to DFA Conversion

## Introduction

This project implements in Python the conversion of a regular expression to a deterministic finite automaton (DFA) through four stages:

1. Explicit insertion of the concatenation operator.
2. Conversion from infix to postfix notation using the shunting yard algorithm.
3. Construction of an NFA using Thompson's algorithm.
4. Conversion from NFA to DFA using the subset construction algorithm.

The program receives a regular expression and an alphabet, and produces as output the equivalent DFA with its respective states and transitions.

## Proposed Solution

As stated above, my solution divides the problem into four linked stages, where each one transforms the previous representation into something closer to execution. This approach allows each module to be independent and testable.

The most relevant design decision was representing the DFA states as `frozenset` of NFA states. A `frozenset` is an immutable and hashable set in Python, which allows it to be used directly as a dictionary key to store transitions and as an element of a set to track already-visited states without the need for auxiliary mapping structures. Each DFA state is therefore a subset of NFA states, which reflects the use of the subset construction algorithm in the solution.

## Implemented Algorithms

**`add_concat`** traverses the expression a single time and inserts the `.` operator between each pair of adjacent characters where concatenation is implicit.

**`shunting_yard`** applies Dijkstra's algorithm with an operator stack and an output queue. It respects the precedence of the five operators (`*`, `+`, `?`, `.`, `|`) and produces a postfix expression where the evaluation order is predetermined.

**`build_nfa`** evaluates the postfix expression with a fragment stack applying Thompson's construction. Each operand creates a two-state fragment, binary operators consume two fragments and produce one, and unary operators consume one and produce one. Upon completion, the stack contains exactly the complete NFA.

**`nfa_to_dfa`** applies the subset construction algorithm. Each DFA state is the ε-closure of a set of NFA states. For each unprocessed state and each symbol of the alphabet, it computes the reachable states using move + epsilon_closure, adding new states to the queue until no unexplored states remain.

## Asymptotic Complexity

The first three stages operate in O(n) time and space, where n is the length of the regular expression. `add_concat` and `shunting_yard` perform a single pass over the input, processing each character exactly once. `build_nfa` is also O(n) because Thompson's construction generates two states per symbol of the expression.

The most expensive stage is `nfa_to_dfa` with complexity O(D · |Σ| · n), since the subset construction algorithm iterates over each DFA state (D), for each symbol of the alphabet (|Σ|), and executes move and epsilon_closure, each with a cost of O(n). In the worst case, D can reach 2^n, since each DFA state represents a subset of NFA states.

## Use of Generative AI

Generative AI was used as a support tool during the development of this project. Development was limited to the topics covered in the class. The use of this tool represented a change in the way problems are solved, as it was possible to obtain clear explanations and detect errors efficiently.

## Bibliographic References

_"McNaughton-Yamada-Thompson algorithm"_. (2021). Rosetta Code. https://rosettacode.org/wiki/McNaughton-Yamada-Thompson_algorithm

_"Shunting yard algorithm."_ (2024). Wikipedia. https://en.wikipedia.org/wiki/Shunting_yard_algorithm
