# Contributor Setup Guide

Covers first-time environment setup, GitHub CLI authentication, and SSL troubleshooting.
Companion to the quick-start steps in the root `README.md`.

---

## 1. Python

You do **not** need to install Python separately. `uv` manages Python versions for you.

Install `uv` first:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then let uv pull the correct Python version and install all dependencies in one step:

```bash
uv python install 3.12   # downloads and pins the interpreter
uv sync --all-groups     # creates .venv + installs backend + dev deps
```

Verify:

```bash
uv run python --version  # should print Python 3.12.x
```

---

## 2. Node.js

Install Node.js 20 LTS or later:

- **Windows / macOS**: download the installer from [nodejs.org](https://nodejs.org)
- **macOS (Homebrew)**: `brew install node`
- **Windows (winget)**: `winget install OpenJS.NodeJS.LTS`

Verify:

```bash
node --version   # 20.x or later
npm --version
```

---

## 3. GitHub CLI

### Install

- **macOS**: `brew install gh`
- **Windows**: `winget install GitHub.cli`
- **Linux**: see [cli.github.com/manual/installation](https://cli.github.com/manual/installation)

### Fix SSL errors (do this before authenticating)

SSL failures on the `gh` CLI almost always come from the CLI using a different certificate
store than your browser or OS. Fix by platform:

**Windows** (most common cause: antivirus or corporate proxy doing SSL inspection)

Switch Git and `gh` to the Windows native certificate store (SChannel), which trusts the same
CAs as your browser:

```powershell
git config --global http.sslBackend schannel
```

Restart your terminal, then verify with:

```powershell
gh api user
```

If that returns your GitHub username, SSL is resolved. If you still get an error, check
whether your machine is on a VPN or corporate network — you may need to import the proxy's
root CA cert into the Windows Certificate Store (ask your IT admin for the `.cer` file, then
run `certlm.msc` → Trusted Root Certification Authorities → Import).

**macOS**

```bash
brew upgrade gh          # outdated cert bundle is the most common cause
gh api user              # verify
```

If still failing and you're behind a proxy, set:

```bash
export HTTPS_PROXY=http://your-proxy:port
```

Add it to `~/.zshrc` or `~/.bashrc` to persist.

**Linux**

```bash
sudo apt update && sudo apt install --reinstall ca-certificates   # Debian/Ubuntu
gh api user
```

### Authenticate

Use the browser-based flow — it is the most reliable method across all environments and does
not depend on the CLI's SSL chain to complete:

```bash
gh auth login
```

When prompted:
1. **Where?** → `GitHub.com`
2. **Protocol?** → `HTTPS`
3. **Authenticate?** → `Login with a web browser`
4. Copy the one-time code shown in the terminal, press Enter, and complete the flow in your browser.

Verify authentication:

```bash
gh auth status   # should show: Logged in to github.com as <your-username>
```

---

## 4. Clone and finish setup

```bash
gh repo clone <org>/flightaware_tv_oracle
cd flightaware_tv_oracle

# Root Node deps (Husky hooks + commitlint)
npm install

# Frontend deps
cd frontend && npm install && cd ..

# Pre-commit hook environments (one-time download)
uv run pre-commit install-hooks

# Environment variables
cp .env.example .env
# → open .env and fill in GEMINI_API_KEY
```

---

## 5. Smoke test

```bash
# Backend
uv run uvicorn backend.main:app --reload
# → open http://localhost:8000/health — should return {"status": "ok"}

# Frontend (new terminal)
cd frontend && npm run dev
# → open http://localhost:5173
```

If both servers start without errors, your environment is ready.
