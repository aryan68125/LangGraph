from langgraph.graph import StateGraph , START, END
import random
from typing import Dict, List , TypedDict

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

# Now we can add nodes in this empty graph
graph.add_node("greeting")



