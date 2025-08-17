from langchain_mcp_adapters.client import MultiServerMCPClient

from agent_basil.components.graph import create_agent_graph
from agent_basil.components.llm import get_llm
from agent_basil.components.tools import send_task_to_human, wait_1_minute


async def start_agent_basil():
    client = MultiServerMCPClient(
        {
            "camera": {
                "url": "http://localhost:8000/mcp/",
                "transport": "streamable_http",
            },
            "climate_irrigation": {
                "url": "http://localhost:8001/mcp/",
                "transport": "streamable_http",
            },
        }
    )
    tools = await client.get_tools()
    tools.extend(
        [
            send_task_to_human,
            wait_1_minute,
        ]
    )
    llm = get_llm()
    agent = create_agent_graph(tools, llm)

    async for event in agent.astream(input={}, stream_mode="updates"):
        print(event)
