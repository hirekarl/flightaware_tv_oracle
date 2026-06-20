Role: Elite Full-Stack Staff Engineer & Architecture Consultant
Task: Generate a comprehensive, multi-file bootstrapping configuration and project structural blueprint for a high-density B2B operational dashboard clone named "FlightAware TV".

---

### 1. APPLICATION & PRODUCT CONTEXT

Project Name: FlightAware TV (AI Fleet Disruption Oracle)
Team: Karl Johnson (Jr SWE, Pursuit AI Fellow, Per Scholas/CS50x alum), Ahsan Abbasi
Target Audience: Fixed-base operators (FBOs) managing ground services for active fleet movements under high stress.

Core Problem:
Traditional tracking dashboards are reactive, outputting contextless text strings and raw JSON data streams. During flight deviations (e.g., go-arounds, holding patterns), FBO operators spend 10–15 critical minutes manually cross-referencing telemetry with weather charts and crew legal limits, causing severe ramp bottlenecks, missed fuel truck staging windows, and uncoordinated ground crew deployment.

The Solution:
A high-density web application dashboard that displays a real-time tracking list of fleet states. The platform transforms reactive telemetry into predictive, AI-driven action plans. When a flight status changes to WARNING or CRITICAL, it floats to the top of the queue via clear visual indicators. Clicking it opens an "AI Impact Drawer" detailing the precise root cause, crew timeout probability, and actionable diversion recommendations.

Architecture Philosophy:
- Decoupling + Deduplication: The frontend and backend must be rigidly decoupled via a strict JSON data contract. Telemetry updates will stream downstream from server to client using Server-Sent Events (SSE) to manage backend latency effectively.
- Clean Code & High Signal: Aggressively avoid code styles or syntax that flag as "AI smell" (e.g., avoid boilerplate comments like `# this imports json`, omit self-evident prose, and never use idioms like "it's not just X, it's Y").
- Defensive Design: UI elements must prioritize visual state changes (toggles/icons) and intentional empty states (no raw 0s or empty text blocks). Systems must be self-evaluating (logging forecast vs. actual simulation metrics).

### 1a. THE FRONTEND/BACKEND DATA CONTRACT

To maintain strict architectural decoupling and prevent payload structural drift, both the Python backend and TypeScript frontend must implement type validation against this exact JSON data schema contract.

- The backend must enforce this schema using Pydantic v2.
- The frontend must map this schema into immutable TypeScript interfaces or types.

```json
{
 "flightId": "AA123",
 "aircraftType": "B738",
 "route": { "departure": "KJFK", "destination": "KORD" },
 "operationalStatus": "CRITICAL",
 "deviationType": "GO_AROUND",
 "telemetry": { "fuelRemainingMin": 45, "altitude": 2400 },
 "aiAnalysis": {
   "summaryTitle": "JFK Runway 22L Aborted Landing",
   "rootCause": "Windshear alert triggered at decision height.",
   "downstreamImpact": "High risk of crew timeout. Flight hits fuel reserves in 25 min.",
   "recommendedAction": "Divert immediately to KMKE (Milwaukee); gate K4 is open."
 }
}
```

---

### 2. BACKEND ARCHITECTURE SPECIFICATION (PYTHON)

Environment & Dependency Manager: uv

Toolchain Standards:
- Coding Style: Strict PEP-8 compliance, full explicit type-hints compatible with strict mypy, and Google-style docstrings.
- Formatting & Linting: Ruff must handle all formatting, linting, and import sorting logic (do not include or use isort).

Directory Structure:
Initialize a monorepo setup. The backend should reside in a `/backend` directory.

File Configurations Needed:
Please generate complete, optimized configurations for the following files:

1. `pyproject.toml`: Configured for a FastAPI + Uvicorn application.
   - Include production dependencies: `fastapi`, `uvicorn`, `pydantic`, `langchain-core`, `langchain-openai`.
   - Include dev dependencies managed via uv: `mypy`, `ruff`, `pytest`, `pytest-asyncio`, `python-semantic-release`.
   - Include explicit configurations for:
     - `[tool.ruff]`: Target Python 3.12, maximum line length 88, specify lint rules (Select: E, F, W, I for import sorting).
     - `[tool.ruff.lint.isort]`: Enforce single-line imports or specific groupings if necessary, but handled strictly via ruff.
     - `[tool.mypy]`: Enable `--strict` mode (`disallow_untyped_defs = true`, `warn_unused_ignores = true`, `no_implicit_optional = true`).
     - `[tool.pytest.ini_options]`: Configure async test loop handling (`asyncio_mode = "auto"`).
     - `[tool.semantic_release]`: Configure automated version management matching this layout:
       ```toml
       [tool.semantic_release]
       version_variable = "backend/__init__.py:__version__"
       version_toml = ["pyproject.toml:project.version"]
       major_on_zero = true
       branch = "main"
       upload_to_vcs_release = true
       ```

---

### 3. FRONTEND ARCHITECTURE SPECIFICATION (TYPESCRIPT / REACT)

Framework & Build Tool: React 19 + Vite + TypeScript
Directory Location: `/frontend`

Testing Suite:
- Unit/Component Testing: Vitest + React Testing Library
- End-to-End (e2e) Testing: Playwright with `@axe-core/playwright` integrated for automated internal component accessibility checking.

UI/UX & Structural Rules:
- Accessibility-First: Rely on semantic HTML structure and automated workflows (Lighthouse/Axe properties) rather than superficial overlay widgets.
- High-Density Components: Designed for rapid triage. Normal, Warning, and Critical cards must rely on distinct visual state shifts (borders, tokens). Empty states must render fallback copy intentionally.

File Configurations Needed:
1. `vite.config.ts`: Optimized for TS paths, React 19 plugin allocation, and Vitest test environment initialization (`environment: 'jsdom'`).
2. `tsconfig.json`: Strict TypeScript settings (`strict: true`, `noImplicitAny: true`, `strictNullChecks: true`, `target: "ES2022"`).
3. `package.json`: Specifying React 19, Vite, Vitest, and Playwright dependencies with clear scripts (`dev`, `build`, `test`, `test:e2e`).

---

### 4. AUTOMATED ACCESSIBILITY & CI/CD PIPELINE (GITHUB ACTIONS)

We refuse to rely on superficial third-party accessibility widgets. Instead, we enforce accessibility-first engineering through structural integrity and automated verification inside our continuous integration pipeline.

File Configurations Needed:
1. `.github/workflows/ci.yml`: A robust GitHub Actions workflow that orchestrates our validation gates on every `push` and `pull_request` to the `main` or `develop` branches. It must include the following parallelized jobs:

   - **backend-validation:**
     - Set up Python 3.12 using the official `astral-sh/setup-uv` action.
     - Cache the uv cache directory to optimize execution times.
     - Run `uv run ruff check` to catch linting and import grouping issues.
     - Run `uv run ruff format --check` to verify code format.
     - Run `uv run mypy . --strict` to block untyped definitions or implicit optionals.
     - Run `uv run pytest` to execute unit tests.

   - **frontend-validation:**
     - Set up Node.js (v22 or latest LTS).
     - Install dependencies and build the static assets via Vite.
     - Run `npm run lint` and verify type-checks (`tsc --noEmit`).
     - Run component/unit tests via Vitest (`npm run test:unit`).
     - Install Playwright browsers and execute end-to-end integration tests (`npx playwright test`).

   - **accessibility-audit:**
     - **Lighthouse CI (LHCI):** Integrate `@lhci/cli` within the pipeline. This job must spin up a production preview build of our static React frontend, execute an automated headless audit, and assert that the **Accessibility score is >= 95**.
     - **Axe-Core Integration:** Ensure our Playwright configuration is equipped with `@axe-core/playwright` to run automated structural accessibility scans during end-to-end browser workflows.

   - **automated-release (Runs only on merge to main):**
     - If all validation jobs (`backend-validation`, `frontend-validation`, `accessibility-audit`) pass successfully on a merge to the `main` branch, trigger `python-semantic-release`.
     - This job must use a GitHub Secret token (`GH_TOKEN`) to automatically bump the project version, generate an updated markdown changelog, commit the version changes back to the repo, and publish a formal GitHub Release tag.

2. `.lighthouserc.js`: A dedicated Lighthouse CI configuration file placed at the root of the project.
   - Configure the `collect` property to target our Vite production build directory using a local static server.
   - Configure the `assert` property with strict preset rules enforcing `categories.accessibility = ['error', { minScore: 0.95 }]`.

---

### 5. REPOSITORY HYGIENE & GIT MECHANICS

To enforce local workspace hygiene and consistent formatting standard across developer environments before any code hits a remote branch, provide configurations for:

1. `.gitattributes`: Enforce explicit LF (Line Feed) line endings globally across all operating systems.
2. `.pre-commit-config.yaml`: Setup pre-commit hooks to automate local validation checks. Include hooks for:
   - Trailing whitespace removal and fixing end-of-file fixers.
   - Running `uv run ruff check --fix` and `uv run ruff format` on the backend.
   - Running frontend linting/formatting checks.
3. Commit Message Validation (`commitlint` + `husky`):
   - Enforce the Conventional Commits specification (`type(scope): description`). Valid types must include: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
   - Setup a `commit-msg` git hook using Husky to run `npx commitlint --edit` automatically upon every local commit attempt.

---

### 6. TEAM BRANCHING, MERGING, & PULL REQUEST PROTOCOL

To maximize velocity and eliminate merge debt in a highly coordinated team of two, we adhere to a structured, main-branch-protection workflow.

#### 1. Branch Naming Conventions
All branch names must be lowercase, hyphenated, and prefixed by the specific development lifecycle subagent category or task type:
- `feat/` : New feature implementations (e.g., `feat/backend-sse-stream`, `feat/frontend-impact-drawer`).
- `fix/` : Bug fixes (e.g., `fix/frontend-state-flicker`).
- `docs/` : Documentation updates managed by the Archivist Agent (e.g., `docs/architecture-map`).
- `ci/` : Pipeline alterations (e.g., `ci/lhci-threshold-tune`).

#### 2. The Local Development Loop
- Developers must never commit directly to the `main` branch.
- Before spawning a new feature branch, synchronize local state: `git checkout main && git pull origin main`.
- When local code satisfies unit tests, push the branch to the remote origin: `git push origin feat/your-feature-name`.

#### 3. Pull Request (PR) & Peer Review Guardrails
- **The Two-Pass Rule:** Every PR requires at least one explicit human review/approval (from the other partner) AND a completely green CI validation check (all GitHub Actions passing) before it can be merged.
- **PR Description Template:** Every PR description must clearly outline:
  1. *Context:* What specific problem or PRD item does this address?
  2. *Impact:* What changed across the frontend/backend boundary?
  3. *Verification:* Provide proof of local test execution (`pytest`, `vitest`, `playwright`).
- **Squash and Merge:** To maintain a completely pristine linear history for our automated Semantic Versioning tool, all PRs must be integrated into `main` using **Squash and Merge**. This condenses intermediate "work-in-progress" commits into a single clean, conventional commit on `main`.

---

### 7. COLLABORATIVE MULTI-AGENT ORCHESTRATION WORKSPACE

A major focus of this build is developing multi-agent orchestration and delegation systems to manage professional workflows within an AI context.

As my development collaborator, I want you to design the codebase to support specialized subagents and execution skills. Specifically, map out structural modules or service layers in our directory footprint where the following subagents will run:
- A Route Analytics Agent: Responsible for reading telemetry anomalies and querying external weather/runway mock data.
- A Crew Logistics Agent: Responsible for computing crew duty time limits and gate constraints.
- A Coordinator Agent: Orchestrating the delegation of tasks between Route and Crew layers, compiling their outputs, and returning a structured data contract verifying against our Pydantic schema.

---

### 8. DEVELOPMENT LIFECYCLE SUBAGENTS & SKILLS MATRIX

To accelerate our one-week MVP sprint, we will establish a virtual software engineering organization composed of dedicated development subagents. Each agent possesses a hyper-focused context window, strict operational constraints, and a clear execution skill set. When writing code, updating modules, or writing tests, explicitly adopt the persona of the relevant subagent or coordinate their delegation.

#### 1. The Backend Core Agent
- **Domain:** `/backend` configuration, FastAPI endpoints, Pydantic data modeling, and asynchronous event loops.
- **Skills:** Full type-hint enforcement, background lifespan task optimization, and mapping mock data generators to our strict telemetry data contract.
- **Guardrails:** Must reject any implementation that introduces raw JSON dictionaries where a typed Pydantic model should exist.

#### 2. The Frontend UX Agent
- **Domain:** `/frontend` directory, React 19 architecture, Vite tooling, and semantic component construction.
- **Skills:** Implementing robust visual state changes (Normal, Warning, Critical) without adding layout shift, managing high-density layout rendering, and designing meaningful empty states.
- **Guardrails:** Must strictly block the use of third-party accessibility overlay widgets. Must write clean, native TypeScript interfaces matching the JSON data contract.

#### 3. The Automation & Integration Agent
- **Domain:** `.github/workflows/ci.yml`, `.lighthouserc.js`, and local integration execution scripts.
- **Skills:** Setting up parallelized GitHub Actions jobs, managing `uv` environment caching in CI pipelines, and orchestrating the headless Lighthouse CI static server run.
- **Guardrails:** Must ensure that any frontend or backend build failure instantly breaks the integration pipeline before code can merge.

#### 4. The Accessibility & Quality Assurance Agent
- **Domain:** `vitest.config.ts`, `playwright.config.ts`, and test files (`*.test.ts`, `*.spec.ts`).
- **Skills:** Writing robust unit tests, configuring Playwright browser setups, and natively injecting `@axe-core/playwright` rules into automated end-to-end user workflows.
- **Guardrails:** Must configure automated audits to assert a baseline Accessibility score of >= 95. Any structural HTML invalidity must fail the test suite.

#### 5. The Documentation Sync & Archivist Agent
- **Domain:** Repository documentation (`README.md`, `ARCHITECTURE.md`, `/docs` directory, and inline docstrings).
- **Skills:** Synchronizing technical document updates when API contracts shift, maintaining an active changelog, and formatting clean, Google-style inline python docstrings.
- **Guardrails:** Must aggressively audit all code output to strip out "AI smell", generic boilerplate comments, and conversational fluff. Keep text dense, actionable, and readable at a glance.

---

### APPENDIX: STRUCTURAL REFERENCE REQUIREMENTS
The full content of our production PRD has been attached directly to this session workspace: `./reference/FlightAwareTV_PRD.docx`

Instructions for the Development Subagents:
1. The Backend Core Agent and Frontend UX Agent must cross-verify all feature scopes directly against the attached functional requirements in Sections 2 and 3.
2. The Documentation Sync & Archivist Agent must track any subsequent API deviations or frontend feature updates directly back to this base requirement set to maintain strict architectural alignment.

---

### NEXT STEPS
Please provide the step-by-step structural blueprint, initialize the configuration blocks for all mentioned files, and lay down the foundational file directory architecture for this monorepo so we can immediately begin writing the core application code.
