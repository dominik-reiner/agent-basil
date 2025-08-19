from datetime import datetime
import json
from typing import cast

from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode

from agent_basil.components.agent import create_agent_basil
from agent_basil.config import PROJ_ROOT
from agent_basil.domain.graph_state import AgentState


def should_continue(state: AgentState):
    last_message: AIMessage = cast(AIMessage, state["messages"][-1])
    if not last_message.tool_calls:
        print("STOPPING: No tool calls in the last message.")
        return "end"
    else:
        return "continue"


def create_agent_graph(tools: list, llm: ChatGoogleGenerativeAI) -> CompiledStateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("agent", create_agent_basil(tools, llm))
    graph.add_node(
        "tools", ToolNode([tool for tool in tools if tool.name != "capture_image"])
    )

    graph.set_entry_point("agent")

    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END,
        },
    )

    graph.add_edge("tools", "agent")

    agent_graph = graph.compile()
    return agent_graph


def save_message(role: str, content: str):
    messages = load_messages()
    messages.append(
        (role, f"Turn from the {datetime.now().strftime('%Y-%m-%d')}: {content}")
    )
    with open(PROJ_ROOT / "messages.json", "w") as f:
        json.dump([{"role": r, "content": c} for r, c in messages], f, indent=2)


def load_messages():
    try:
        with open(PROJ_ROOT / "messages.json", "r") as f:
            messages_raw = json.load(f)
            return [(msg["role"], msg["content"]) for msg in messages_raw]
    except (FileNotFoundError, json.JSONDecodeError):
        return []
