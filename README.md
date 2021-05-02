# AUTOMATA THEORY - PROGRAMMING ASSIGNMENT


## By - Gokul Vamsi Thota
## Roll number - 2019111009


### OneDrive link to video

* https://iiitaphyd-my.sharepoint.com/:u:/g/personal/gokul_vamsi_research_iiit_ac_in/ERV8gYg6PTpIqCI64VZV1bQBlweBkRS6szBUI7KM0NAjEg?e=judFcA



### Question wise approach - 



#### Question 1 - 

* On taking the input regular expression, it is first converted to postfix format (for creating a tree in the next steps). This is done with the help of Shunting-Yard algorithm. It is ensured that precedence order is followed on doing so (Kleene star '*' > Concatenation > Union '+')

* Once the postfix expression is obtained, a regular expression tree is obtained. This is done with the help of a class called RegexTree, which contains information about left child, right child, and current node's value (used if its not a symbol), and the type (if its a symbol). Thus, the regular expression tree is constructed for the postfix expression such that, every non-symbol character (operator) would have its 2 operands as left and right children.

* Now the regular expression tree is parsed, using a recursive function called parseRegularExpression(tree), the function chooses to recurse down the path based on the type of operator/symbol it encounters. Union operator, concatenation operator, kleene star operator and symbols are handled in different recursive functions, which are called from parseRegularExpression(tree) based on what it encountered.

* Each of the above mentioned recursive function for an operator, obtains the NFA of the subtree of left child (and right child if exists), and uses these NFAs to construct the final NFA for this subtree including the operator. At each point, initial and final states of NFAs obtained this way are returned, so that they are used in further steps. The recursive function for the symbol of tree simply creates 2 states (initial and final), and connects them with a directed edge with weight as symbol itself.

* Thus, when the regular expression is correctly parsed in above way, the final NFA is obtained. Final states are calculated as states which don't have any transitions which move outward from this edge.



#### Question 2 - 

* In the final DFA which is computed from given NFA, the set of letters would be same as that of the NFA, and the set of states would be a set of lists which includes all possible subsets of the states of NFA (powerset). Hence, both these values are calculated accordingly.

* The final states of DFA would be those combinations of states of NFA in which there exists atleast one NFA accept state. This is computed accordingly.

* A directed graph is constructed, including all transistions involving 'epsilon' state as their symbol, based on the transition table.

* A function called allEpsilonTransitionsFromState(state) is defined such that it includes all the NFA states which are reachable via 0 or more epsilon arrows, from each NFA state in the current DFA state. DFS function is used to obtain such a collection for every DFA state. This is to ensure epsilon states are included in the final DFA appropriately.

* Transition function is obtained such that, for a particular DFA state and a particular symbol, the next DFA state would be a collection of all NFA states that are reachable from atleast one NFA state in the current DFA state. Epsilon transitions are included accordingly. 

* The start state is computed such that it includes all epsilon transitions from start state of NFA.

* Thus, as all properties required are computed above, the final DFA is obtained.



#### Question 3 - 

* In case the given DFA digraph has incoming edge to start state, create a new start state such that it has an epsilon transition to DFA start state, and no incoming edges are present for this new start state.

* In case the given DFA digraph has multiple final states, convert these to non-final by creating a new final state, and adding an epsilon transition to this new state from the previous final states.

* In case the given DFA digraph has outgoing edge from final state, create new final state with no outgoing edge. 

* Now traverse through every intermediate state one by one, and obtain the list of all states contributing an incoming edge to this state (from_states), and list of all states which receive the outgoing edge from this state (to_states), for the current state being traversed.

* Now use these lists from_states and to_states, to eliminate current state, by connecting all paths in which this state is present, in an appropriate way, with the help of every combination of from_state and to_state of this state. Update the relevant edge weights of the digraph whenever such elimination occurs.

* After performing above process for every intermediate state, the final regular expression would be the value on the edge connection start state and final state.



#### Question 4 - 

* For the given DFA, remove all the unreachable states from the start states. This is done by constructing digraph for given DFA and conducting a DFS from start state, and eliminating unvisited states. Thus, states, accept states, transition function of DFA are updated. 

* Letters of the minimized DFA would be same as letters of given DFA.

* Construct an undirected graph connecting every accept state with every non-accept state of given DFA.

* Repeatedly add distinct edges to above undirected graph, until its no longer possible in the following way: Iterate through every pair of distinct states q1 and q2, and every action a, add the edge between q1 and q2 if there exists an edge between delta(q1, a) and delta(q2, a), where delta is the transition function of DFA.

* Obtain a set of collections for each state in the following way: Add state2 to the collection of state1 and state1 to collection of state2 if there is no edge between these two in the undirected graph, say state_collection

* Thus, the distinct state collections obtained would be the states of minimized dfa (each state would be a list of DFA states given as input). Minimized dfa would have the start state as state_collection of start state, final states would be the list of state_collections of every final state of given dfa.

* Minimized DFA Transition function is obtained as: for every dfa state q in input DFA and for every symbol a in input DFA, the transition would be given by the symbol a, from state collection of q to state collection of delta(q, a), where delta is the input DFA transition function.

* Hence, we obtained minimized DFA for the given input DFA.


