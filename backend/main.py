"""FlightAware TV — AI Fleet Disruption Oracle API."""

import asyncio
import json
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from backend.agents.coordinator import CoordinatorAgent
from backend.models.flight import FlightState
from backend.simulation import generate_mock_fleet

_cors_origins = [
    o.strip()
    for o in os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")
    if o.strip()
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize shared resources for the application lifetime."""
    app.state.coordinator = CoordinatorAgent()
    yield


app = FastAPI(
    title="FlightAware TV Oracle",
    version="0.1.0",
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


async def _sse_fleet_stream(
    coordinator: CoordinatorAgent,
) -> AsyncGenerator[str, None]:
    while True:
        fleet = generate_mock_fleet()
        analyzed: list[FlightState] = []
        for flight in fleet:
            analysis = await coordinator.analyze(flight)
            analyzed.append(flight.model_copy(update={"aiAnalysis": analysis}))
        payload = json.dumps([f.model_dump() for f in analyzed])
        yield f"data: {payload}\n\n"
        await asyncio.sleep(5)


@app.get("/api/fleet/stream")
async def stream_fleet() -> StreamingResponse:
    """SSE endpoint — pushes live fleet state updates to connected clients."""
    coordinator: CoordinatorAgent = app.state.coordinator
    return StreamingResponse(
        _sse_fleet_stream(coordinator),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
