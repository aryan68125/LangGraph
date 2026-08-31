from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph

# matplotlib related to vizualizing the implemented code and visualizing the code 
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Implement the state schema first 
"This stores the state of your agent"
"It is also known as data model in normal python language"
class AgentState(TypedDict):
    values : List[int]
    name : str
    results : str

# Here I am going to create a node that is capable of handling multiple input values at the same time 
def process_values(state: AgentState) -> AgentState :
    """This function handles multiple different inputs
    """
    print(f"Printing state before processing : {state}")
    state["results"] = f'Well Hello there {state["name"]}! your sum = {sum(state["values"])}'
    print(f"Printing state after processing : {state}")
    return state

# Now here we are gonna create a graph here 
graph = StateGraph(AgentState)

# Now we are gonna add the node into this newly created graph 
graph.add_node("processor_node",process_values)

# Now that we have added a node named "process_values" in our empty graph we also have to add the starting node and the ending node in our graph as well
# add a starting node in the graph
graph.set_entry_point("processor_node")
# add an ending node in the graph
graph.set_finish_point("processor_node")

# Now we have to compile the graph that we have created with all the nodes that we have attached to that graph so far 
print(f"Compiling the graph ..... ")
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

# Now here I am going to invoke the graph that has been compiled so far 
answers = compiled_graph.invoke({"values":[1,2,3,4,5], "name":"Rollex"})
print(f"Using the invoke function to run the compiled graph : {answers['results']}")

for step in compiled_graph.stream({"values":[1,2,3,4,5], "name":"Rollex"}):
    print(f"Using .steam() to print the data flowing in the graph : {step}")



