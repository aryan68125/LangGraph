from typing import Dict, TypedDict
# This is the framework that allows you design and manage the flow of tasks in your application using graph
from langgraph.graph import StateGraph 

# Here we now will create an AgentState - A shared data structure that keeps track of information as your application runs.

# Create a State
# In LangGraph we create States using classes 
class AgentState(TypedDict):
    message : str

# Create a Node
def greeting_node(state : AgentState) -> AgentState:
    # Docs string are very important in case of langraph 
    # these docs strings will tell the llm what this function actually does
    # what actions does this function performs


