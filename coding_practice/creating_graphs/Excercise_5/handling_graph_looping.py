from langgraph.graph import StateGraph , START, END
import random
from typing import Dict, List , TypedDict

import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# Common agent state maintianed globally in langgraph to maintain the state of the agent globally throught the program run time lifetime
class AgentState(TypedDict):
    name : str
    number : List[int]
    counter : int

# This is a sample node that carry out greetings related task in the graph
class GreetingNode : 
    def __call__(self, state : AgentState) -> AgentState:
        """Greeting Node which says hi to the person"""
        state['name'] = f"Well hello there, {state['name']}"
        state['counter'] = 0
        return state

# This is the random node that creates a random state
class RandomNode :
    def __call__(self,state : AgentState) -> AgentState:
        """Generates a random number from 0 to 10"""
        state['number'].append(random.randint(0,10))
        state['counter'] += 1
        return state

# This is node is the decision node in langgraph
class ShouldContinue:
    def __call__(self, state : AgentState) -> AgentState:
        """Function to decide what to do next"""
        if state['counter'] < 5:
            print(f"Entering LOOP {state['counter']}")
            # return the edge name 
            return "loop"
        else:
            # return the edge name
            return "exit"

# Create an empty graph here
graph = StateGraph(AgentState)

# Now here I am going to create class objects 
should_continue = ShouldContinue()
random_node = RandomNode()
greeting_node = GreetingNode()

# Now we can add nodes in this empty graph
graph.add_node("greeting_node",greeting_node)
graph.add_node("random_node",random_node)

# Now I am going to add edges 
graph.add_edge(START, "greeting_node")
graph.add_edge("greeting_node","random_node")
graph.add_conditional_edges(
            "random_node", #source node
            should_continue, # rounting node (Action)
            {
                "loop" : "random_node", #self-loop
                "exit" : END # End graph
            }

        )

# Now here I am going to compile the graph
compiled_graph = graph.compile()


result = compiled_graph.invoke({"name":"ROLLEX","number": [],"counter":0})
print(f"result = {result}")

# Here I am going to write a logic to plot the compiled graph using matplotlib 
png_bytes = compiled_graph.get_graph().draw_mermaid_png()
img = mpimg.imread(io.BytesIO(png_bytes), format="png")
plt.figure(figsize=(4, 6))
plt.imshow(img)
plt.axis("off")                 # hide the pixel-coordinate axes
plt.title("handling_multiple_inputs_graph")
plt.tight_layout()
plt.show()   

