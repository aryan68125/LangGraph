"""
This program is written to demonstrate how to handle loops in langgraph 
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# imports related to matplotlib
# Using these imports I want to visualize the graph that is being created here in the code 
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# This is the main global state that this agent will use to manage the agent state in this program
class AgentState(TypedDict):
    num1 : float
    num2 : float
    operator : str
    result : float
    answer : str

# This function is used to print the graph in matplotlib canvas so that I am able to visualize it and understand the struture of graph created in langgraph 
def visualize_graph() -> None:
    """
    Operational : Call this function when the user presses 'q' to quite the langgraph loop and exits the program 
    """
    png_bytes = compiled_graph.get_graph().draw_mermaid_png()
    image = mpimg.imread(io.BytesIO(png_bytes), format = "png")
    plt.imshow(image)
    plt.axis("off")
    plt.show()

# This is the first node in langgraph graph whose job is to show the welcome message to the user when the program starts 
class GreetingsNode:
    def __call__(self, state : AgentState) -> AgentState:
        state['answer'] = (
                    "Well, hello there! Welcome to the LangGraph calculator"
                    "Here I have implemented a calculator using graphs created using langgraph in python programming language"
                    "Enter an operator (+, -, *, /) and two numbers or press 'q' to quite the program"
                )
        print(state['answer'])
        return state

# This node is responsible to get the input from the user at runtime and set operator , num1 and num2 in global state for this langgraph program
class GetUserInputNode:
    def __call__(self, state : AgentState) -> AgentState:
        operator = input("\n Enter the operator ( +, -, *, /) or 'q' to quit the langgraph program : ").strip()
        state['operator'] = operator
        if operator.lower() != 'q':
            state['num1'] = float(input("\n Enter the first number : "))
            state['num2'] = float(input("\n Enter the second number : "))
        return state

# Now here I am going to write nodes that performs operations on two numbers and returns an updated global state
class test:
    pass

#------------------------------------------------------------------------------------------
# Decision logic : 
# 1. The nodes that serves as a decision nodes in a graph that do not return any state instead they return an edge based on the decision made inside the decision logic based on the input that these nodes get 
#------------------------------------------------------------------------------------------
# This decision node is responsible for making decision which operation to operform on two input numbers based on the input that it recieves in the operator key in the global state set by the GetUserInputNode based on the inputs recieved from the user at runtime 
class OperatorDecisionNode:
    def __call__(self, state : AgentState) -> str:
        state['operator'] = state['operator'].strip().lower()
        if state['operator'] == 'q':
            return "exit_node_edge"
        elif state['operator'] == '+':
            return "add_node_edge"
        elif state['operator'] == '-':
            return "subtract_node_edge"
        elif state['operator'] == '*':
            return "multiplier_node_edge"
        elif state['operator'] == '/':
            return "division_decision_node_edge"
        else:
            return "operator_error_edge"

# This decision node decides if the divide by zero error has occured or not based on if the second number is a zero or not 
class DivisionDecisionNode:
    def __call__(self, state : AgentState) -> str:
        if state['num2'] == 0:
            return "divide_by_zero_error_edge"


compiled_graph = graph.compile()
