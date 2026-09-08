from typing import TypedDict, List

from langgraph import StateGraph, START, END

import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class AgentState(TypedDict):
    num1 : float
    num2 : float
    operator : str
    result : float
    answer : str

# Create nodes that carry out calculations in the graphs
def adder(state : AgentState) -> AgentState:
    state['result'] = state['num1'] + state['num2']
    return state

def subtractor(state : AgentState) -> AgentState:
    state['result'] = state['num1'] - state['num2']
    return state

def multiplier(state : AgentState) -> AgentState:
    state['result'] = state['num1'] * state['num2']
    return state

def divisor(state : AgentState) -> AgentState:
    if state['num2'] == 0:
        raise ZeroDivisionError("Divide by zero error!")
    state['result'] = state['num1'] / state['num2']
    return state

# Create the final node that will present the result in a human readable form
# This node will come exactly before the end node
def answer_humanizer(state : AgentState) -> AgentState:
    state['answer'] = f"{state['num1']} {state['operator']} {state['num2']} = {state['result']}"

# Now here I am going to create a node called router that will be responsible to activate the nodes based on the choice made by the user 
# this router node only returns the edges not the agent state like other nodes hence how I put this node in the graph will be different from the other nodes that I add in the graph
def decision_node(state : AgentState):
    if state['operator'] == '+':
        # Here instead of calling the function that is carrying out the operation I will call the edge that connects this router to that node that is carrying out the operation 
        return "addition_operation_edge"
    elif state['operator'] == '-':
        return "subtraction_operation_edge"
    elif state['operator'] == '*':
        return "multiplication_operation_edge"
    elif state['operator'] == '/':
        return "division_operation_edge"
    else : 
        raise ValueError("The choice is invalid : The system can only perform these operations +, - , * and / ")
    
# Now here I am going to create an empty graph
graph = StateGraph(AgentState)


# Now here I am going add all the normal nodes that is responsible for processing num1 and num2 into the graph
graph.add_node("adder",adder)
graph.add_node("subtractor",subtractor)
graph.add_node("multiplier",multiplier)
graph.add_node("divisor",divisor)


# Now I am going to add the router node (the decision making node) into the graph
# The reason this router node has a different way of adding it into the graph is because this particular type of node in langgraph is accepting state but it is not returning a state unlike other nodes instead it is returning an edge based on the operator chosen by the user 
# lambda state:state --> meanse that the input and output state in this node is the same hence signifying that this particular node is not making any changes in the state like what normally happens in a normal node in langgraph
graph.add_node("router",lambda state:state)


# Now I am going to add edges in the graph and connect all the nodes in the graph
graph.add_edge(START,"router")

# Now I am going to connect the router node with all the nodes that is performing operations on num1 and num2 by creating edges that conncect this router node with all the other operation nodes 
graph.add_conditional_edges(
            "router",
            decision_node,
            {
                "addition_operation_edge" : "adder",
                "subtraction_operation_edge" : "subtractor",
                "multiplication_operation_edge" : "multiplier",
                "division_operation_edge" : "divisor",
            }
        )

# I have to connect all the operation nodes with the answer_humanizer node by creating nodes between them
graph.add_edge("adder","answer_humanizer")
graph.add_edge("subtractor","answer_humanizer")
graph.add_edge("multiplier","answer_humanizer")
graph.add_edge("divisor","answer_humanizer")

# Now Finally I can add this answer_humanizer node to the end node in the graph 
graph.add_edge("answer_humanizer",END)


# Now that I have completed the graph creation process now I can go ahead and compile this graph
compiled_graph = graph.compile()


# Here I am going to write a logic to plot the compiled graph using matplotlib 
png_bytes = compiled_graph.get_graph().draw_mermaid_png()
img = mpimg.imread(io.BytesIO(png_bytes), format="png")
plt.figure(figsize=(4, 6))
plt.imshow(img)
plt.axis("off")                 # hide the pixel-coordinate axes
plt.title("handling_multiple_inputs_graph")
plt.tight_layout()
plt.show()   

# taking inputs at run time 
num1 = float(input(f"Enter the first number : "))
print("\n")
num2 = float(input(f"Enter the second number : "))
print("\n")
print(f"Choose the operation that you want to perform on these two numbers  : num1 = {num1} , num2 = {num2}")
print("\n")
print(f"The operations that this system can perform are + , - , * , /")
print("\n")
operator = input("Enter the operator now : ")
print("\n")


# Now I am going to run this compiled graph using .invoke() function
answers = compiled_graph.invoke({"num1":num1, "num2":num2, "operator":operator})
print(f"Using the invoke function to run the compiled_graph :")
print("\n")
print(answers)

# Now I am going the run the compiled graph using .stream() function
print("Using .stream() function to run the compiled graph : ")
print("\n")
for step in compiled_graph.stream({"num1":num1,"num2":num2,"operator":operator}):
    print(step)






