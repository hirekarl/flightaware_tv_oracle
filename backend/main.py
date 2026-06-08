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
from fastapi.responses import StreamingResponse

from backend import __version__
from backend.agents.coordinator import CoordinatorAgent
from backend.models.flight import FlightState, OperationalStatus
from backend.simulation import generate_mock_fleet

logger = logging.getLogger(__name__)

_cors_origins = [
    o.strip()
    for o in os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")
    if o.strip()
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


app = FastAPI(
    title="FlightAware TV Oracle",
    version=__version__,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_methods=["GET"],
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


async def _enrich_flight(
    coordinator: CoordinatorAgent, flight: FlightState
) -> FlightState:
    """Return flight with AI analysis; NORMAL flights pass through unchanged."""
    if flight.operationalStatus == OperationalStatus.NORMAL:
        return flight
    t0 = time.perf_counter()
    ai_analysis = await coordinator.analyze(flight)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    logger.info(
        "analyzed flight=%s status=%s elapsed_ms=%.1f",
        flight.flightId,
        flight.operationalStatus,
        elapsed_ms,
    )
    return flight.model_copy(update={"aiAnalysis": ai_analysis})


async def _sse_fleet_stream() -> AsyncGenerator[str, None]:
    """Yield SSE-formatted fleet state payloads every 5 seconds.

    WARNING and CRITICAL flights receive AI-generated analysis via CoordinatorAgent;
    NORMAL flights are passed through with their simulation data unchanged.
    """
    coordinator = CoordinatorAgent()
    while True:
        fleet = generate_mock_fleet()
        enriched = await asyncio.gather(
            *[_enrich_flight(coordinator, f) for f in fleet]
        )
        payload = json.dumps([f.model_dump() for f in enriched])
        yield f"data: {payload}\n\n"
        await asyncio.sleep(5)


@app.get("/api/fleet/stream")
async def stream_fleet() -> StreamingResponse:
    """SSE endpoint — pushes live fleet state updates to connected clients."""
    return StreamingResponse(
        _sse_fleet_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
