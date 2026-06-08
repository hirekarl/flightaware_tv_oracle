# Pydantic v2

**Version:** `pydantic>=2.9` (current stable: 2.13.4)
**Role:** Enforces the frontend/backend data contract. Every API input and output is
a typed `BaseModel` subclass. No raw dicts cross module boundaries.

---

## Key Patterns

### Defining models (v2 style)
```python
from pydantic import BaseModel, Field
from enum import StrEnum

class OperationalStatus(StrEnum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class Telemetry(BaseModel):
    fuelRemainingMin: int = Field(ge=0)
    altitude: int = Field(ge=0)
```
`StrEnum` (Python 3.11+) makes enum values directly comparable to strings without
`.value` unwrapping — ideal for JSON serialization and pattern matching.

### Validating external data
```python
flight = FlightState.model_validate(raw_dict)       # replaces v1 parse_obj
flight = FlightState.model_validate_json(json_str)
```

### Serializing
```python
flight.model_dump()              # → dict
flight.model_dump_json()         # → JSON string
flight.model_dump(mode="json")   # → dict with JSON-safe types (enums as strings)
```

### Strict vs lax mode
By default Pydantic runs in **lax mode** — it coerces compatible types (e.g., `"1"` → `int`).
Enable **strict mode** per-field or globally to prevent coercion:
```python
class FlightState(BaseModel):
    model_config = ConfigDict(strict=True)
```
Strict mode is recommended at the SSE boundary to catch malformed payloads early.

### Field descriptions flow into Instructor prompts
```python
class AiAnalysis(BaseModel):
    summaryTitle: str = Field(description="One-line title for the dispatcher card.")
    rootCause: str = Field(description="Single dense sentence identifying the root cause.")
```
These descriptions appear in the JSON schema Instructor sends to Gemini — treat them
as implicit LLM instructions, not documentation.

### Immutable models (matches frontend `readonly`)
```python
class FlightState(BaseModel):
    model_config = ConfigDict(frozen=True)
```

---

## Gotchas

- v2 `model_dump()` replaces v1 `.dict()`. The old method still exists but emits a
  deprecation warning. Use `model_dump()` everywhere.
- `model_validate` (v2) replaces `parse_obj` (v1). Don't mix v1 and v2 APIs in the
  same codebase.
- `StrEnum` requires Python 3.11+. This project targets 3.12 — no issue.
- Nested models validate recursively. A `ValidationError` on a nested field surfaces
  the full path (e.g., `telemetry.fuelRemainingMin`).
- `model_config = ConfigDict(frozen=True)` enables hashing (`__hash__`) but raises
  `TypeError` on any field mutation attempt. Use it for value-object models.
- Pydantic v2 is Rust-powered — significantly faster than v1 for large validation
  volumes. The speed advantage matters for the SSE stream parsing path.

---

## Resources

- https://pydantic.dev/docs/validation/latest/get-started/ (Pydantic v2 docs — fetched 2026-06-08, v2.13.4)
<!-- Drop additional links here — Archivist will synthesize -->
