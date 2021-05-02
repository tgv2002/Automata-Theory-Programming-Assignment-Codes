import sys
import json

min_dfa_states = []
min_dfa_letters = []
min_dfa_transition_function = []
min_dfa_start_states = []
min_dfa_final_states = []
dfa_di_graph = {}
undir_graph = {}
reachable_states = []

def construct_undir_graph(dfa_states, dfa_final_states, dfa_transition_function, dfa_letters):
    global undir_graph
    undir_graph = {state: [] for state in dfa_states}
    delta_r_a = {r: {a: '' for a in dfa_letters} for r in dfa_states}
    edges_added = 0
    for final_state in dfa_final_states:
        for state in dfa_states:
            if state in dfa_final_states:
                continue
            if final_state not in undir_graph[state]:
                undir_graph[state].append(final_state)
                undir_graph[final_state].append(state)
                edges_added += 1
    prev_edges_added = edges_added
    for dfa_transition in dfa_transition_function:
        delta_r_a[dfa_transition[0]][dfa_transition[1]] = dfa_transition[2]
    while True:
        for state_1 in dfa_states:
            for state_2 in dfa_states:
                if state_1 == state_2:
                    continue
                for letter in dfa_letters:
                    u = delta_r_a[state_1][letter]
                    v = delta_r_a[state_2][letter]
                    if u == '' or v == '':
                        continue
                    if u in undir_graph[v] and state_1 not in undir_graph[state_2]:
                        edges_added += 1
                        undir_graph[state_1].append(state_2)
                        undir_graph[state_2].append(state_1)
        if prev_edges_added == edges_added:
            break
        prev_edges_added = edges_added
    
def get_new_states_collection(dfa_states):
    global undir_graph
    state_collection = {state: [] for state in dfa_states}
    for state_1 in dfa_states:
        for state_2 in dfa_states:
            if state_1 not in undir_graph[state_2]:
                state_collection[state_1].append(state_2)
                state_collection[state_2].append(state_1)
    for state in dfa_states:
        if state_collection[state]:
            state_collection[state] = list(set(state_collection[state]))
            state_collection[state].sort()
    return state_collection

def get_minimized_dfa(dfa_states, dfa_start_states, dfa_final_states, dfa_transition_function, dfa_letters):
    global min_dfa_states
    global min_dfa_transition_function
    global min_dfa_start_states
    global min_dfa_final_states
    state_collection = get_new_states_collection(dfa_states)
    all_states = []
    for state in dfa_states:
        all_states.append(state_collection[state])
    all_states = [list(new_state) for new_state in set(tuple(new_state) for new_state in all_states)]
    min_dfa_states = all_states
    min_dfa_start_states = state_collection[dfa_start_states[0]]
    min_dfa_final_states = [state_collection[final_state] for final_state in dfa_final_states]
    min_dfa_final_states = [list(new_state) for new_state in set(tuple(new_state) for new_state in min_dfa_final_states)]
    delta_r_a = {r: {a: '' for a in dfa_letters} for r in dfa_states}
    for dfa_transition in dfa_transition_function:
        delta_r_a[dfa_transition[0]][dfa_transition[1]] = dfa_transition[2]
    for dfa_state in dfa_states:
        for dfa_letter in dfa_letters:
            if delta_r_a[dfa_state][dfa_letter] in dfa_states and [state_collection[dfa_state], dfa_letter, state_collection[delta_r_a[dfa_state][dfa_letter]]] not in min_dfa_transition_function:
                min_dfa_transition_function.append([state_collection[dfa_state], dfa_letter, state_collection[delta_r_a[dfa_state][dfa_letter]]])
    
def construct_dfa_di_graph(dfa_transition_function, dfa_states):
    global dfa_di_graph
    dfa_di_graph = {state: [] for state in dfa_states}
    for dfa_transition in dfa_transition_function:
        u = dfa_transition[0]
        v = dfa_transition[2]
        dfa_di_graph[u].append(v)

def dfs(curr_dfa_state):
    global dfa_di_graph
    global reachable_states
    reachable_states.append(curr_dfa_state)
    for to_state in dfa_di_graph[curr_dfa_state]:
        if to_state not in reachable_states:
            dfs(to_state)
            
def remove_unreachable_states(dfa_states, dfa_transition_function, dfa_start_states, dfa_final_states):
    global reachable_states
    reachable_states = []
    dfs(dfa_start_states[0])
    dfa_states = reachable_states
    dfa_transition_function = [dfa_transition for dfa_transition in dfa_transition_function if dfa_transition[0] in reachable_states and dfa_transition[2] in reachable_states]
    dfa_final_states = [dfa_state for dfa_state in dfa_final_states if dfa_state in reachable_states]
    return dfa_states, dfa_transition_function, dfa_final_states

input_path = str(sys.argv[1])
output_path = str(sys.argv[2])
DFA = {}
with open(input_path) as f:
    DFA = json.load(f)
dfa_states, dfa_letters, dfa_transition_function, dfa_start_states, dfa_final_states = DFA["states"], DFA["letters"], DFA["transition_function"], DFA["start_states"], DFA["final_states"]

min_dfa_letters = dfa_letters
construct_dfa_di_graph(dfa_transition_function, dfa_states)
dfa_states, dfa_transition_function, dfa_final_states = remove_unreachable_states(dfa_states, dfa_transition_function, dfa_start_states, dfa_final_states)
construct_undir_graph(dfa_states, dfa_final_states, dfa_transition_function, dfa_letters)
get_minimized_dfa(dfa_states, dfa_start_states, dfa_final_states, dfa_transition_function, dfa_letters)

MIN_DFA = {
    "states": min_dfa_states,
    "letters": min_dfa_letters,
    "transition_function": min_dfa_transition_function,
    "start_states": min_dfa_start_states,
    "final_states": min_dfa_final_states
}
with open(output_path, "w") as f:
    json.dump(MIN_DFA, f,indent=4)