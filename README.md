# divmcp

HTTP MCP service for dividend tools.

This service is intentionally separate from `divcore`.

```text
Agent -> divmcp /mcp -> divcore FastAPI -> DB/services/RAG
```

## Quick Start

Set the backend connection:

```bash
DIVCORE_BASE_URL=http://127.0.0.1:8000
DIVCORE_AUTH_USERNAME=mcp
DIVCORE_ADMIN_PASSWORD=admin123
```

Start the service:

```bash
uv run fastapi dev
```

Useful endpoints:

- `GET /health`
- `POST /mcp`
- `/docs` for the debug REST wrappers that are exposed as MCP tools

## Tools

- `get_dividend_snapshot`
- `get_dividend_by_symbol`
- `get_universe_symbols`
- `refresh_nasdaq_calendar`
- `refresh_symbol_universe`
- `search_dividend_rag`

## Project Structure

- `main.py` - deployable FastAPI host that mounts MCP at `/mcp`
- `divmcp/backend_client.py` - HTTP client for divcore
- `divmcp/tools.py` - MCP-exposed tool wrappers
