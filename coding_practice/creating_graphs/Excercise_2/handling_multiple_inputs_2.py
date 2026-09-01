from typing import TypedDict, List

from langgraph.graph import StateGraph

# import math library for calculations
import math

#import matplotllib so that we can view the graph after it has been compiled
import io
from matplotlib import pyplot as plt
from matplotlib import image as mpimg


# Now here I am going to define my state
class AgentState(TypedDict):
    name : str
    revenue : List[float]
    result : float
    operation : str
    answer : str

# Now here I am going to create a processing node 
def processing_node(state : AgentState) -> AgentState:
    if state['operation'] == '+':
        result = f"the total sum of your revenue is {sum(state['revenue'])}"
    elif state['operation'] == 'avg':
        result = f"your average revenue is {sum(state['revenue'])/len(state['revenue'])}"
    else:
        print(f"The choices that are allowed are '+' or 'avg'")
        print(f"you are trying to perform an invalid operation")
    state['answer'] = f"Hello {state['name']},{result}"
    return state

# Now I am going to create an empty graph
graph = StateGraph(AgentState)

# Add the process node in this empty graph
graph.add_node("processing_node",processing_node)

#Now here I am going to add a starting and ending node in the graph
#Adding starting node
graph.set_entry_point("processing_node")
#Adding finishing node
graph.set_finish_point("processing_node")

# Now I am going to compile the graph
print("Compiling graphs ....")
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

#Now here I am going to invoke the compiled graph using .invoke() function
name = input(f"Enter the name ")
revenue_list = list(map(float, input("Enter monthly revenue values separated by space : ").split()))

print(f"Now you have to enter the operation that you want to perform : ")
print(f"Enter '+' to perform sumission")
print(f"Enter 'avg' to perform average")
operation = input(f"Enter the operation that you want to perform : ")
result = compiled_graph.invoke({"name":name,"revenue":revenue_list,"operation":operation})
print(f"Using the .invoke() function to run the compiled_graph : {result}")

# Now here I am going to use .stream() function to invoke the compiled graph
for step in compiled_graph.stream({"name":name,"revenue":revenue_list,"operation":operation}):
    print(f"Using the .stream() function to run the compiled_graph : {step}")


