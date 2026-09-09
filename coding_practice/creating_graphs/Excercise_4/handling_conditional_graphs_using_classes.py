from typing import TypedDict
from langgraph.graph import TypedDict, START, END

import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class AgentState(TypedDict):
    num1 : float
    num2 : float
    operator : str
    result : float
    answer : str

# Add a router node that will decide which edge to execute based on the operator selected by the user at runtime 
class Router:
    def __call__(self,state : AgentState):
        if state['operator'] == '+':
            return "adder_edge"
        elif state['operator'] == '-':
            return "subtractor_edge"
        elif state['operator'] == '*':
            return "multiplier_edge"
        elif state['operator'] == '/':
            return "divisor_decision_decision_edge"
        else : 
            
class OperatorSelectionErrorNode:
    def __call__(self, state : AgentState) -> AgentSate:
        state['result'] = 0
        state['answer'] = f"The system only supports (+, - , * , /) : This operation {state['operator']} is invalid"

# Add the nodes using classes that perform the actual numeric operations in the graphs
class AdderNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['result'] = state['num1'] + state['num2']
        return state

class SubtractorNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['result'] = state['num1'] - state['num2']
        return state

class MultiplierNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['result'] = state['num1'] * state['num2']
        return state

# This node is a conditional node that is responsible for running the edge based on the condition if the second number is 0 or not.
class DivisorDecisionRouterNode:
    def __call__(self, state : AgentState):
        if state['num2'] == 0:
            return "divide_by_zero_error_edge"
        else:
            return "divisor_edge"

class DivisorNode:
    def __call__(self,state : AgentState) -> AgentState:
        state['result'] = state['num1'] / state['num2']
        return state

class DivisorErrorNode:
    def __call__(self, state : AgentState):
        state ['result'] = 0
        state ['answer'] = "Divide by zero error!"
        return state

class FinalAnswerNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['answer'] = f"{state['num1']} {state['operator']} {state['num2']} = {state['result']}"
        return state

# Now here I am going to create an empty graph 
graph = StateGraph(AgentState)

# Now here I am going to create the objects of all the nodes that I have created using classes 
router = Router()
operator_error = OperatorSelectionErrorNode()
adder = AdderNode()
subtractor = SubtractorNode()
multiplier = MultiplierNode()
divisor_decision = DivisorDecisionRouterNode()
divisor = DivisorNode()
divisor_error = DivisorErrorNode()
final_answer = FinalAnswerNode()

# Now Here I am going to start adding nodes in this empty graph that I have created so far 
graph.add_node()
