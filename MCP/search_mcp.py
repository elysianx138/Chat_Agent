import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from MCP.mcp_stores import mcp_tools


async def search_website():
    client = MultiServerMCPClient({
        "bright_data": {
            "url": f"https://mcp.brightdata.com/sse?token={os.getenv('SEARCH_API')}",
            "transport": "sse",
        }
    })

    search_website_tools = await client.get_tools()
    mcp_tools.clear()
    mcp_tools.extend(search_website_tools)
    return search_website_tools