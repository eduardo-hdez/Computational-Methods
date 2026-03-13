"""
main.py
Author: Eduardo Hernández Alonso
"""

from add_concat import add_concat
from shunting_yard import shunting_yard
from nfa import build_nfa, print_nfa
from dfa import nfa_to_dfa, print_dfa


def main():
    input_alphabet = input("Enter the alphabet: ")
    input_regex = input("Enter a regex: ")

    concat = add_concat(input_regex)
    postfix = shunting_yard(concat)
    nfa = build_nfa(postfix)
    dfa_transitions, start, accept_states = nfa_to_dfa(nfa, input_alphabet)

    print("----RESULTS----")
    print(f"\nINPUT:\n{input_regex}")
    print_nfa(nfa)
    print_dfa(dfa_transitions, start, accept_states)

main()