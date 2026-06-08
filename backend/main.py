"""FlightAware TV — AI Fleet Disruption Oracle API."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from backend.models.flight import FlightState
from backend.simulation import generate_mock_fleet


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


app = FastAPI(
    title="FlightAware TV Oracle",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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


async def _sse_fleet_stream() -> AsyncGenerator[str, None]:
    """Yield SSE-formatted fleet state payloads every 5 seconds."""
    import asyncio
    import json

    while True:
        fleet = generate_mock_fleet()
        payload = json.dumps([f.model_dump() for f in fleet])
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
