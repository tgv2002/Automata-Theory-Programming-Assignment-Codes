import sys
import json

regular_expression = ''

input_path = str(sys.argv[1])
output_path = str(sys.argv[2])
DFA = {}
with open(input_path) as f:
    DFA = json.load(f)
dfa_states, dfa_letters, dfa_transition_function, dfa_start_states, dfa_final_states = DFA["states"], DFA["letters"], DFA["transition_function"], DFA["start_states"], DFA["final_states"]

def incoming_edge_to_start_state():
    global dfa_transition_function
    global dfa_start_states
    there_is = False
    for dfa_transition in dfa_transition_function:
        if dfa_transition[2] == dfa_start_states[0]:
            there_is = True
            break
    return there_is

def outgoing_edge_from_final_state():
    global dfa_transition_function
    global dfa_final_states
    if len(dfa_final_states) >= 2:
        return True
    there_is = False
    for dfa_transition in dfa_transition_function:
        if dfa_transition[0] == dfa_final_states[0]:
            there_is = True
            break
    return there_is
    
def get_edge_values():
    global dfa_states
    global dfa_letters
    global dfa_transition_function
    global dfa_start_states
    edge_values = {u: {v: '' for v in dfa_states} for u in dfa_states}
    for dfa_transition in dfa_transition_function:
        u = dfa_transition[0]
        v = dfa_transition[2]
        if edge_values[u][v] == '':
            edge_values[u][v] = dfa_transition[1]
        else:
            edge_values[u][v] += '+' + dfa_transition[1]
    return edge_values

def get_from_and_to_states(edge_values, dfa_state, dfa_states):
    from_states = []
    to_states = []
    curr_dict_for_from = {f_s: {t_s: v for t_s, v in val.items() if t_s == dfa_state} for f_s, val in edge_values.items()}
    for from_state in dfa_states:
        if from_state not in curr_dict_for_from.keys() or from_state == dfa_state:
            continue
        if curr_dict_for_from[from_state][dfa_state] != '':
            from_states.append(from_state)
    for to_state in dfa_states:
        if to_state not in edge_values[dfa_state].keys() or dfa_state == to_state:
            continue
        if edge_values[dfa_state][to_state] != '':
            to_states.append(to_state)
    return from_states, to_states

def convert_DFA_to_regular_expression(edge_values, dfa_final_state, dfa_initial_state):
    global dfa_states
    global dfa_letters
    global dfa_transition_function
    global dfa_start_states
    for dfa_state in dfa_states:
        if dfa_state == dfa_initial_state or dfa_state == dfa_final_state:
            continue
        from_states, to_states = get_from_and_to_states(edge_values, dfa_state, dfa_states)
        for from_state in from_states:
            if from_state not in edge_values.keys():
                continue
            for to_state in to_states:
                if to_state not in edge_values[from_state].keys():
                    continue
                initial_edge_value = ''
                if edge_values[from_state][to_state] != '':
                    initial_edge_value = '(' + edge_values[from_state][to_state] + ')'
                self_loop_edge_value = ''
                if edge_values[dfa_state][dfa_state] != '':
                    self_loop_edge_value = '(' + edge_values[dfa_state][dfa_state] + ')' + '*'
                from_to_curr_edge_value = ''
                if edge_values[from_state][dfa_state] != '':
                    from_to_curr_edge_value = '(' + edge_values[from_state][dfa_state] + ')'
                curr_to_to_edge_value = ''
                if edge_values[dfa_state][to_state] != '':
                    curr_to_to_edge_value = '(' + edge_values[dfa_state][to_state] + ')'
                updated_edge_value = from_to_curr_edge_value + self_loop_edge_value + curr_to_to_edge_value
                if initial_edge_value != '':
                    updated_edge_value += ('+' + initial_edge_value)
                edge_values[from_state][to_state] = updated_edge_value
        edge_values = {f_s: {t_s: v for t_s, v in val.items() if t_s != dfa_state} for f_s, val in edge_values.items() if f_s != dfa_state}
    return edge_values[dfa_initial_state][dfa_final_state]
        
if incoming_edge_to_start_state():
    dfa_states.append("Qi")
    dfa_transition_function.append(["Qi", "$", dfa_start_states[0]])
    dfa_start_states = ["Qi"]
    
if outgoing_edge_from_final_state():
    dfa_states.append("Qf")
    for final_state in dfa_final_states:
        dfa_transition_function.append([final_state, "$", "Qf"])
    dfa_final_states = ["Qf"] 

edge_values = get_edge_values()
regular_expression = convert_DFA_to_regular_expression(edge_values, dfa_final_states[0], dfa_start_states[0])
regex_output = {
    "regex": regular_expression
}

with open(output_path, "w") as f:
    json.dump(regex_output, f, indent=4)