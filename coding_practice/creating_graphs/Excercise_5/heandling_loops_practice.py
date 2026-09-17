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

# 
