# Tech Stack

This document provides an index of key technologies used across foundational tools, infrastructure, development, protocol layers, deployment systems, and services. Each entry links to a corresponding document describing how it's used.

## 🧱 Foundational Tools

*   **Editor:** [VS Code](./foundational/VSCode.md)
*   **Languages:** [JavaScript](./foundational/JavaScript.md), [Python](./foundational/Python.md)

## 🛠️ Foundational Dev Tools

*   **Version Control:** [Git](./foundational_dev/Git-for-windows.md)
*   **Package Management:** [UV](./foundational_dev/UV.md)

## 🏗️ Infrastructure

*   **Database:** [Supabase](./infrastructure/Supabase.md) (PostgreSQL + BaaS)
*   **Automation:** [n8n](./infrastructure/n8n.md) (Workflow Automation)
*   **Containerization:** [Docker](./infrastructure/Docker.md)
*   **Cloud Hosting:** [Digital Ocean](./infrastructure/DigitalOcean.md)
*   **Testing:** [Playwright](./infrastructure/Playwright.md) (E2E Testing)

## 📡 Protocol & Middleware

*   **LLM Protocol:** [FastMCP](./protocol_middleware/FastMCP.md) (Python MCP Server Framework)
*   **API Framework:** [FastAPI](./protocol_middleware/FastAPI.md) (Python API Framework)

## 🛠️ Development Tools

| Category         | Subcategory      | Primary        | Secondary      | Tertiary       | Additional   |
|------------------|------------------|----------------|----------------|----------------|----------------|
| AI Core          | LLMs             | Claude, Gemini, GPT-4o | DeepSeek       | Qwen           |                |
| AI Core          | AI Tools         | Bolt.new       | Windsurf       | Cursor         | Bolt.diy       |
| AI Core          | Frameworks       | Pydantic AI    | LanGraph       |                | Flowise        |
| LLM Evaluation   | Tooling          | Custom Agents  | Bolt.diy       | ragas          | Phoenix        |
| Search           | AI Search        | Brave          | Firecrawl      | Perplexity.AI  | Search1.API    |

## 🚀 Deployment

| Category         | Subcategory      | Primary        | Secondary      | Tertiary       | Additional   |
|------------------|------------------|----------------|----------------|----------------|----------------|
| CI/CD            | Pipeline          | GitHub Actions |                |                |                |

## 💳 Services & Integration

| Category         | Subcategory      | Primary        | Secondary      | Tertiary       | Additional   |
|------------------|------------------|----------------|----------------|----------------|----------------|
| Payments         | Transactions      | Stripe         |                |                |                |

---

## 📝 Missing Tool Documentation

The following tools were mentioned in the `session-notes/MCP/` directory but do not yet have dedicated documentation files in the `/tools` structure:

*   **Cursor IDE / Cursor:** Referenced in `01-MCP-overview.md`, `03-N8N-selfhost+mcp.md`, `04-N8N-ServerNode.md`
*   **Claude Desktop:** Referenced in `01-MCP-overview.md`, `03-N8N-selfhost+mcp.md`, `04-N8N-ServerNode.md`
*   **Cline:** Referenced in `03-N8N-selfhost+mcp.md`
*   **Roo:** Referenced in `03-N8N-selfhost+mcp.md`
*   **Klein:** Referenced in `03-N8N-selfhost+mcp.md`
*   **Boomerang Tasks:** Referenced in `03-N8N-selfhost+mcp.md`
*   **Postgres:** Referenced in `03-N8N-selfhost+mcp.md` (Note: Supabase uses Postgres)
*   **Langchain:** Referenced in `03-N8N-selfhost+mcp.md`
*   **Instantly:** Referenced in `03-N8N-selfhost+mcp.md`
*   **Starlette:** Referenced in `05-BuildingMCP.md`
*   **uvicorn:** Referenced in `05-BuildingMCP.md`, `05a-BuildingMCP-Plan.md`
*   **Gemini:** Referenced in `05-BuildingMCP.md`, `05a-BuildingMCP-Plan.md`
*   **Google Cloud Run:** Referenced in `session-notes/MCP/05-BuildingMCP.md`, `session-notes/MCP/05a-BuildingMCP-Plan.md`
*   **gcloud (Google Cloud CLI):** Referenced in `session-notes/MCP/05-BuildingMCP.md`, `session-notes/MCP/05a-BuildingMCP-Plan.md`

The following tools were mentioned in `session-notes/Databases/01-Session-Overview.md` but do not yet have dedicated documentation files in the `/tools` structure:

*   **SQLModel:** ORM for Python.
*   **Prisma:** ORM for Node.js.
*   **SQLite:** Embedded database.
*   **React:** Frontend framework.
*   **sqlite-utils:** Python package.
*   **python-dotenv:** Python package.
*   **create-next-app / Next.js:** React framework/tooling.
*   **DB Browser for SQLite:** Database GUI tool.
*   **PostgREST:** Tool for creating REST API from Postgres DB (used by Supabase).
