import httpx
from fastmcp import FastMCP


def get_cam_mcp_server():
    """
    Create and return the MCP server for the ESP 32 Cam.
    """
    client_cam = httpx.AsyncClient(base_url="http://esp32cam.local/")

    # Define a simplified OpenAPI spec for ESP 32 Cam
    openapi_spec_cam = {
        "openapi": "3.0.0",
        "info": {"title": "ESP 32 Cam", "version": "1.0"},
        "paths": {
            "/capture_base64": {
                "get": {
                    "summary": "Capture an image",
                    "operationId": "capture_image",
                    "responses": {
                        "200": {"description": "Image captured successfully."}
                    },
                }
            },
        },
    }

    mcp = FastMCP.from_openapi(
        openapi_spec=openapi_spec_cam, client=client_cam, name="ESP 32 Cam MCP Server"
    )
    return mcp


def get_climate_irrigation_mcp_server():
    """
    Create and return the MCP server for the ESP 8266 Climate Irrigation.
    """
    # Create an HTTP client for the target API
    client_climate_irrigation = httpx.AsyncClient(base_url="http://esp8266-irrigation/")

    # Define a simplified OpenAPI spec for ESP 32 Cam
    openapi_spec_climate_irrigation = {
        "openapi": "3.0.0",
        "info": {"title": "ESP 8266 Climate Irrigation", "version": "1.0"},
        "paths": {
            "/soil_moisture": {
                "get": {
                    "summary": "Get soil moisture",
                    "operationId": "get_soil_moisture",
                    "responses": {
                        "200": {
                            "description": "Soil moisture data retrieved successfully."
                        }
                    },
                }
            },
            "/climate": {
                "get": {
                    "summary": "Get climate data",
                    "operationId": "get_climate_data",
                    "responses": {
                        "200": {"description": "Climate data retrieved successfully."}
                    },
                }
            },
            "/irrigate": {
                "get": {
                    "summary": "Trigger irrigation",
                    "operationId": "trigger_irrigation",
                    "responses": {
                        "200": {"description": "Irrigation triggered successfully."}
                    },
                }
            },
        },
    }
    mcp = FastMCP.from_openapi(
        openapi_spec=openapi_spec_climate_irrigation,
        client=client_climate_irrigation,
        name="ESP 8266 Climate Irrigation MCP Server",
    )
    return mcp
