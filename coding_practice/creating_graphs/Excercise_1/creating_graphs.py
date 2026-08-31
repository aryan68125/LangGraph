from typing import TypedDict, Dict
# This is the framework that allows you design and manage the flow of tasks in your application using graph
from langgraph.graph import StateGraph

# matplotlib related to vizualizing the implemented code and visualizing the code 
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# Create a State
# This will be a shared state that will keep track of the state in this application run 
class AgentState(TypedDict):
    compliment_message : str

# Creating a node 
# A node is nothing but a function inside which some processing happens based on the inputs that it recieves in form of state it will generate an output in form of state in LangGraph
def compliment_node(state : AgentState) -> AgentState :  
    state['compliment_message'] = f"{state['compliment_message']},you are doing an amazing job learning LangGraph!"
    return state 

# Now here we are gonna create a graph here 
graph = StateGraph(AgentState)

# Now we are gonna add the node in this empty graph that we have created so far
graph.add_node("complimenter",compliment_node)

# Now that we have added a node in out empty graph we also have to add start and end node in this graph
# Adding start node
graph.set_entry_point("complimenter")
# Adding ending node 
graph.set_finish_point("complimenter")

# Compile the graph that we created so far
print(f"Compiling the graph!")
app = graph.compile()

# Now its time to invoke the graph after compilation
name_input = input("Enter the name : ")
result = app.invoke({"compliment_message":name_input})
print(f"Using the invoke function to run the compiled graph : {result['compliment_message']}")


# To understand how data flows between nodes through the graph, I am going to use .stream()
name_input_for_stream = input("Enter the name again for stream : ")
for step in app.stream({"compliment_message":name_input_for_stream}):
    print(f"Using .steam() to print the data flowing in the graph : {step}") 


# Here I am writing a logic to use matplotlib to visualize the implemented graph in the code 
png_bytes = app.get_graph().draw_mermaid_png()
img = mpimg.imread(io.BytesIO(png_bytes), format="png")

plt.figure(figsize=(4, 6))
plt.imshow(img)
plt.axis("off")                 # hide the pixel-coordinate axes
plt.title("hello_world_graph")
plt.tight_layout()
plt.show()                      # blocks until you close the window






