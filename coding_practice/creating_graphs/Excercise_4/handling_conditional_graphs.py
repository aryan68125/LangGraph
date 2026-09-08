from typing import TypedDict, List
"""
There is a difference between this implementation that we have done so far 
Here as you can see we have imported START and END point 

There are multiple ways that we can initialize start and end point in langgraph
"""
from langgraph.graph import StateGraph, START, END

# import matplotlib realted libraries that will allow us to visualize the graphs in langgraph after it has been compiled 
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class AgentState(TypedDict):
    num1 : float
    num2 : float
    operator : str
    final_result : float
    result : str

def adder(state : AgentState) -> AgentState:
    """This node adds the 2 numbers"""
    state["final_result"] = state["num1"] + state["num2"]
    return state

def subtractor(state : AgentState) -> AgentState:
    """This node subtracts the 2 numbers"""
    state["final_result"] = state["num1"] - state["num2"]
    return state

def multiplier(state : AgentState) -> AgentState:
    """This node multiples the 2 numbers"""
    state["final_state"] = state["num1"] * state["num2"]
    return state

def divisor(state : AgentState) -> AgentState:
    """This node divides the two numbers"""
    if state["num2"] == 0:
        raise ZeroDivisionError("Divide by zero error!")
    state["final_state"] = state["num1"] / state["num2"]
    return state

def create_final_result(state : AgentState) -> AgentState:
    """This node generates the final output in a humanized text form"""
    state["result"] = f"{state['num1']} + {state['num2']} = {state['final_result']}"
    return state

# This node will make decision which node to execute in the graph based on the inputs provided by the user
# This decision node is also called the router node because this node is responsible to route the flow towards the nodes that must be run based on the input of the user
# This node does not return a state like other nodes the router node only returns an edge
def decision_node(state : AgentState) -> AgentState:
    """This node is responsible to make dicision based on the operation chosen by the user"""
    if state["operator"] == "+":
        # In Langraph we don't call the function that must be executed based on the user choice directly like what we do in normal python code 
        # Instead we call the edge name like "addition_operation"
        return "addition_operation"
    elif state["operator"] == "-":
        return "subtraction_operation"

    elif state["operator"] == "*":
        return "multiplication_operation"

    elif state["operator"] == "/":
        return "division_operation"
    else:
        raise ValueError("Wront choice : The system only supports [+, -, *, /] only. The chosen operation is not supported by the system.")
    
# Now we need to create a graph here 
graph = StateGraph(AgentState)

# Now here we are gonna all the nodes that processes num1 and num2 here 
graph.add_node("adder",adder)
graph.add_node("subtractor",subtractor)
graph.add_node("multiplier",multiplier)
graph.add_node("divisor",divisor)
graph.add_node("create_final_result",create_final_result)
#Now here I am going to add decision node in this graph
"""
if you write this 
graph.add_node("router",decision_node)
then it will fail because as you can notice the decision_node aka "router" node does not return graph state instead it returns an edge based on the condition chosen by the user. The router will change the flow of execution of the graph based on the choice made by the user.
hence we need to use this instead of what we use for the standard nodes here in the graph
graph.add_node("router",lambda state:state)
now you may ask that what the hell is this lambda function and what does it do ? 
lambda state:state --> tells langraph to keep the input and output state as it is where no changes are made in the state i.e your input state will your output state 

Think of this as a pass through function this is done because in this router node we are not changing the state at all we are just routing the flow based on the made decision. 
"""
graph.add_node("router",lambda state:state)

# Now here we are gonna add the edges here
# Now previously we used to add start and end node like set_entry_point and set_finish_point
# In this case we are not gonna do this way.
graph.add_edge(START,"router")
# in order to add an edge that fires the next node based on a condition that is being processed in the router node we use add_conditional_edge function in langgraph
graph.add_conditional_edges(
            "router", # source node
            decision_node, # action function
            { # Path Map -> this is in a format {Edge : Node}
            "addition_operation" : "adder",
            "subtraction_operation" : "subtractor",
            "multiplication_operation" : "multiplier",
            "division_operation" : "divisor"
            }
        )

# Now we need to add all these edges to the create_final_result node
graph.add_edge("adder", "create_final_result")
graph.add_edge("subtractor", "create_final_result")
graph.add_edge("multiplier", "create_final_result")
graph.add_edge("divisor", "create_final_result")

# No finally we need add the edge between the create_final_result node and the end node
graph.add_edge("create_final_result",END)

# Now we need to compile the graph thay we have created so far in here
compiled_graph = graph.compile()


# Here I am writing a logic to use matplotlib to visualize the implemented graph in the code 
png_bytes = compiled_graph.get_graph().draw_mermaid_png()
img = mpimg.imread(io.BytesIO(png_bytes), format="png")

plt.figure(figsize=(4, 6))
plt.imshow(img)
plt.axis("off")                 # hide the pixel-coordinate axes
plt.title("handling_multiple_inputs_graph")
plt.tight_layout()
plt.show()   


# now invoking the graph using invoke function 
answers = compiled_graph.invoke({"num1":15.2, "num2":13.4, "operator":"+"})
print(f"Using the invoke function to run the compiled_graph : {answers}")

# now invoking the grpah using the stream function in a for loop
for step in compiled_graph.stream({"num1":15.2, "num2":13.4, "operator":"-"}):
   print(f"Using .stream() function to run the compiled graph : {step}") 


