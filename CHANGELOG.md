# Changelog

All notable changes to this project will be documented in this file.

This file is maintained automatically by `python-semantic-release` on merge to `main`.
Use `cz changelog` to preview what the next release entry will look like locally.

<!-- version list -->

## v1.0.0 (2026-06-20)

### Bug Fixes

- **api**: Read FastAPI version from package __version__ instead of hardcoding
  ([#2](https://github.com/hirekarl/flightaware_tv_oracle/pull/2),
  [`9353e02`](https://github.com/hirekarl/flightaware_tv_oracle/commit/9353e02c6141ff207d775d9c7d84f0d3a529b3a6))

- **ci**: Drop rootDir, use explicit cd in buildCommand — avoids publish path ambiguity
  ([`de38f51`](https://github.com/hirekarl/flightaware_tv_oracle/commit/de38f51da28bf7fde288d8326dfd72559c237b5d))

- **ci**: Remove plan field from static site — not a valid attribute
  ([`d438517`](https://github.com/hirekarl/flightaware_tv_oracle/commit/d4385179b0896f528dcc8ad92193d7f1a146e0c7))

- **ci**: Remove region from static site in render.yaml — not supported
  ([`3087e06`](https://github.com/hirekarl/flightaware_tv_oracle/commit/3087e065b4d97a1375bd48824248824f50844963))

- **ci**: StaticPublishPath is relative to rootDir, not repo root
  ([`09a00fd`](https://github.com/hirekarl/flightaware_tv_oracle/commit/09a00fd0d5244f15999c695b2453052e80bab61c))

- **frontend**: Address all Karl review items on PR #42
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Address karl's pr review — resize listener, sort order, spread fix, doc fence
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Address karl's pr review — resize listener, sort order, spread fix, doc fence
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

- **frontend**: Address karl's pr review — resize listener, sort order, spread fix, doc fence
  ([#25](https://github.com/hirekarl/flightaware_tv_oracle/pull/25),
  [`11321b0`](https://github.com/hirekarl/flightaware_tv_oracle/commit/11321b0b7d71c11af54533c8ff32b56d75da273b))

- **frontend**: Close Issue #29 and #27 — leaflet/tailwind removed, XSS escape, tests added
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Remove @import tailwindcss from index.css
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **hooks**: Resolve auto-format.sh via git root to fix frontend edits
  ([#44](https://github.com/hirekarl/flightaware_tv_oracle/pull/44),
  [`4c2071b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4c2071bcbe416afb5da60587127cf22f30f38202))

- **tests**: Derive mock fleet IDs from generate_mock_fleet() instead of hardcoding
  ([#37](https://github.com/hirekarl/flightaware_tv_oracle/pull/37),
  [`5843d2e`](https://github.com/hirekarl/flightaware_tv_oracle/commit/5843d2ee687353d2bea791e11028b5f0821491da))

### Build System

- **deps**: Bump actions/cache from 4 to 5
  ([#8](https://github.com/hirekarl/flightaware_tv_oracle/pull/8),
  [`714ce48`](https://github.com/hirekarl/flightaware_tv_oracle/commit/714ce48db36e398a77876a2234e8c1047e57b5e5))

- **deps**: Bump actions/checkout from 4 to 6
  ([#12](https://github.com/hirekarl/flightaware_tv_oracle/pull/12),
  [`1d2cee7`](https://github.com/hirekarl/flightaware_tv_oracle/commit/1d2cee7225bd9fc3e3f1d967634886d66ae45e47))

- **deps**: Bump actions/setup-node from 4 to 6
  ([#11](https://github.com/hirekarl/flightaware_tv_oracle/pull/11),
  [`1f522ec`](https://github.com/hirekarl/flightaware_tv_oracle/commit/1f522ec5f771f7e5df1e761e161cf5a20d59b71e))

- **deps**: Bump astral-sh/setup-uv from 4 to 7
  ([#9](https://github.com/hirekarl/flightaware_tv_oracle/pull/9),
  [`35aa97b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/35aa97b937b1ee654d6064289f76fb3f99140fc3))

- **deps**: Bump dorny/paths-filter from 3 to 4
  ([#30](https://github.com/hirekarl/flightaware_tv_oracle/pull/30),
  [`d0c7c8b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/d0c7c8b38e6ac2129fdfc94f7b2fc1deeb85a6cc))

- **deps**: Bump slackapi/slack-github-action from 2 to 3
  ([#10](https://github.com/hirekarl/flightaware_tv_oracle/pull/10),
  [`9fb6d3b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/9fb6d3b10cd1211312a7866af94088373f048179))

- **deps-dev**: Bump @eslint/js from 9.39.4 to 10.0.1 in /frontend
  ([#23](https://github.com/hirekarl/flightaware_tv_oracle/pull/23),
  [`bae9996`](https://github.com/hirekarl/flightaware_tv_oracle/commit/bae999678b5eb0f4d49a6d2c25cdec61fe9f2b27))

- **deps-dev**: Bump @playwright/test in /frontend
  ([#33](https://github.com/hirekarl/flightaware_tv_oracle/pull/33),
  [`43b4d83`](https://github.com/hirekarl/flightaware_tv_oracle/commit/43b4d835547695e223936f24f875e3ec1707567e))

- **deps-dev**: Bump @tailwindcss/vite from 4.3.0 to 4.3.1 in /frontend
  ([#32](https://github.com/hirekarl/flightaware_tv_oracle/pull/32),
  [`be6346b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/be6346b4654789fedcf53a867d850a430c897d10))

- **deps-dev**: Bump @types/node from 25.9.2 to 25.9.3 in /frontend
  ([#34](https://github.com/hirekarl/flightaware_tv_oracle/pull/34),
  [`62afc46`](https://github.com/hirekarl/flightaware_tv_oracle/commit/62afc46afcda74d36fc3357f588e486b18da9f0e))

- **deps-dev**: Bump eslint from 9.39.4 to 10.4.1 in /frontend
  ([#21](https://github.com/hirekarl/flightaware_tv_oracle/pull/21),
  [`5d92945`](https://github.com/hirekarl/flightaware_tv_oracle/commit/5d929455f10fb607de11a26fa06f1e5d10756b2b))

- **deps-dev**: Bump eslint-config-prettier in /frontend
  ([#16](https://github.com/hirekarl/flightaware_tv_oracle/pull/16),
  [`1f0f0a8`](https://github.com/hirekarl/flightaware_tv_oracle/commit/1f0f0a8d267fff12cc450d74b0e1d7c4b8e6ca50))

- **deps-dev**: Bump eslint-plugin-react-hooks in /frontend
  ([#20](https://github.com/hirekarl/flightaware_tv_oracle/pull/20),
  [`0f36f37`](https://github.com/hirekarl/flightaware_tv_oracle/commit/0f36f37cc16478135fca4518f0cbf7e81cb60058))

- **deps-dev**: Bump eslint-plugin-react-refresh in /frontend
  ([#22](https://github.com/hirekarl/flightaware_tv_oracle/pull/22),
  [`b14a7ec`](https://github.com/hirekarl/flightaware_tv_oracle/commit/b14a7ec89c821afd7bc18a1d2fc0a16af62277eb))

- **deps-dev**: Bump globals from 15.15.0 to 17.6.0 in /frontend
  ([#14](https://github.com/hirekarl/flightaware_tv_oracle/pull/14),
  [`80b780f`](https://github.com/hirekarl/flightaware_tv_oracle/commit/80b780fe23303bfb3fe3b23f0ddef6511f130d09))

- **deps-dev**: Bump jsdom from 25.0.1 to 29.1.1 in /frontend
  ([#15](https://github.com/hirekarl/flightaware_tv_oracle/pull/15),
  [`e9837a3`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e9837a3c195999cb8136fd5503820cdffaa936b1))

- **deps-dev**: Bump prettier from 3.8.3 to 3.8.4 in /frontend
  ([#13](https://github.com/hirekarl/flightaware_tv_oracle/pull/13),
  [`b22999e`](https://github.com/hirekarl/flightaware_tv_oracle/commit/b22999e9e0968240febf21594cb6961f35058a0d))

- **deps-dev**: Bump typescript-eslint in /frontend
  ([#31](https://github.com/hirekarl/flightaware_tv_oracle/pull/31),
  [`69ced9d`](https://github.com/hirekarl/flightaware_tv_oracle/commit/69ced9deddedae4a61cb76e024bcd0ddd36fb807))

- **deps-dev**: Bump typescript-eslint in /frontend
  ([#17](https://github.com/hirekarl/flightaware_tv_oracle/pull/17),
  [`d92f392`](https://github.com/hirekarl/flightaware_tv_oracle/commit/d92f3924ef954cdeb1357d895aa27b0982897f6c))

- **deps-dev**: Bump vitest from 4.1.8 to 4.1.9 in /frontend
  ([#35](https://github.com/hirekarl/flightaware_tv_oracle/pull/35),
  [`5b46065`](https://github.com/hirekarl/flightaware_tv_oracle/commit/5b4606525bf541a88871110603fa2041eda63e79))

- **frontend**: Wire Tailwind CSS v4 into Vite + React 19 setup
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Wire Tailwind CSS v4 into Vite + React 19 setup
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

- **frontend**: Wire Tailwind CSS v4 into Vite + React 19 setup
  ([#25](https://github.com/hirekarl/flightaware_tv_oracle/pull/25),
  [`11321b0`](https://github.com/hirekarl/flightaware_tv_oracle/commit/11321b0b7d71c11af54533c8ff32b56d75da273b))

### Chores

- Ignore frontend/.netlify/, delete map-prompt.md artifact
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

### Code Style

- **frontend**: Apply flightaware aviation navy & slate color theme
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Apply flightaware aviation navy & slate color theme
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

- **tests**: Apply ruff formatting to test suite
  ([#4](https://github.com/hirekarl/flightaware_tv_oracle/pull/4),
  [`4d559e3`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4d559e389563a7705d1365bbacd57785ff34dea8))

### Continuous Integration

- Add path-based job filtering to skip unaffected checks
  ([#24](https://github.com/hirekarl/flightaware_tv_oracle/pull/24),
  [`89cfb43`](https://github.com/hirekarl/flightaware_tv_oracle/commit/89cfb433460bfdb837a939d4a9ad5173e3893dce))

- Fix path filter gaps and normalize checkout version
  ([#24](https://github.com/hirekarl/flightaware_tv_oracle/pull/24),
  [`89cfb43`](https://github.com/hirekarl/flightaware_tv_oracle/commit/89cfb433460bfdb837a939d4a9ad5173e3893dce))

- **deploy**: Add Render Blueprint for free-tier API and static site
  ([#2](https://github.com/hirekarl/flightaware_tv_oracle/pull/2),
  [`9353e02`](https://github.com/hirekarl/flightaware_tv_oracle/commit/9353e02c6141ff207d775d9c7d84f0d3a529b3a6))

- **deploy**: Rename Render services to flightaware-tv-oracle base name
  ([#2](https://github.com/hirekarl/flightaware_tv_oracle/pull/2),
  [`9353e02`](https://github.com/hirekarl/flightaware_tv_oracle/commit/9353e02c6141ff207d775d9c7d84f0d3a529b3a6))

- **deps**: Add Dependabot config for pip, npm, and Actions
  ([#2](https://github.com/hirekarl/flightaware_tv_oracle/pull/2),
  [`9353e02`](https://github.com/hirekarl/flightaware_tv_oracle/commit/9353e02c6141ff207d775d9c7d84f0d3a529b3a6))

- **release**: Fix automated-release always skipped on push to main
  ([`11730ea`](https://github.com/hirekarl/flightaware_tv_oracle/commit/11730eaf00e58f855017d29d8c0d2bf320a38967))

- **settings**: Require confirmation before gh pr merge --admin
  ([#40](https://github.com/hirekarl/flightaware_tv_oracle/pull/40),
  [`e0627fe`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0627fef9841b2699a203e30dfeebc7a332abb3d))

- **slack**: Add Slack notifications for CI results and releases
  ([#2](https://github.com/hirekarl/flightaware_tv_oracle/pull/2),
  [`9353e02`](https://github.com/hirekarl/flightaware_tv_oracle/commit/9353e02c6141ff207d775d9c7d84f0d3a529b3a6))

### Documentation

- Add deployment section to README and update Automation Agent scope in CLAUDE.md
  ([#2](https://github.com/hirekarl/flightaware_tv_oracle/pull/2),
  [`9353e02`](https://github.com/hirekarl/flightaware_tv_oracle/commit/9353e02c6141ff207d775d9c7d84f0d3a529b3a6))

- Fix env var name GEMINI_API_KEY → GOOGLE_API_KEY in contributor setup
  ([#2](https://github.com/hirekarl/flightaware_tv_oracle/pull/2),
  [`9353e02`](https://github.com/hirekarl/flightaware_tv_oracle/commit/9353e02c6141ff207d775d9c7d84f0d3a529b3a6))

- Replace 'dispatcher' with 'FBO operator' across all files
  ([#44](https://github.com/hirekarl/flightaware_tv_oracle/pull/44),
  [`4c2071b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4c2071bcbe416afb5da60587127cf22f30f38202))

- **claude**: Add session start checklist for cross-machine workflow
  ([#18](https://github.com/hirekarl/flightaware_tv_oracle/pull/18),
  [`cc6d2c7`](https://github.com/hirekarl/flightaware_tv_oracle/commit/cc6d2c720fcc6f4d0d3d3f98221f8b90fc7db645))

- **claude**: Correct target audience from airline dispatchers to FBOs
  ([#44](https://github.com/hirekarl/flightaware_tv_oracle/pull/44),
  [`4c2071b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4c2071bcbe416afb5da60587127cf22f30f38202))

- **demo**: Add 4-minute presenter script for Karl and Ahsan
  ([#44](https://github.com/hirekarl/flightaware_tv_oracle/pull/44),
  [`4c2071b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4c2071bcbe416afb5da60587127cf22f30f38202))

- **demo**: Correct audience from dispatchers to FBO operators
  ([#44](https://github.com/hirekarl/flightaware_tv_oracle/pull/44),
  [`4c2071b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4c2071bcbe416afb5da60587127cf22f30f38202))

- **demo**: Describe AiImpactDrawer structure rather than predicting Gemini output
  ([#44](https://github.com/hirekarl/flightaware_tv_oracle/pull/44),
  [`4c2071b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4c2071bcbe416afb5da60587127cf22f30f38202))

- **demo**: Rewrite script for AI builder audience — business impact focus, beats 1-6, 4-min timing
  ([`06fa74b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/06fa74b87412ec50887bab717bd1157d749cc9f1))

- **demo**: Sharpen Act 4 close — business case landing, plain AI language
  ([`49e6705`](https://github.com/hirekarl/flightaware_tv_oracle/commit/49e6705ab6050046237aa15e3812762125f04f23))

- **demo**: Update beat cues to match DemoControls 1-indexed display
  ([#44](https://github.com/hirekarl/flightaware_tv_oracle/pull/44),
  [`4c2071b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4c2071bcbe416afb5da60587127cf22f30f38202))

- **todo**: Add two Sprint 2 backend items from PR #4 review
  ([#5](https://github.com/hirekarl/flightaware_tv_oracle/pull/5),
  [`5a9932f`](https://github.com/hirekarl/flightaware_tv_oracle/commit/5a9932fb78fa1f78ee7650d3157d49f03389e8e1))

- **todo**: Mark derive-mock-fleet-ids item complete (#37)
  ([#39](https://github.com/hirekarl/flightaware_tv_oracle/pull/39),
  [`4e60d60`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4e60d604e1e028b7e867f34bbaccc3efb46639eb))

- **todo**: Move telemetry adapter to icebox — AeroAPI access not available
  ([#38](https://github.com/hirekarl/flightaware_tv_oracle/pull/38),
  [`0252a9d`](https://github.com/hirekarl/flightaware_tv_oracle/commit/0252a9d1e85846216b950f194acfc123d5f44dc8))

- **todo**: Sync sprint board to 2026-06-19 state
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **todo**: Sync sprint board to current state
  ([#36](https://github.com/hirekarl/flightaware_tv_oracle/pull/36),
  [`6f10fd7`](https://github.com/hirekarl/flightaware_tv_oracle/commit/6f10fd73150bc2036d379b1743a719c06e1a986e))

- **todo**: Sync sprint board to current state
  ([#18](https://github.com/hirekarl/flightaware_tv_oracle/pull/18),
  [`cc6d2c7`](https://github.com/hirekarl/flightaware_tv_oracle/commit/cc6d2c720fcc6f4d0d3d3f98221f8b90fc7db645))

### Features

- **backend**: Add concurrent connection rate limiting to SSE endpoint
  ([#6](https://github.com/hirekarl/flightaware_tv_oracle/pull/6),
  [`62449a8`](https://github.com/hirekarl/flightaware_tv_oracle/commit/62449a866607962a626c71bad9bdf8f7b8baaa91))

- **backend**: Add structured per-cycle logging to SSE stream
  ([#4](https://github.com/hirekarl/flightaware_tv_oracle/pull/4),
  [`4d559e3`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4d559e389563a7705d1365bbacd57785ff34dea8))

- **backend**: Agent tests, crew logistics bug fix, SSE + AI integration
  ([#1](https://github.com/hirekarl/flightaware_tv_oracle/pull/1),
  [`df3e7f4`](https://github.com/hirekarl/flightaware_tv_oracle/commit/df3e7f47fdb954afc28912b94de13b8e2690051c))

- **backend**: Make CORS origins configurable via CORS_ORIGINS env var
  ([`77dcc8d`](https://github.com/hirekarl/flightaware_tv_oracle/commit/77dcc8d850c25bfc186aaf50b9d875d6e97b5493))

- **backend**: Wire CoordinatorAgent into SSE stream with full agent test coverage
  ([#4](https://github.com/hirekarl/flightaware_tv_oracle/pull/4),
  [`4d559e3`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4d559e389563a7705d1365bbacd57785ff34dea8))

- **demo**: 6-beat JFK crisis scenario engine with presenter UI
  ([#44](https://github.com/hirekarl/flightaware_tv_oracle/pull/44),
  [`4c2071b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4c2071bcbe416afb5da60587127cf22f30f38202))

- **demo**: Add background traffic and smooth map animation
  ([#44](https://github.com/hirekarl/flightaware_tv_oracle/pull/44),
  [`4c2071b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4c2071bcbe416afb5da60587127cf22f30f38202))

- **demo**: JFK crisis scenario engine, presenter UI, FBO audience correction
  ([#44](https://github.com/hirekarl/flightaware_tv_oracle/pull/44),
  [`4c2071b`](https://github.com/hirekarl/flightaware_tv_oracle/commit/4c2071bcbe416afb5da60587127cf22f30f38202))

- **frontend**: Add AiImpactDrawer slide-out panel for AI analysis
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Add leaflet map centered on kjfk with 20 moving aircraft
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Add leaflet map centered on kjfk with 20 moving aircraft
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

- **frontend**: Add severity-first flight sort utility and Tailwind CSS
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Add severity-first flight sort utility and Tailwind CSS
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

- **frontend**: Add severity-first flight sort utility and Tailwind CSS
  ([#25](https://github.com/hirekarl/flightaware_tv_oracle/pull/25),
  [`11321b0`](https://github.com/hirekarl/flightaware_tv_oracle/commit/11321b0b7d71c11af54533c8ff32b56d75da273b))

- **frontend**: Blue-navy tile hue, kjfk label, 45-aircraft busy traffic
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Blue-navy tile hue, kjfk label, 45-aircraft busy traffic
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

- **frontend**: Fix icon colors, align board columns, expand mock flight list
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Fix icon colors, align board columns, expand mock flight list
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

- **frontend**: Implement UI shell — mockFlights, FlightCard, MockFlightBoard, AppLayout
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Implement UI shell — mockFlights, FlightCard, MockFlightBoard, AppLayout
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

- **frontend**: Implement UI shell — mockFlights, FlightCard, MockFlightBoard, AppLayout
  ([#25](https://github.com/hirekarl/flightaware_tv_oracle/pull/25),
  [`11321b0`](https://github.com/hirekarl/flightaware_tv_oracle/commit/11321b0b7d71c11af54533c8ff32b56d75da273b))

- **frontend**: Implement useFleetStream SSE hook and wire into AppLayout
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: JFK live map + flight board UI shell
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

- **frontend**: Sprint 2 — Issue #29/#27 cleanup + useFleetStream SSE wiring
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Switch to maplibre-gl vector tiles for exact flightaware color fidelity
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Switch to maplibre-gl vector tiles for exact flightaware color fidelity
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

- **frontend**: Teal tile filter, jfk perimeter polygon, 30s update interval
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Teal tile filter, jfk perimeter polygon, 30s update interval
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

- **frontend**: Ui shell — tailwind, mock data, responsive layout
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Ui shell — tailwind, mock data, responsive layout
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

- **frontend**: UI shell — Tailwind, mock data, responsive layout
  ([#25](https://github.com/hirekarl/flightaware_tv_oracle/pull/25),
  [`11321b0`](https://github.com/hirekarl/flightaware_tv_oracle/commit/11321b0b7d71c11af54533c8ff32b56d75da273b))

- **frontend**: Wake sleeping Render backend via health-poll on SSE error
  ([`980cba9`](https://github.com/hirekarl/flightaware_tv_oracle/commit/980cba93717ef61bdc8655f7e0b177e109175ba6))

- **frontend**: Wire live FlightState into MapPanel, lift SSE to AppLayout
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Zoom map to jfk, add ground traffic, 10s updates
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Zoom map to jfk, add ground traffic, 10s updates
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

### Performance Improvements

- **backend**: Parallelize SSE coordinator calls with asyncio.gather
  ([#7](https://github.com/hirekarl/flightaware_tv_oracle/pull/7),
  [`a74b206`](https://github.com/hirekarl/flightaware_tv_oracle/commit/a74b2064b915550c272b002ab4dd3937fdb5dd1e))

- **backend**: Skip + cache Gemini calls to stay within free-tier quota
  ([`9a84645`](https://github.com/hirekarl/flightaware_tv_oracle/commit/9a8464553d1376ec7a1a5af884f546d238d47f98))

- **scripts**: SSE throughput baseline + lru-cache icebox close
  ([`23b6559`](https://github.com/hirekarl/flightaware_tv_oracle/commit/23b65595f5f09c7fabfcdaea8a35969576a13c81))

### Testing

- **api**: Add integration tests for HTTP contract and SSE stream
  ([#2](https://github.com/hirekarl/flightaware_tv_oracle/pull/2),
  [`9353e02`](https://github.com/hirekarl/flightaware_tv_oracle/commit/9353e02c6141ff207d775d9c7d84f0d3a529b3a6))

- **api**: HTTP contract and SSE stream integration tests
  ([#2](https://github.com/hirekarl/flightaware_tv_oracle/pull/2),
  [`9353e02`](https://github.com/hirekarl/flightaware_tv_oracle/commit/9353e02c6141ff207d775d9c7d84f0d3a529b3a6))

- **api**: Update tests to match main.py signatures after rebase
  ([#2](https://github.com/hirekarl/flightaware_tv_oracle/pull/2),
  [`9353e02`](https://github.com/hirekarl/flightaware_tv_oracle/commit/9353e02c6141ff207d775d9c7d84f0d3a529b3a6))

- **frontend**: Failing Vitest specs for UI shell components
  ([#42](https://github.com/hirekarl/flightaware_tv_oracle/pull/42),
  [`e1aec29`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e1aec29c1404fafded593b542635a53ac4f7cfbe))

- **frontend**: Failing Vitest specs for UI shell components
  ([#28](https://github.com/hirekarl/flightaware_tv_oracle/pull/28),
  [`e0d4702`](https://github.com/hirekarl/flightaware_tv_oracle/commit/e0d4702c1fdc1803f0efd84dba712519aa221981))

- **frontend**: Failing Vitest specs for UI shell components
  ([#25](https://github.com/hirekarl/flightaware_tv_oracle/pull/25),
  [`11321b0`](https://github.com/hirekarl/flightaware_tv_oracle/commit/11321b0b7d71c11af54533c8ff32b56d75da273b))
