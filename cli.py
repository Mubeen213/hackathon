#!/usr/bin/env python
import asyncio
import sys
from typing import Optional

from core.client import MCPClient
from core.chat_service import ChatService
from config.logging_config import logger

async def cli_chat_loop(chat_service: ChatService):
    """Run an interactive chat loop."""
    print("\nMCP Client Started!")
    print("Type your queries or 'quit' to exit.")
    
    context_id = "cli-session"
    
    while True:
        try:
            query = input("\nQuery: ").strip()
            
            if query.lower() == 'quit':
                break
                
            if query.lower() == 'clear':
                chat_service.clear_context(context_id)
                print("\nContext cleared.")
                continue
                
            result = await chat_service.process_query(query, context_id)
            print("\n" + result["response"])
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

async def main():
    """Main CLI entrypoint."""
    if len(sys.argv) < 2:
        print("Usage: python cli.py <URL of SSE MCP server (i.e. http://localhost:8080/sse)>")
        sys.exit(1)

    server_url = sys.argv[1]
    client = MCPClient()
    
    try:
        await client.connect_to_sse_server(server_url=server_url)
        chat_service = ChatService(client)
        await cli_chat_loop(chat_service)
    except Exception as e:
        logger.error(f"Error in CLI: {str(e)}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())