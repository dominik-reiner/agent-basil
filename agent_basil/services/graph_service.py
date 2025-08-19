from langchain_mcp_adapters.client import MultiServerMCPClient

from agent_basil.components.graph import create_agent_graph, load_messages, save_message
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
    input = {"memory": load_messages()}
    final_message = None
    async for event in agent.astream(input=input, stream_mode="updates"):
        print(event)
        final_message = event
    if final_message:
        save_message("assistant", final_message["agent"]["messages"][0].content)
