from typing import TypedDict, List
from langgraph.graph import StateGraph

# import matplotlib realted libraries that will allow us to visualize the graphs in langgraph after it has been compiled 
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Here I am going to implement agent state schema
class AgentState(TypedDict) : 
    name : str
    age : int
    skills : List[str]
    answer : str

# Here I am going to implement first node 
def first_node(state : AgentState) -> AgentState : 
    state['answer'] = f"{state['name']}, welcome to the system!"
    return state

# Here I am going to implement second node
def second_node(state : AgentState) -> AgentState : 
    state['answer'] = state['answer'] + " " + f"You are {state['age']} years old!"
    return state

# HEre I am going to implement third node
def third_node(state: AgentState) -> AgentState : 
    state['answer'] = state['answer'] + " " + f"You have skills in : {state['skills']}"
    return state

# Now here I am going to create an empty graph
graph = StateGraph(AgentState)

# Here I am going to add the first_node, second_node and third_node in this empty graph that I have created so far 
graph.add_node("first_node",first_node)
graph.add_node("second_node",second_node)
graph.add_node("third_node",third_node)

# Now here I am going to add the starting node in this graph
graph.set_entry_point("first_node")

# Now here I am going to add the final node in this graph
graph.set_finish_point("third_node")

# Now here I am going to connect first, second and third node togeather using .add_edge() method
graph.add_edge("first_node","second_node")
graph.add_edge("second_node","third_node")

# Now I can finally compile the graph that I have created so far 
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
print("Enter the things below so that you can run the compiled graph using .invoke() methos : \n")
name = input(f"Enter the name :\n")
age = int(input(f"Enter the age : \n"))
skills = input("Enter skills separated by space: \n").split()   
answers = compiled_graph.invoke({"name":name,"age":age,"skills":skills})
print(f"Using the .invoke() method to run the compiled_graph : \n {answers}")

# Now I am going to use the .stream() method to run the compiled graph
print("\n \n")
print("Enter the things below so that you can run the compiled graph using the .stream() method \n")
name = input(f"Enter the name : \n")
age = int(input("Enter the age : \n"))
skills = input("Enter the skills separated by space : \n").split()
for step in compiled_graph.stream({"name":name,"age":age,"skills":skills}):
    print(f"Using the .stream() method to run the comiled_graph : \n {step}")


