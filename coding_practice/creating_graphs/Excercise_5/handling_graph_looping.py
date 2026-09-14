from langgraph.graph import StateGraph , START, END
import random
from typing import Dict, List , TypedDict

class AgentState(TypedDict):
    name : str
    number : List[int]
    counter : int

def GreetingNode : 
    def __call__(self, state : AgentState) -> AgentState:
        """Greeting Node which says hi to the person"""
        state("name")
