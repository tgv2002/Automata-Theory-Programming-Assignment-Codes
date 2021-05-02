import sys
import json
from itertools import *

dfa_states = []
dfa_letters = []
dfa_transition_function = []
dfa_start_states = []
dfa_final_states = []
epsilon_transition_graph = {}
visited_states = []

def get_final_states(dfa_states, nfa_final_states):
    global dfa_final_states
    for dfa_state in dfa_states:
        found_a_final_state = False
        for nfa_state in dfa_state:
            if nfa_state in nfa_final_states:
                found_a_final_state = True
                break
        if found_a_final_state:
            dfa_final_states.append(dfa_state)

def constructEpsilonTransitionGraph(nfa_states, nfa_transition_function):
    global epsilon_transition_graph
    for nfa_state in nfa_states:
        epsilon_transition_graph[nfa_state] = []
    for nfa_transition in nfa_transition_function:
        if nfa_transition[1] == '$':
            epsilon_transition_graph[nfa_transition[0]].append(nfa_transition[2])

def dfs(curr_nfa_state):
    global epsilon_transition_graph
    global visited_states
    visited_states.append(curr_nfa_state)
    for to_state in epsilon_transition_graph[curr_nfa_state]:
        if to_state not in visited_states:
            dfs(to_state)

def allEpsilonTransitionsFromState(curr_state):
    global visited_states
    visited_states = []
    for nfa_state in curr_state:
        if nfa_state not in visited_states:
            dfs(nfa_state)
    all_epsilon_transitions = visited_states
    return all_epsilon_transitions

def obtain_transition_function(nfa_transition_function, dfa_states, nfa_letters):
    global dfa_transition_function
    nfa_transitions = {}
    for nfa_transition in nfa_transition_function:
        nfa_transitions[nfa_transition[0] + '#' + nfa_transition[1]] = []
    for nfa_transition in nfa_transition_function:
        nfa_transitions[nfa_transition[0] + '#' + nfa_transition[1]].append(nfa_transition[2])
    for dfa_state in dfa_states:
        for nfa_letter in nfa_letters:
            to_state = []
            for nfa_state in dfa_state:
                if nfa_state + '#' + nfa_letter in nfa_transitions.keys():
                    possible_to_state = allEpsilonTransitionsFromState(nfa_transitions[nfa_state + '#' + nfa_letter])
                    to_state = list(set().union(to_state, possible_to_state))
            dfa_transition_function.append([dfa_state, nfa_letter, to_state])
                            
input_path = str(sys.argv[1])
output_path = str(sys.argv[2])
NFA = {}
with open(input_path) as f:
    NFA = json.load(f)
nfa_states, nfa_letters, nfa_transition_function, nfa_start_states, nfa_final_states = NFA["states"], NFA["letters"], NFA["transition_function"], NFA["start_states"], NFA["final_states"]
dfa_letters = nfa_letters
dfa_states = list(map(list, chain.from_iterable(combinations(nfa_states, r) for r in range(len(nfa_states) + 1))))
get_final_states(dfa_states, nfa_final_states)
constructEpsilonTransitionGraph(nfa_states, nfa_transition_function)
dfa_start_states.append(allEpsilonTransitionsFromState(nfa_start_states))
obtain_transition_function(nfa_transition_function, dfa_states, nfa_letters)

DFA = {
    "states": dfa_states,
    "letters": dfa_letters,
    "transition_function": dfa_transition_function,
    "start_states": dfa_start_states,
    "final_states": dfa_final_states
}

with open(output_path, "w") as f:
    json.dump(DFA, f, indent=4)