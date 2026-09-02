"""The FastMCP server instance and tool registration.

`stateless_http=True` + `json_response=True` make each request self-contained —
no server-side session state to keep — which is exactly what a serverless host
(FastAPI Cloud) needs. `streamable_http_path="/"` means that when `main.py` mounts
this app at `/mcp`, the MCP endpoint lands exactly at `/mcp` (not `/mcp/mcp`).
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="divmcp",
    instructions=(
        "Tools that give a dividend-analysis agent its REACH. The agent's job is to "
        "surface hard-to-get, often-unofficial leading signals that a company's "
        "dividend may be cut, suspended, or raised BEFORE any official announcement. "
        "Use `web_search` to DISCOVER sources you cannot name in advance, then "
        "`fetch_url` to READ the promising ones in full and corroborate a claim "
        "across several independent sources. Prefer agreement across sources plus "
        "recency over any single page. Always keep the URL you relied on so you can "
        "cite it; never state a hard figure you cannot point to."
    ),
    stateless_http=True,
    json_response=True,
    streamable_http_path="/",
)

# Register tools onto the instance above. Import placement (after `mcp` exists)
# keeps registration explicit and avoids circular imports.
from divmcp.tools import register_all  # noqa: E402

register_all(mcp)
