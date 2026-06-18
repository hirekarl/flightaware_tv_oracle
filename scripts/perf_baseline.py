"""SSE throughput baseline — measures enrichment latency and concurrent connection behaviour.

Calls _enrich_flight() and stream_fleet() directly with a mocked CoordinatorAgent so
the numbers reflect asyncio.gather + Pydantic serialisation overhead without Gemini API
latency or the 5-second inter-cycle sleep.  Real-world numbers add Gemini round-trip
time per flight.

Usage:
    uv run python scripts/perf_baseline.py
"""

import asyncio
import json
import statistics
import time
from unittest.mock import AsyncMock, MagicMock

from backend.main import _enrich_flight, _sse_fleet_stream, app, stream_fleet
from backend.models.flight import AiAnalysis, FlightState
from backend.simulation import generate_mock_fleet


def _mock_coordinator() -> MagicMock:
    mock = MagicMock()
    mock.analyze = AsyncMock(
        return_value=AiAnalysis(
            summaryTitle="Baseline",
            rootCause="N/A",
            downstreamImpact="N/A",
            recommendedAction="N/A",
        )
    )
    return mock


async def _one_enrichment_cycle() -> tuple[float, int]:
    """Run one full fleet enrichment cycle. Returns (elapsed_us, fleet_size)."""
    coord = _mock_coordinator()
    fleet = generate_mock_fleet()
    t0 = time.monotonic()
    results = await asyncio.gather(*[_enrich_flight(coord, f) for f in fleet])
    elapsed_us = (time.monotonic() - t0) * 1_000_000
    payload = json.dumps([r[0].model_dump() for r in results])
    # Verify serialisation round-trip
    parsed = json.loads(payload)
    for item in parsed:
        FlightState(**item)
    return elapsed_us, len(fleet)


async def benchmark_enrichment_latency(cycles: int = 200) -> None:
    print(f"\n=== Enrichment latency — {cycles} cycles total (mock coordinator, no Gemini) ===")
    fleet_size = len(generate_mock_fleet())
    # Measure total wall time across many cycles for reliable timing on Windows
    t0 = time.perf_counter_ns()
    for _ in range(cycles):
        await _one_enrichment_cycle()
    total_ns = time.perf_counter_ns() - t0
    mean_us = (total_ns / cycles) / 1000
    print(f"  fleet size  {fleet_size} flights")
    print(f"  mean        {mean_us:.1f} µs/cycle")
    print(f"  throughput  {1_000_000 / mean_us:.0f} cycles/s (mock; excl. 5s sleep)")
    print("  note: real-world +200–800 ms per cycle for Gemini round-trip")


async def benchmark_concurrent_enrichment(connections: int, cycles_each: int = 10) -> None:
    print(f"\n=== {connections} concurrent connections — {cycles_each} cycles each ===")
    t0 = time.monotonic()
    results = await asyncio.gather(
        *[
            asyncio.gather(*[_one_enrichment_cycle() for _ in range(cycles_each)])
            for _ in range(connections)
        ]
    )
    wall_us = (time.monotonic() - t0) * 1_000_000
    all_us = [t for conn in results for t, _ in conn]
    total_events = sum(len(conn) for conn in results)
    print(f"  total events    {total_events}")
    print(f"  wall time       {wall_us / 1000:.0f} ms")
    print(f"  throughput      {total_events / (wall_us / 1_000_000):.0f} enrichments/s")
    print(f"  per-cycle mean  {statistics.mean(all_us):.0f} µs")
    print(f"  per-cycle p95   {sorted(all_us)[int(len(all_us) * 0.95)]:.0f} µs")
    print(f"  per-cycle max   {max(all_us):.0f} µs")


async def benchmark_first_sse_event(runs: int = 100) -> None:
    """Time from generator start to first event (no sleep on first iteration)."""
    print("\n=== Time-to-first-event (1 SSE connection) ===")
    total_ns = 0
    payload_size = 0
    for _ in range(runs):
        coord = _mock_coordinator()
        gen = _sse_fleet_stream(coord)
        try:
            t0 = time.perf_counter_ns()
            event = await gen.__anext__()
            total_ns += time.perf_counter_ns() - t0
            payload_size = len(json.loads(event[len("data: "):].strip()))
        finally:
            await gen.aclose()
    mean_us = (total_ns / runs) / 1000
    print(f"  mean {mean_us:.1f} µs  ({payload_size} flights in first payload, averaged over {runs} runs)")


async def benchmark_connection_limit() -> None:
    print("\n=== Connection limit (SSE_MAX_CONNECTIONS=10) ===")
    app.state.max_sse_connections = 10
    app.state.coordinator = _mock_coordinator()

    app.state.active_sse_connections = 10
    response = await stream_fleet()
    assert response.status_code == 429, f"Expected 429, got {response.status_code}"
    assert response.headers["retry-after"] == "5"
    print("  11th connection → 429 Too Many Requests (Retry-After: 5s) ✓")

    app.state.active_sse_connections = 9
    response = await stream_fleet()
    assert response.status_code == 200
    print("  10th connection → 200 StreamingResponse ✓")

    app.state.active_sse_connections = 0


async def main() -> None:
    print("FlightAware TV — SSE performance baseline")
    print("Coordinator: mocked  |  Gemini latency: excluded  |  inter-cycle sleep: excluded")

    await benchmark_enrichment_latency()
    await benchmark_concurrent_enrichment(connections=5, cycles_each=10)
    await benchmark_concurrent_enrichment(connections=10, cycles_each=10)
    await benchmark_first_sse_event()
    await benchmark_connection_limit()

    print("\nDone.  Add GOOGLE_API_KEY and rerun against the live coordinator for")
    print("real-world numbers (expect +200–800ms per cycle for Gemini round-trips).")


if __name__ == "__main__":
    asyncio.run(main())
