from typing import Dict, TypedDict
# This is the framework that allows you design and manage the flow of tasks in your application using graph
from langgraph.graph import StateGraph 

# imports related to visualizing the implemented code 
from IPython.display import Image, display

# Here we now will create an AgentState - A shared data structure that keeps track of information as your application runs.

# Create a State
# In LangGraph we create States using classes
# When creating StateGraph we need to pass this AgentState class as our state schema into our graph that we create in LangGraph project
class AgentState(TypedDict):
    message : str

# Create a Node
def greeting_node(state : AgentState) -> AgentState:
    # Docs string are very important in case of langraph 
    # these docs strings will tell the llm what this function actually does
    # what actions does this function performs
    # when you do @tool / bind_tools(), the docstring becomes the tool description in the model's schema
    # Important NOTE : A node docstring is for humans — LangGraph never shows it to a model.
    """
    Simple node that add a greeting message to the_state
    """
    state['message'] = f"Hey {state['message']} how is your day going?"
    return state

# Now we are going to create a graph here
# Pass in the state that we have created earlier in this graph that we have created below as an input parameter
# Right now this graph is nothing but empty so how do we actually add a node in this graph?
graph = StateGraph(AgentState)
# To add node in this empty graph use the add_node function below and pass in two parameters in this function 
# 1. Name of the node 
# 2. What action does that node performs (the action of a node is defined by the function that we have created earlier with the name "greeting_node" so in the action we will pass in the name of that function) 
graph.add_node("greeter",greeting_node)

# Up until now we have added a single node in our graph but so far we haven't added a start and the end node in our graph here 
# Here I am going to set an entry point in this graph which is essentially a start node in our graph that we have created so far
# Here you will have to pass in one parameter which is the key
graph.set_entry_point("greeter")

# Now here we will set up the finish point or the ending node for our graph
graph.set_finish_point("greeter")

# One last thing that we need to do is to compile thiws graph using the inbuilt compile engine
app = graph.compile()

# Just a word of caution here 
# Just because a graph compiles without an error doesn't mean it will successfully run

# Here I am writing a code that will help you visualize this 
display(Image(app.get_graph().draw_mermaid_png()))

# Now its time to run the graph 
result = app.invoke({"message","ROLLEX"})
print(result)
print(result["message"])

# To understand how data flows through the graph I am going to use .stream() instead of using print after every node 
for step in app.stream({"message","ROLLEX"}):
    # {'greater' : {"message": "Hey ROLLEX how is your day going?"}}
    print(step)

