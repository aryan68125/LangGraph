from typing import TypedDict
from langgraph.graph import StateGraph

# import matplotlib realted libraries that will allow us to visualize the graphs in langgraph after it has been compiled 
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Implement agent state schema 
class AgentState(TypedDict):
    name : str
    age : int
    final : str

# implementing the first node
def first_node(state : AgentState) -> AgentState :
    """This is the first node in our sequence"""
    state["final"] = f"Hello {state['name']}"
    return state

# implementing the second node
def second_node(state : AgentState) -> AgentState:
    """This is the second node in our sequence"""
    state["final"] = state['final'] + f"You are {state['age']} years old"
    return state

# Create an empty graph
graph = StateGraph(AgentState)

# Add both the nodes first_node and second_node in this empty graph
graph.add_node("first_node",first_node)
graph.add_node("second_node",second_node)

# Now we have to add starting node into this graph
graph.set_entry_point("first_node")

# Now that we have added the starting node into this graph how do we connect the first_node with the second_node in this graph?
"""
The way to connect the first and second togeather in a graph in langgraph is by using something called Action .add_edge() method that is provided by langgraph
.add_edge("add a starting node key","ending node key") and this will create an edge between those two nodes in the graph and hence connecting those two graphs togeather in a graph

The type of edge created between the first node and the second node will be a directed edge.
"""
graph.add_edge("first_node","second_node")

# Now we are gonna add the final node into this graph
graph.set_final_point("second_node")

# Now finally we can compile this graph
compiled_graph = graph.compile()

# after compiling this graph I am going to print the graph diagram using matplotlib 
# Here I am writing a logic to use matplotlib to visualize the implemented graph in the code 
png_bytes = compiled_graph.get_graph().draw_mermaid_png()
img = mpimg.imread(io.BytesIO(png_bytes), format="png")

plt.figure(figsize=(4, 6))
plt.imshow(img)
plt.axis("off")                 # hide the pixel-coordinate axes
plt.title("handling_multiple_nodes_in_a_graph")
plt.tight_layout()
plt.show()   

# Now I am going to use .invoke() method to run the compiled graph 
answers = compiled_graph.invoke({"name":"Rollex", "age":28})
print(f"Using the .invoke() method to run the compiled_graph : \n {answers}")

# Now I am going to use .stream() method to run the compiled graph
for step in compiled_graph.stream({"name":"Ballistic","age":25}):
    print(f"Using the .stream() method to run the compiled graph : \n {step}"









