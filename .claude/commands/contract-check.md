You are the Backend Core Agent performing a data contract integrity check.

Steps:
1. Read `backend/models/flight.py` — locate `FlightState` and all sub-models.
2. Read `frontend/src/types/flight.ts` — locate all TypeScript interfaces that mirror the contract.
3. For every field in `FlightState` (and sub-models), verify:
   - The field exists in the corresponding TypeScript interface.
   - The type mapping is correct (`str` → `string`, `int | float` → `number`, `Optional[X]` → `X | null`, `list[X]` → `X[]`).
   - Nesting depth and structure match.
4. Report all drift: missing fields, type mismatches, structural differences.
5. If the contract is fully aligned, confirm it explicitly.

A clean contract report must state: "Contract aligned — no drift detected."
