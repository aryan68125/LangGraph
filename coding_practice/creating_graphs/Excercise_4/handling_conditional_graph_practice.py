from typing import TypedDict, List

from langgraph import StateGraph, START, END

import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class AgentState(TypedDict):
    num1 : float
    num2 : float
    operator : str
    result : float
    answer : str

# Create nodes that carry out calculations in the graphs
def adder(state : AgentState) -> AgentState:
    state['result'] = state['num1'] + state['num2']
    return state

def subtractor(state : AgentState) -> AgentState:
    state['result'] = state['num1'] - state['num2']
    return state

def multiplier(state : AgentState) -> AgentState:
    state['result'] = state['num1'] * state['num2']
    return state

def divisor(state : AgentState) -> AgentState:
    if state['num2'] == 0:
        raise ZeroDivisionError("Divide by zero error!")
    state['result'] = state['num1'] / state['num2']
    return state

# Create the final node that will present the result in a human readable form
# This nor
