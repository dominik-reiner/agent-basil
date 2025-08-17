import asyncio

import agent_basil.config  # noqa: F401
from agent_basil.services.graph_service import start_agent_basil
from agent_basil.services.mcp_service import start_mcp_servers


async def main():
    """
    This is the main entrypoint for the application.
    """
    task_mcp_server = asyncio.create_task(start_mcp_servers())
    task_agent = asyncio.create_task(start_agent_basil())

    # Wait for Agent basil loop to finish
    done, pending = await asyncio.wait(
        [task_mcp_server, task_agent], return_when=asyncio.FIRST_COMPLETED
    )

    # Cancel mcp server task
    for task in pending:
        task.cancel()
    # Wait for the cancelled mcp servers to finish their cleanup
    try:
        await asyncio.gather(*pending, *done)
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    asyncio.run(main())
