from langgraph.graph import StateGraph, END
from graph.state import AgentState
from agents.planner import planner_agent
from agents.searcher import searcher_agent
from agents.writer import writer_agent
from agents.critic import critic_agent


def should_continue(state: AgentState) -> str:
    if state["is_satisfactory"] or state.get("revision_count", 0) >= 3:
        return "end"
    return "revise"


def build_graph():
    graph = StateGraph(AgentState)

    # add the 4 agents as nodes
    graph.add_node("planner", planner_agent)
    graph.add_node("searcher", searcher_agent)
    graph.add_node("writer", writer_agent)
    graph.add_node("critic", critic_agent)

    # set the entry point
    graph.set_entry_point("planner")

    # linear edges
    graph.add_edge("planner", "searcher")
    graph.add_edge("searcher", "writer")
    graph.add_edge("writer", "critic")

    # conditional edge — loop back to writer or stop
    graph.add_conditional_edges(
        "critic",
        should_continue,
        {
            "revise": "writer",
            "end": END
        }
    )

    return graph.compile()
