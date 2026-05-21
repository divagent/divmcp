from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from divmcp.backend_client import DivcoreClient


router = APIRouter(prefix="/tools", tags=["mcp-tools"])


class RagSearchRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(5, ge=1, le=20)


@router.get(
    "/dividend-snapshot",
    operation_id="get_dividend_snapshot",
    summary="Return the current dividend snapshot from divcore.",
)
async def get_dividend_snapshot(
    limit: int = Query(100, ge=1, le=1000),
) -> dict[str, Any]:
    rows = await DivcoreClient().get_dividend_snapshot(limit=limit)
    return {"count": len(rows), "items": rows}


@router.get(
    "/dividend-by-symbol/{symbol}",
    operation_id="get_dividend_by_symbol",
    summary="Return dividend rows for one ticker symbol.",
)
async def get_dividend_by_symbol(symbol: str) -> dict[str, Any]:
    rows = await DivcoreClient().get_dividend_by_symbol(symbol=symbol)
    return {"symbol": symbol.upper(), "count": len(rows), "items": rows}


@router.get(
    "/universe-symbols",
    operation_id="get_universe_symbols",
    summary="Return curated dividend symbol universe entries.",
)
async def get_universe_symbols(
    limit: int = Query(1000, ge=1, le=10000),
) -> dict[str, Any]:
    rows = await DivcoreClient().get_universe_symbols(limit=limit)
    return {"count": len(rows), "items": rows}


@router.post(
    "/refresh-nasdaq-calendar",
    operation_id="refresh_nasdaq_calendar",
    summary="Trigger divcore Nasdaq dividend refresh.",
)
async def refresh_nasdaq_calendar() -> dict[str, Any]:
    return await DivcoreClient().refresh_nasdaq_calendar()


@router.post(
    "/refresh-symbol-universe",
    operation_id="refresh_symbol_universe",
    summary="Trigger divcore symbol universe refresh.",
)
async def refresh_symbol_universe() -> dict[str, Any]:
    return await DivcoreClient().refresh_symbol_universe()


@router.post(
    "/search-dividend-rag",
    operation_id="search_dividend_rag",
    summary="Search dividend RAG through divcore.",
)
async def search_dividend_rag(payload: RagSearchRequest) -> dict[str, Any]:
    return await DivcoreClient().search_dividend_rag(
        question=payload.question,
        top_k=payload.top_k,
    )
