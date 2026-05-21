from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from divmcp.config import get_settings
from divmcp.tools import router as tools_router


app = FastAPI(
    title="Dividend MCP",
    version="0.1.0",
    description="HTTP MCP service exposing dividend tools backed by divcore.",
)

app.include_router(tools_router)


@app.get("/health", tags=["health"])
def health():
    settings = get_settings()
    return {
        "status": "ok",
        "divcore_base_url": settings.DIVCORE_BASE_URL,
    }


mcp = FastApiMCP(
    app,
    name="Dividend MCP",
    description="MCP tools for dividend snapshots, symbol universe, ingestion refresh, and RAG search.",
    include_tags=["mcp-tools"],
    describe_full_response_schema=True,
    describe_all_responses=True,
)
mcp.mount_http(mount_path="/mcp")
