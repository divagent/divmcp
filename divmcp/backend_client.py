from __future__ import annotations

from typing import Any

import httpx

from divmcp.config import get_settings


class DivcoreClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.DIVCORE_BASE_URL.rstrip("/")
        self.auth = (settings.DIVCORE_AUTH_USERNAME, settings.DIVCORE_ADMIN_PASSWORD)
        self.timeout = settings.DIVCORE_TIMEOUT_SECONDS

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        async with httpx.AsyncClient(
            base_url=self.base_url,
            auth=self.auth,
            timeout=self.timeout,
        ) as client:
            response = await client.request(method, path, params=params, json=json)
            response.raise_for_status()
            return response.json()

    async def get_dividend_snapshot(self, limit: int = 100) -> list[dict[str, Any]]:
        rows = await self._request("GET", "/div_show/list")
        return rows[:limit]

    async def get_dividend_by_symbol(self, symbol: str) -> list[dict[str, Any]]:
        return await self._request("GET", f"/div_show/by-symbol/{symbol.upper()}")

    async def get_universe_symbols(self, limit: int = 1000) -> list[dict[str, Any]]:
        return await self._request("GET", "/div_show/symbols", params={"limit": limit})

    async def refresh_nasdaq_calendar(self) -> dict[str, Any]:
        return await self._request("POST", "/div_inject/div_daily")

    async def refresh_symbol_universe(self) -> dict[str, Any]:
        return await self._request("POST", "/div_inject/div_yearly_symbol_list")

    async def search_dividend_rag(self, question: str, top_k: int = 5) -> dict[str, Any]:
        return await self._request(
            "POST",
            "/div_rag_contract/rag/query-contract",
            json={"question": question, "top_k": top_k},
        )
