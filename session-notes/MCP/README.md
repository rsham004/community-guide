# Session Notes: Model Context Protocol (MCP)

These notes cover the concepts, technologies, and implementation patterns related to the Model Context Protocol (MCP). MCP provides a standardized way for Large Language Models (LLMs) and AI Agents to interact with external tools and services.

## Reading Order & File Overview

It's recommended to read these notes sequentially:

1.  **[01-MCP-overview.md](./01-MCP-overview.md):** Introduces the core concepts of MCP, the problems it solves, its components, and its potential. Start here for a foundational understanding.
2.  **[02-SSE.md](./02-SSE.md):** Explains Server-Sent Events (SSE), a key technology used for real-time communication in some MCP implementations, including the native n8n nodes and the custom Python server example.
3.  **[03-N8N-selfhost+mcp.md](./03-N8N-selfhost+mcp.md):** A practical guide on setting up a self-hosted instance of n8n, which can act as an MCP server. This covers the initial setup required before configuring the MCP connection.
4.  **[04-N8N-ServerNode.md](./04-N8N-ServerNode.md):** Details the native `MCP Server Trigger` and `MCP Client Tool` nodes introduced in n8n v1.88. This explains *how* to configure n8n (once self-hosted per file 03) to act as an MCP server for clients like Claude Desktop or Cursor.
5.  **[05-BuildingMCP.md](./05-BuildingMCP.md):** Provides a step-by-step guide to building a custom MCP server from scratch using Python, Starlette, SSE (FastMCP), and deploying it to Google Cloud Run. This serves as an alternative or more advanced implementation compared to using n8n.

These notes aim to provide both conceptual understanding and practical guidance for working with MCP.

---
*Licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/)*
*Visit [ProductFoundry.ai](https://productfoundry.ai)*
