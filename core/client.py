import asyncio
from typing import Optional, List, Dict, Any
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client

from config.logging_config import logger
from utils.error_handlers import ClientConnectionError, ToolExecutionError

class MCPClient:
    def __init__(self):
        """Initialize the MCP client."""
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self._streams_context = None
        self._session_context = None
        self._connected = False
        self._available_tools = None

    async def connect_to_sse_server(self, server_url: str):
        """Connect to an MCP server running with SSE transport."""
        try:
            logger.info(f"Connecting to MCP server at {server_url}")
            
            # Store the context managers so they stay alive
            self._streams_context = sse_client(url=server_url)
            streams = await self._streams_context.__aenter__()

            self._session_context = ClientSession(*streams)
            self.session: ClientSession = await self._session_context.__aenter__()

            # Initialize
            await self.session.initialize()
            
            # List available tools to verify connection
            response = await self.session.list_tools()
            tools = response.tools
            
            tool_names = [tool.name for tool in tools]
            logger.info(f"Connected to server with tools: {tool_names}")
            
            self._connected = True
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {str(e)}")
            await self.cleanup()
            raise ClientConnectionError(f"Failed to connect to MCP server: {str(e)}")

    async def cleanup(self):
        """Properly clean up the session and streams."""
        logger.info("Cleaning up MCP client resources")
        try:
            if self._session_context:
                await self._session_context.__aexit__(None, None, None)
            if self._streams_context:
                await self._streams_context.__aexit__(None, None, None)
            
            self._connected = False
            self.session = None
            logger.info("MCP client resources cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get the list of available tools from the MCP server."""
        if not self._connected or not self.session:
            raise ClientConnectionError("MCP client is not connected")
            
        try:
            response = await self.session.list_tools()
            available_tools = [{
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            } for tool in response.tools]
            
            self._available_tools = available_tools
            return available_tools
        except Exception as e:
            logger.error(f"Failed to get available tools: {str(e)}")
            raise ClientConnectionError(f"Failed to get available tools: {str(e)}")

    async def call_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the MCP server."""
        if not self._connected or not self.session:
            raise ClientConnectionError("MCP client is not connected")
            
        try:
            logger.info(f"Calling tool {tool_name} with args: {tool_args}")
            result = await self.session.call_tool(tool_name, tool_args)
            logger.info(f"Tool {tool_name} executed successfully")
            print(f"Tool {tool_name} result: {result}")
            return {
                "content": result.content
            }
        except Exception as e:
            logger.error(f"Tool execution failed for {tool_name}: {str(e)}")
            raise ToolExecutionError(tool_name=tool_name, error=str(e))

    @property
    def is_connected(self) -> bool:
        """Return whether the client is connected."""
        return self._connected