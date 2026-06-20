# Instructor + google-genai

**Versions:** `instructor>=1.7`, `google-genai>=2.0` (current: 2.8.0 as of 2026-06-08)
**Role:** Structured LLM output layer. `CoordinatorAgent` sends an FBO operator brief
prompt and gets back a validated `AiAnalysis` Pydantic model — no JSON parsing, no
schema wrangling.

---

## Key Patterns

### Recommended: from_provider (async)
```python
import instructor

client = instructor.from_provider("google/gemini-2.5-flash", async_client=True)
# Reads GOOGLE_API_KEY from environment automatically.

analysis: AiAnalysis = await client.create(
    response_model=AiAnalysis,
    messages=[{"role": "user", "content": prompt}],
)
```
This is the preferred pattern — no manual `genai.Client` construction needed.

### Alternative: explicit client via from_genai (v2 API)
```python
from google.genai import Client
from instructor.v2 import from_genai
from instructor import Mode

raw_client = Client(api_key=os.environ["GOOGLE_API_KEY"])
client = from_genai(raw_client, mode=Mode.TOOLS)   # sync
```
Use this when you need explicit API key control or non-standard client config.

### Available modes
| Mode | Mechanism | Status |
|---|---|---|
| `Mode.TOOLS` | Function calling — auto-filters Gemini thought parts | **Preferred** |
| `Mode.JSON` | JSON schema structured response | Supported |
| `Mode.GEMINI_JSON` | Legacy alias → maps to `Mode.JSON` | Deprecated (emits warning) |

### Models (use the `"google/<model>"` provider string)
| Model | Best for |
|---|---|
| `"google/gemini-2.5-flash"` | Low-latency structured output ← **our default** |
| `"google/gemini-2.5-pro"` | Higher reasoning depth, slower |

### Streaming
```python
# Stream a partial model as it's generated
async for partial in client.create_partial(
    response_model=AiAnalysis,
    messages=[{"role": "user", "content": prompt}],
):
    ...  # partial is an AiAnalysis with some fields filled

# Extract multiple objects from one response
async for item in client.create_iterable(
    response_model=AiAnalysis,
    messages=[{"role": "user", "content": prompt}],
):
    ...
```

### Prompt design: use Field descriptions as implicit constraints
```python
class AiAnalysis(BaseModel):
    summaryTitle: str = Field(description="One-line title for the operator card.")
    rootCause: str = Field(description="Single dense sentence identifying the cause.")
```
These flow into the JSON schema Instructor sends to the model and act as constraints,
not documentation.

---

## Gotchas

- **No `Union` or `Optional` types** in structured output models when using
  `Mode.TOOLS` or `Mode.JSON`. Instructor raises an error if it detects these.
  Use required fields with sentinel values or separate models instead.
- **Gemini 2.5 thought parts** (internal reasoning tokens) are automatically stripped
  by Instructor before validation — no manual filtering needed.
- **`GOOGLE_API_KEY`** is what `from_provider` reads from the environment (not
  `GEMINI_API_KEY`). Both refer to the same Gemini Developer API key — just the
  env var name differs.
- **Retry on validation failure** — Instructor retries malformed responses up to 3
  times by default. Tune with `max_retries=N` in the `create()` call.
- **Old SDK imports are gone** — `from instructor import from_gemini` (the old
  helper for `google-generativeai`) is replaced by `from_provider` or
  `from instructor.v2 import from_genai`. Do not mix old and new APIs.

---

## Resources

- https://python.useinstructor.com/integrations/genai/ (Instructor google-genai integration — fetched 2026-06-08)
- https://pypi.org/project/google-genai/ (google-genai PyPI, v2.8.0 — fetched 2026-06-08)
