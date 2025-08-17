import asyncio

from agent_basil.components.mcp_tools import (
    get_cam_mcp_server,
    get_climate_irrigation_mcp_server,
)


async def start_mcp_servers() -> None:
    """
    Create and return the MCP servers for the ESP 32 Cam and ESP 8266 Climate Irrigation.
    """
    cam_mcp_server = get_cam_mcp_server()
    climate_irrigation_mcp_server = get_climate_irrigation_mcp_server()

    cam_server_task = asyncio.create_task(
        cam_mcp_server.run_async(
            transport="http",
            host="127.0.0.1",
            port=8000,
        )
    )
    climate_irrigation_server_task = asyncio.create_task(
        climate_irrigation_mcp_server.run_async(
            transport="http",
            host="127.0.0.1",
            port=8001,
        )
    )

    await asyncio.gather(cam_server_task, climate_irrigation_server_task)
