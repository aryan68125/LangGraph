from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# imports related to matplotlib
# used to visualize the graph that I have created here
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class AgentState(TypedDict):
    num1: float
    num2: float
    operator: str
    result: float
    answer: str


class GreetingsNode:
    def __call__(self, state: AgentState) -> AgentState:
        state['answer'] = (
            "Well, hello there! Welcome to the LangGraph calculator. "
            "Enter an operator (+, -, *, /) and two numbers, or 'q' to quit."
        )
        print(state['answer'])
        return state


class GetUserInputNode:
    def __call__(self, state: AgentState) -> AgentState:
        """Collects the operator and the two operands, unless quitting."""
        operator = input("\nEnter the operator (+, -, *, /) or 'q' to quit: ").strip()
        state['operator'] = operator
        if operator.lower() != 'q':
            state['num1'] = float(input("Enter first number: "))
            state['num2'] = float(input("Enter the second number: "))
        return state


# ---------------------------------------------------------------------------
# Decision logic. These callables return an edge-label string, not state —
# they are only ever passed to add_conditional_edges, never to add_node.
# The nodes they're attached to ("operator_router_node",
# "division_router_node") are separate: plain `lambda state: state`
# passthroughs registered with add_node, whose only job is to give the
# decision a real position in the graph without touching state.
# ---------------------------------------------------------------------------
class OperatorDecisionNode:
    def __call__(self, state: AgentState) -> str:
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
            return "division_node_decision_edge"
        else:
            return "operator_error_edge"


class DivisionDecisionNode:
    def __call__(self, state: AgentState) -> str:
        if state['num2'] == 0:
            return "divide_by_zero_edge"
        else:
            return "division_node_edge"


class OperatorErrorNode:
    def __call__(self, state: AgentState) -> AgentState:
        state['result'] = 0
        state['answer'] = (
            f"You have selected `{state['operator']}` but the system only "
            f"supports (+, -, *, /) operators. Select the correct operator and try again!"
        )
        print(state['answer'])
        return state


class AddNode:
    def __call__(self, state: AgentState) -> AgentState:
        state['result'] = state['num1'] + state['num2']
        state['answer'] = f"{state['num1']} {state['operator']} {state['num2']} = {state['result']}"
        print(state['answer'])
        return state


class SubtractNode:
    def __call__(self, state: AgentState) -> AgentState:
        state['result'] = state['num1'] - state['num2']
        state['answer'] = f"{state['num1']} {state['operator']} {state['num2']} = {state['result']}"
        print(state['answer'])
        return state


class MultiplierNode:
    def __call__(self, state: AgentState) -> AgentState:
        state['result'] = state['num1'] * state['num2']
        state['answer'] = f"{state['num1']} {state['operator']} {state['num2']} = {state['result']}"
        print(state['answer'])
        return state


class DivisionNode:
    def __call__(self, state: AgentState) -> AgentState:
        state['result'] = state['num1'] / state['num2']
        state['answer'] = f"{state['num1']} {state['operator']} {state['num2']} = {state['result']}"
        print(state['answer'])
        return state


class DivisionErrorNode:
    def __call__(self, state: AgentState) -> AgentState:
        state['result'] = 0
        state['answer'] = "Divide by Zero ERROR"   # <- was missing '=' in your draft
        print(state['answer'])
        return state


class EndEdgeNode:
    def __call__(self, state: AgentState) -> AgentState:
        state['answer'] = "Program Terminated!"
        print(state['answer'])
        return state


# ---------------------------------------------------------------------------
# Build the graph
# ---------------------------------------------------------------------------
graph = StateGraph(AgentState)

greeting_message_node = GreetingsNode()
user_input_node = GetUserInputNode()

add_node = AddNode()
subtract_node = SubtractNode()
multiplier_node = MultiplierNode()
division_node = DivisionNode()

operator_router_node = OperatorDecisionNode()   # decision callable (router fn)
division_router_node = DivisionDecisionNode()   # decision callable (router fn)

operator_error_node = OperatorErrorNode()
division_error_node = DivisionErrorNode()

end_edge_node = EndEdgeNode()

# register real nodes
graph.add_node("greeting_message_node", greeting_message_node)
graph.add_node("user_input_node", user_input_node)

# passthrough nodes: identity function, so state in == state out.
# These exist purely to give the decision a position in the graph; the
# actual decision logic lives in the router callables above, wired in
# via add_conditional_edges below — never passed to add_node.
graph.add_node("operator_router_node", lambda state: state)
graph.add_node("division_router_node", lambda state: state)

graph.add_node("add_node", add_node)
graph.add_node("subtract_node", subtract_node)
graph.add_node("multiplier_node", multiplier_node)
graph.add_node("division_node", division_node)

graph.add_node("operator_error_node", operator_error_node)
graph.add_node("division_error_node", division_error_node)

graph.add_node("end_edge_node", end_edge_node)

# fixed edges
graph.add_edge(START, "greeting_message_node")
graph.add_edge("greeting_message_node", "user_input_node")

# user_input_node -> operator_router_node is a PLAIN edge (not conditional).
# The decision happens one step later, once we're sitting at the
# passthrough node — this is what makes it consistent with how division
# is handled below.
graph.add_edge("user_input_node", "operator_router_node")

graph.add_conditional_edges(
    "operator_router_node",       # source: the passthrough node
    operator_router_node,         # router: the OperatorDecisionNode instance
    {
        "exit_node_edge": "end_edge_node",
        "add_node_edge": "add_node",
        "subtract_node_edge": "subtract_node",
        "multiplier_node_edge": "multiplier_node",
        "division_node_decision_edge": "division_router_node",
        "operator_error_edge": "operator_error_node",
    },
)

graph.add_conditional_edges(
    "division_router_node",       # source: the passthrough node
    division_router_node,         # router: the DivisionDecisionNode instance
    {
        "divide_by_zero_edge": "division_error_node",
        "division_node_edge": "division_node",
    },
)

# every terminal calculation/error node loops back for another round
graph.add_edge("add_node", "user_input_node")
graph.add_edge("subtract_node", "user_input_node")
graph.add_edge("multiplier_node", "user_input_node")
graph.add_edge("division_node", "user_input_node")
graph.add_edge("division_error_node", "user_input_node")
graph.add_edge("operator_error_node", "user_input_node")

# quitting ends the graph
graph.add_edge("end_edge_node", END)

app = graph.compile()


def visualize_graph() -> None:
    """Optional: call manually if you want to see the graph structure.
    Needs network access (LangGraph renders via the mermaid.ink API)."""
    png_bytes = app.get_graph().draw_mermaid_png()
    img = mpimg.imread(io.BytesIO(png_bytes), format="png")
    plt.imshow(img)
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    initial_state: AgentState = {
        "num1": 0.0,
        "num2": 0.0,
        "operator": "",
        "result": 0.0,
        "answer": "",
    }
    # default recursion_limit (25) counts graph steps, not loop iterations —
    # raised generously since this loop is meant to run until the user quits
    app.invoke(initial_state, config={"recursion_limit": 1000})















