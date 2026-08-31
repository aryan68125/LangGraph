from typing import TypedDict, List
from langgraph.graph import StateGraph

# import matplotlib realted libraries that will allow us to visualize the graphs in langgraph after it has been compiled 
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# import math library for calculations
import math

# Implement agent state schema
class AgentState(TypedDict):
    name : str
    values : List[int]
    operation : str
    output : str

# implement node that will process the input
def process_node(state : AgentState) -> AgentState:
    if state['operation'] == '+':
        print(f"operation selected by the user = {state['operation']}")
        result = sum(state['values'])
    elif state['operation'] == '*':
        print(f"operation selected by the user = {state['operation']}")
        result = math.prod(state['values'])
    state['output'] = f"Hi {state['name']}, your answer is : {result}"
    return state

# Now we are gonna create a graph here
graph = StateGraph(AgentState)

# Add the process_node in this empty graph
graph.add_node("processor_node",process_node)

# Now we have to add starting and ending node 
# Adding start node
graph.set_entry_point("processor_node")
# Adding end node
graph.set_finish_point("processor_node")

# Now its time to compile the graph
print(f"Compiling graph...")
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
answers = compiled_graph.invoke({"name":"Rollex", "values":[1,2,3,4,5], "operation":"+"})
print(f"Using the invoke function to run the compiled_graph : {answers}")

# now invoking the grpah using the stream function in a for loop
for step in compiled_graph.stream({"name":"Ballistic","values":[1,2,3,4,5],"operation":"*"}):
   print(f"Using .stream() function to run the compiled graph : {step}") 


