from typing import TypedDict
from langgraph.graph import StateGraph, START, END

import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class AgentState(TypedDict):
    num1 : float
    num2 : float
    operator : str
    result : float
    answer : str

# Add a router node that will decide which edge to execute based on the operator selected by the user at runtime 
class Router:
    def __call__(self,state : AgentState):
        if state['operator'] == '+':
            return "adder_edge"
        elif state['operator'] == '-':
            return "subtractor_edge"
        elif state['operator'] == '*':
            return "multiplier_edge"
        elif state['operator'] == '/':
            return "divisor_decision_decision_edge"
        else :
            return "operator_error_edge"
            
class OperatorSelectionErrorNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['result'] = 0
        state['answer'] = f"The system only supports (+, - , * , /) : This operation '{state['operator']}' is invalid"
        return state

# Add the nodes using classes that perform the actual numeric operations in the graphs
class AdderNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['result'] = state['num1'] + state['num2']
        return state

class SubtractorNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['result'] = state['num1'] - state['num2']
        return state

class MultiplierNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['result'] = state['num1'] * state['num2']
        return state

# This node is a conditional node that is responsible for running the edge based on the condition if the second number is 0 or not.
class DivisorDecisionRouterNode:
    def __call__(self, state : AgentState):
        if state['num2'] == 0:
            return "divide_by_zero_error_edge"
        else:
            return "divisor_edge"

class DivisorNode:
    def __call__(self,state : AgentState) -> AgentState:
        state['result'] = state['num1'] / state['num2']
        return state

class DivisorErrorNode:
    def __call__(self, state : AgentState):
        state ['result'] = 0
        state ['answer'] = "Divide by zero error!"
        return state

class FinalAnswerNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['answer'] = f"{state['num1']} {state['operator']} {state['num2']} = {state['result']}"
        return state

# Now here I am going to create an empty graph 
graph = StateGraph(AgentState)

# Now here I am going to create the objects of all the nodes that I have created using classes 
# conditional node
router = Router()
operator_error = OperatorSelectionErrorNode()
adder = AdderNode()
subtractor = SubtractorNode()
multiplier = MultiplierNode()
# conditional node
divisor_decision = DivisorDecisionRouterNode()
divisor = DivisorNode()
divisor_error = DivisorErrorNode()
final_answer = FinalAnswerNode()

# Now Here I am going to start adding nodes in this empty graph that I have created so far 
# I am going to add the conditional node like this where I am going to pass in a lambda function where input and output state will be the same signifying that the decision node is not making any changes in the agent's state since the decision node reutns the edge that is supposed to be executed based on the decisions made that is dependent on the input provided to these decision node.
graph.add_node("router", lambda state: state)
graph.add_node("divisor_decision", lambda state: state)
# Here I am going to add the rest of the nodes in the graph that returns the state and performs operations on the state.
graph.add_node("operator_error", operator_error)
graph.add_node("adder", adder)
graph.add_node("subtractor", subtractor)
graph.add_node("multiplier", multiplier)
graph.add_node("divisor", divisor)
graph.add_node("divisor_error", divisor_error)
graph.add_node("final_answer", final_answer)


# Now here I am going to connect all the nodes in the graph using edges in the graph
graph.add_edge(START,"router")
graph.add_conditional_edges(
            "router", # source node 
            router,
            {
                "adder_edge" : "adder", # edge_name : destination_node_name
                "subtractor_edge" : "subtractor",
                "multiplier_edge" : "multiplier",
                "divisor_decision_decision_edge" : "divisor_decision",
                "operator_error_edge" : "operator_error"
            }
        )
graph.add_conditional_edges(
            "divisor_decision", # source node 
            divisor_decision,
            {
                "divisor_edge" : "divisor", # edge name : destination node name
                "divide_by_zero_error_edge" : "divisor_error"
            }
        )
graph.add_edge("adder", "final_answer")
graph.add_edge("subtractor", "final_answer")
graph.add_edge("multiplier", "final_answer")
graph.add_edge("divisor", "final_answer")
graph.add_edge("final_answer",END)

# Now that all the nodes has been added and connected to each other using edges in a graph I can now go ahead and compile the graph
compiled_graph = graph.compile()

# I am going to enter some inputs now at run time 
num1 = float(input("Enter the first number : "))
num2 = float(input("Enter the second number : "))
operator = (input("Enter the operation that you want to perform on these two numbers ('+', '-', '*', '/')"))

# Here I am going to write a logic to plot the compiled graph using matplotlib 
png_bytes = compiled_graph.get_graph().draw_mermaid_png()
img = mpimg.imread(io.BytesIO(png_bytes), format="png")
plt.figure(figsize=(4, 6))
plt.imshow(img)
plt.axis("off")                 # hide the pixel-coordinate axes
plt.title("handling_multiple_inputs_graph")
plt.tight_layout()
plt.show()   

# Now I am going to run the compiled graph here
result = compiled_graph.invoke({"num1":num1,"num2":num2,"operator":operator})
print(result)


