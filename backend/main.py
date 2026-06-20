"""FlightAware TV — AI Fleet Disruption Oracle API."""

import asyncio
import json
import logging
import os
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, StreamingResponse
from pydantic import BaseModel

from backend import __version__
from backend.agents.coordinator import CoordinatorAgent
from backend.models.flight import FlightState
from backend.simulation import _engine, generate_mock_fleet

_cors_origins = [
    o.strip()
    for o in os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")
    if o.strip()
]

_logger = logging.getLogger(__name__)

_SSE_RETRY_AFTER = 5


class BeatResponse(BaseModel):
    beat: int
    name: str


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize shared resources for the application lifetime."""
    app.state.coordinator = CoordinatorAgent()
    app.state.max_sse_connections = int(os.environ.get("SSE_MAX_CONNECTIONS", "10"))
    app.state.active_sse_connections = 0
    yield


app = FastAPI(
    title="FlightAware TV Oracle",
    version=__version__,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}


@app.get("/api/fleet", response_model=list[FlightState])
async def get_fleet() -> list[FlightState]:
    """Return a snapshot of the current fleet states."""
    return generate_mock_fleet()


@app.get("/demo/status", response_model=BeatResponse)
async def demo_status() -> BeatResponse:
    """Return the current demo scenario beat without advancing it."""
    return BeatResponse(beat=_engine.beat_index, name=_engine.beat_name)


@app.post("/demo/next", response_model=BeatResponse)
async def demo_next() -> BeatResponse:
    """Advance the demo scenario to the next beat and return the new state."""
    idx, name = _engine.advance()
    return BeatResponse(beat=idx, name=name)


@app.post("/demo/reset", response_model=BeatResponse)
async def demo_reset() -> BeatResponse:
    """Reset the demo scenario to beat 0."""
    _engine.reset()
    return BeatResponse(beat=_engine.beat_index, name=_engine.beat_name)


async def _enrich_flight(
    coordinator: CoordinatorAgent, flight: FlightState
) -> tuple[FlightState, dict[str, str]]:
    forecast_title = flight.aiAnalysis.summaryTitle
    analysis = await coordinator.analyze(flight)
    return (
        flight.model_copy(update={"aiAnalysis": analysis}),
        {
            "flight_id": flight.flightId,
            "status": str(flight.operationalStatus),
            "forecast_title": forecast_title,
            "actual_title": analysis.summaryTitle,
        },
    )


async def _sse_fleet_stream(
    coordinator: CoordinatorAgent,
) -> AsyncGenerator[str, None]:
    while True:
        start = time.monotonic()
        fleet = generate_mock_fleet()
        results = await asyncio.gather(*[_enrich_flight(coordinator, f) for f in fleet])
        analyzed = [r[0] for r in results]
        flight_metrics = [r[1] for r in results]
        elapsed_ms = round((time.monotonic() - start) * 1000, 3)
        _logger.info(
            "sse_cycle_complete",
            extra={
                "fleet_size": len(fleet),
                "elapsed_ms": elapsed_ms,
                "flights": flight_metrics,
            },
        )
        payload = json.dumps([f.model_dump() for f in analyzed])
        yield f"data: {payload}\n\n"
        await asyncio.sleep(5)


@app.get("/api/fleet/stream", response_model=None)
async def stream_fleet() -> Response:
    """SSE endpoint — pushes live fleet state updates to connected clients.

    Returns 429 with a Retry-After header when the concurrent connection limit
    is reached. Otherwise increments the active connection count and streams
    fleet state events, decrementing the count when the connection closes.
    """
    if app.state.active_sse_connections >= app.state.max_sse_connections:
        return JSONResponse(
            {"detail": "Too many concurrent SSE connections. Try again later."},
            status_code=429,
            headers={"Retry-After": str(_SSE_RETRY_AFTER)},
        )

    coordinator: CoordinatorAgent = app.state.coordinator
    app.state.active_sse_connections += 1

    async def _guarded_stream() -> AsyncGenerator[str, None]:
        try:
            async for chunk in _sse_fleet_stream(coordinator):
                yield chunk
        finally:
            app.state.active_sse_connections -= 1

    return StreamingResponse(
        _guarded_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
