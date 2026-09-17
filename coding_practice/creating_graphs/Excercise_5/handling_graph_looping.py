from langgraph.graph import StateGraph , START, END
import random
from typing import Dict, List , TypedDict

# Common agent state maintianed globally in langgraph to maintain the state of the agent globally throught the program run time lifetime
class AgentState(TypedDict):
    name : str
    number : List[int]
    counter : int

# This is a sample node that carry out greetings related task in the graph
def GreetingNode : 
    def __call__(self, state : AgentState) -> AgentState:
        """Greeting Node which says hi to the person"""
        state("This is the first node in the langgraph program")
