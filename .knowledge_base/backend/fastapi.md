# FastAPI + Uvicorn

**Version:** `fastapi[standard]>=0.115`, `uvicorn[standard]>=0.32`
**Role:** HTTP framework for the Oracle API. Owns the `/api/fleet` snapshot endpoint,
the `/api/fleet/stream` SSE endpoint, and the `/health` liveness probe. Startup/shutdown
managed via `lifespan`.

---

## Key Patterns

### Lifespan (startup / shutdown)
```python
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # setup — initialize CoordinatorAgent, warm connections, etc.
    yield
    # teardown

app = FastAPI(lifespan=lifespan)
```
Use `lifespan` — not the deprecated `@app.on_event` — to initialize `CoordinatorAgent`
once at startup rather than per-request.

### SSE endpoint
```python
from fastapi.responses import StreamingResponse
import asyncio, json

async def _stream() -> AsyncGenerator[str, None]:
    while True:
        payload = json.dumps([f.model_dump() for f in get_fleet()])
        yield f"data: {payload}\n\n"   # double newline is required by SSE spec
        await asyncio.sleep(5)

@app.get("/api/fleet/stream")
async def stream_fleet() -> StreamingResponse:
    return StreamingResponse(
        _stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```
`X-Accel-Buffering: no` prevents nginx from buffering the stream in production.

### Typed response models
```python
@app.get("/api/fleet", response_model=list[FlightState])
async def get_fleet() -> list[FlightState]:
    return generate_mock_fleet()
```
Always declare `response_model=` on endpoints returning Pydantic types. FastAPI
serializes via `.model_dump()` automatically. Never return raw dicts.

### Dependency injection
```python
from fastapi import Depends

async def get_coordinator() -> CoordinatorAgent:
    return CoordinatorAgent()

@app.get("/api/fleet/{flight_id}/analyze")
async def analyze(
    flight_id: str,
    coordinator: CoordinatorAgent = Depends(get_coordinator),
) -> AiAnalysis:
    ...
```

### Running locally
```bash
uv run uvicorn backend.main:app --reload       # dev, auto-reload on change
uv run fastapi dev backend/main.py             # alternative: FastAPI CLI dev mode
```

---

## Gotchas

- `fastapi[standard]` includes python-multipart, email-validator, and the FastAPI CLI.
  The `[standard]` extra is what adds httpx for testing — without it, `TestClient`
  is not available.
- `StreamingResponse` with `text/event-stream` requires the generator to yield
  `data: ...\n\n` format exactly. A single `\n` will not flush to the client.
- Blocking calls (e.g., sync Instructor/Gemini calls) inside `async def` stall the
  event loop. Wrap with `await asyncio.to_thread(...)`.
- CORS `allow_origins` must include the Vite dev server (`http://localhost:5173`), or
  the frontend SSE connection will be silently rejected by the browser.
- FastAPI auto-generates `/docs` (Swagger UI) and `/redoc`. Both are enabled by
  default in development — useful for manually testing endpoints before the frontend
  is wired up.
- `response_model=` triggers validation on the *output* — if the agent returns a
  dict instead of a typed model, FastAPI will attempt coercion and may silently
  drop unknown fields. Always return typed models.

---

## Resources

- https://fastapi.tiangolo.com/ (FastAPI docs homepage — fetched 2026-06-08)
<!-- Drop additional links here — Archivist will synthesize -->
