"""
Real Estate MCP Server

A comprehensive Model Context Protocol server for real estate data management.
Provides tools, resources, and prompts for property listings, agent management,
market analysis, client relationships, and area intelligence.
"""

import asyncio
import sys

from mcp.server.fastmcp import FastMCP

from prompts import register_all_prompts
from resources import (
    register_agent_resources,
    register_client_resources,
    register_location_resources,
    register_market_resources,
    register_property_resources,
)
from tools.agent_tools import register_agent_tools
from tools.area_tools import register_area_tools
from tools.client_tools import register_client_tools
from tools.market_tools import register_market_tools

# Import all component registration functions
from tools.property_tools import register_property_tools
from tools.system_tools import register_system_tools
from utils import data_manager

# Create the FastMCP server
mcp = FastMCP("Real Estate MCP Server")


def register_all_components():
    """Register all tools, resources, and prompts with the MCP server"""

    # Register all tool categories
    register_property_tools(mcp)
    register_agent_tools(mcp)
    register_market_tools(mcp)
    register_client_tools(mcp)
    register_area_tools(mcp)
    register_system_tools(mcp)

    # Register all resources
    register_property_resources(mcp)
    register_agent_resources(mcp)
    register_market_resources(mcp)
    register_client_resources(mcp)
    register_location_resources(mcp)

    # Register all prompts
    register_all_prompts(mcp)


async def main():
    """Main server function with transport selection"""
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stderr)]
    )
    logger = logging.getLogger(__name__)
    
    # Register all components
    register_all_components()

    # Log startup information to stderr
    logger.info("Real Estate MCP Server Starting...")
    logger.info(f"Loaded {len(data_manager.get_all_properties())} properties")
    logger.info(f"Loaded {len(data_manager.get_all_agents())} agents")
    logger.info(f"Loaded {len(data_manager.get_all_clients())} clients")
    logger.info(f"Loaded {len(data_manager.get_recent_sales())} recent sales")
    logger.info(f"Loaded {len(data_manager.get_all_areas())} areas")

    # Get Railway Vars
    import os
    # Determine transport mode from command line arguments
    transport = "stdio"  # Default to stdio for Claude Desktop compatibility
    if len(sys.argv) > 1:
        transport = sys.argv[1].lower()

    if transport == "sse":
        host = os.environ.get("HOST", "0.0.0.0")
        port = int(os.environ.get("PORT", "8000"))

        logger.info(f"Running with SSE transport on http://{host}:{port}/sse")
        await mcp.run_sse_async(host=host, port=port)
    else:
        # Run with STDIO transport for Claude Desktop
        logger.info("Running with STDIO transport")
        await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
