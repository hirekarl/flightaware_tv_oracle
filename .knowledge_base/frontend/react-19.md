# React 19

**Version:** 19.x
**Role:** UI framework. Owns the fleet queue display, `FlightCard` visual states, and
the `AiImpactDrawer`. The `useFleetStream` hook consumes the backend SSE endpoint.

---

## Key Patterns

### New hooks relevant to this dashboard

**`useActionState`** — async operations with automatic pending/error tracking:
```tsx
const [error, submitAction, isPending] = useActionState(
  async (prevState, formData) => {
    const err = await doSomething(formData);
    return err ?? null;
  },
  null,
);
```
Use this for any user-triggered data mutation (e.g., acknowledging a disruption alert).

**`useOptimistic`** — show optimistic UI while a mutation is in-flight:
```tsx
const [optimisticStatus, setOptimistic] = useOptimistic(flight.operationalStatus);
```
Useful if dispatchers can manually override a flight status before the backend confirms.

**`use(promise)`** — read a promise or context in render (suspends until resolved):
```tsx
const flights = use(flightsPromise); // component suspends until data is ready
```
Pair with `<Suspense fallback={<LoadingSkeleton />}>` for the fleet queue initial load.

### `ref` as a prop (no more `forwardRef`)
```tsx
function FlightCard({ flight, ref }: { flight: FlightState; ref: React.Ref<HTMLElement> }) {
  return <article ref={ref} data-status={flight.operationalStatus}>{...}</article>;
}
```

### Context as provider (no `.Provider`)
```tsx
<FleetContext value={fleetState}>
  <FlightQueue />
</FleetContext>
// Instead of: <FleetContext.Provider value={fleetState}>
```

### Document metadata in components
```tsx
function FlightQueue() {
  return (
    <>
      <title>FlightAware TV — {criticalCount} Critical</title>
      <FlightList flights={flights} />
    </>
  );
}
```
React 19 hoists `<title>` to `<head>` automatically.

### SSE client hook pattern
```tsx
function useFleetStream(url: string) {
  const [fleet, setFleet] = useState<FlightState[]>([]);

  useEffect(() => {
    const source = new EventSource(url);
    source.onmessage = (e) => setFleet(JSON.parse(e.data) as FlightState[]);
    return () => source.close();
  }, [url]);

  return fleet;
}
```

---

## Breaking Changes from React 18

- **`forwardRef` deprecated** — use `ref` as a direct prop
- **`Context.Provider` deprecated** — use `<Context value={...}>` directly
- **`useFormState` renamed** → `useActionState`
- **Ref callbacks** can now return cleanup functions (like `useEffect`)
- **`useDeferredValue`** accepts an optional `initialValue` parameter

---

## Gotchas

- `EventSource` is not available in jsdom (Vitest environment). Mock it in
  `src/test/setup.ts`:
  ```typescript
  globalThis.EventSource = class MockEventSource { ... } as unknown as typeof EventSource;
  ```
- `use(promise)` only suspends — it does not catch errors. Wrap in an Error Boundary
  or use `useActionState` for error handling.
- The `useOptimistic` value resets to the actual value when the enclosing async
  transition settles. Don't store derived state from it.
- Server Components (`'use server'`) require a framework (Next.js, Remix). This
  project uses client-side React only — no `'use server'` directive needed.
- React 19 StrictMode fires effects twice in development. The SSE hook must properly
  close the `EventSource` in the cleanup function or you'll get duplicate connections.

---

## Resources

- https://react.dev/blog/2024/12/05/react-19 (React 19 release blog — fetched 2026-06-08)
<!-- Drop additional links here — Archivist will synthesize -->
