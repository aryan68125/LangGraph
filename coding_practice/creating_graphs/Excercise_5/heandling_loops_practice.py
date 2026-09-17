from typing import TypedDict
from langgraph.graph import StateGraph, START, END

import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Here I am going to create aa global agent state that I am going to use to manage and track the sate of this graph 
class AgentState(TypedDict):
    num1 : float
    num2 : float
    operator : str
    result : float
    answer : str

# Here I am going to create a greetings node where the user will be greeted by the system and explain what this program does 
class GreetingsNode:
    def __call__(self, state : AgentState) -> AgentState :
        """This node will greete the user and explain in brief on what the system does
         in short"""
         state['answer'] = f"Well, Hello there. Welcome to LangGraph calculator here you will use graphs to perform operations on two numbers based on the operator that you select"
         return state

# This is the router node that will be used to make decisions which node to execute based on the operator selected by the user at run-time 
class OperatorDecisionNode:
    def __call__(self, state : AgentState) -> AgentState:
        """This is the node that decides which edge to execute based on the selected operator by the user"""
        if state['operator'] == '+':
            return "add_node_edge"
        elif state['operator'] == '-':
            return "subtract_node_edge"
        elif state['operator'] == '*':
            return "multiplier_node_edge"
        elif state['operator'] == '/':
            return "division_node_decision_edge"
        else : 
            return "operator_error_edge"

# This node is responsible to print the error message when user selects the operator that is not supported by the system
class OperatorErrorNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['result'] = 0
        state['answer'] = f"You have selected `{state['operator']}` but the system only supports (+, -, *, /) operators. Select the correct operator and try again!"
        return state

# Now I am going to create number processing nodes here 
class AddNode:
    def __call__(self, state : AgentState) -> AgentState:
        """This node is will add num1 and num2"""
        state['result'] = state['num1'] + state['num2']
        state['answer'] = f"{state['num1']} {state['operator']} {state['num2']} = {state['result']}"
        return state

class SubtractNode:
    def __call__(self, state : AgentState) -> AgentState:
        """This node will subtract num1 and num2"""
        state['result'] = state['num1'] - state['num2']
        state['answer'] = f"{state['num1']} {state['operator']} {state['num2']} = {state['result']}"
        return state

class MultiplierNode:
    def __call__(self, state : AgentState) -> AgentState:
        """This node will multiply two numbers"""
        state['result'] = state['num1'] * state['num2']
        state['answer'] = f"{state['num1']} {state['operator']} {state['num2']} = {state['result']}"
        return state

# This is a router node that will decide which edge to execute based on if num2 is zero or not
class DivisionDecisionNode:
    def __call__(self, state : AgentState) -> AgentState:
        """This node will make decision which edge to execute"""
        if state['num2'] == 0:
            return "divide_by_zero_edge"
        else:
            return "division_node_edge"

class DivisionNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['result'] = state['num1'] / state['num2']
        state['answer'] = f"{state['num1']} {state['operator']} {state['num2']} = {state['result']}"
        return state

class DivisionErrorNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['result'] = 0
        state['answer'] f"Divide by Zero ERROR"
        return state

class LoopDecisionNode:
    def __call__(self, state : AgentState) -> AgentState:
        if state['operator'] == 'q':
            return "exit_edge"
        else:
            return "loop_edge"

class EndEdgeNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['answer'] = f"Program Terminated!"
        return state

# Here I am going to create an empty graph 
graph = StateGraph(AgentState)

# Create objects of the nodes before adding them to this empty graph
# Add greeting node
greeting_message_node = GreetingsNode()

# Objects of nodes that actually perform operations on the numbers
add_node = AddNode()
subtract_node = SubtractNode()
multiplier_node = MultiplierNode()
division_node = DivisionNode()

# objects of router nodes 
operator_router_node = OperatorDecisionNode()
division_router_node = DivisionDecisionNode()
looping_router_node = LoopDecisionNode()

# error handling node 
operator_error_node = OperatorErrorNode()
division_error_node = DivisionErrorNode()

# end edge node
end_edge_node = EndEdgeNode()

# Add nodes to this empty graph 
# Add greeting node in the graph
graph.add_node("greeting_message_node",greeting_message_node)

# Add Router nodes
graph.add_node("operator_router_node", lambda state: state)
graph.add_node("division_router_node", lambda state: state)
graph.add_node("looping_router_node", lambda state: state)

# Add nodes that perform operation ADD, SUBTRACTION , MULTIPLICATION, DIVISION
graph.add_node("add_node",add_node)
graph.add_node("subtract_node",subtract_node)
graph.add_node("multiplier_node",multiplier_node)
graph.add_node("division_node",division_node)

# Add error handeling nodes in the graph
graph.add_node("operator_error_node",operator_error_node)
graph.add_node("division_error_node",division_error_node)


# add the last node in the graph
graph.add_node("end_edge_node",end_edge_node)


# Now here I am going to connect these nodes using edges
graph.add_edge(START, "greeting_message_node")
graph.add_edge("greeting_message_node","operator_router_node")
graph.add_conditional_edges(
            "operator_router_node", # Source node
            operator_router_node, # action 
            {
                "add_node_edge" # edge_name : target_node_name
                "subtract_node_edge"
                "multiplier_node_edge"
                "division_node_decision_edge"
            }
        )
















