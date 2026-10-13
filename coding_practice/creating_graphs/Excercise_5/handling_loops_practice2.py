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


