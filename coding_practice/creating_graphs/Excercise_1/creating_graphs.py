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
class compliment_node(state : AgentState) -> AgentState :  
    state['compliment_message'] = f"{state['compliment_message'],you are doing an amazing job learning LangGraph}!"
    return state 








