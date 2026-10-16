# HYDRA — Autonomous AI Agent Firewall

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastMCP](https://img.shields.io/badge/FastMCP-SSE-orange.svg)](https://github.com/jlowin/fastmcp)
[![ArmorIQ](https://img.shields.io/badge/ArmorIQ-CSRG--IAP-green.svg)](https://armoriq.ai/)
[![Gemini](https://img.shields.io/badge/Gemini-3.8%20Flash-purple.svg)](https://ai.google.dev/)

An enterprise-grade autonomous firewall for Model Context Protocol (MCP) agents. Every tool invocation is cryptographically bound to user intent via **ArmorIQ CSRG-IAP** and evaluated against security policies before execution.

---

## Architecture Pipeline

```text
┌────────────────────────┐      ┌───────────────────────────┐
│   Developer Directive  │ ───► │  Gemini Cognitive Planner │
└────────────────────────┘      └─────────────┬─────────────┘
                                              │ Structured Execution Graph
                                              ▼
┌────────────────────────┐      ┌───────────────────────────┐
│  MCP Sandbox Runtime   │ ◄─── │   ArmorIQ Policy Engine   │
│  (Real Actions/Audits) │      │  (Cryptographic Proofs)   │
└────────────────────────┘      └───────────────────────────┘
```

1. **Developer Directive**: Natural language prompt specifying the autonomous task.
2. **Cognitive Planner**: Gemini 3.8 / 3.7 Flash decomposes the intent into a typed execution graph.
3. **ArmorIQ CSRG-IAP**: Mints a cryptographically signed intent token and verifies Merkle inclusion proofs.
4. **Policy Enforcement Gatekeeper**: Evaluates each action against enterprise policies (`armoriq.yaml`) prior to MCP tool execution.
5. **Sandbox Runtime**: Authorizes benign actions on `./sandbox_repo` while hard-intercepting destructive operations and prompt injections.

---

## Enforcement Vectors

| Vector | Name | Type | Description |
| :--- | :--- | :--- | :--- |
| **01** | **Authorized Code Audit** | `Safe / Allowed` | Reads `payment_service.py`, detects SQL injection, and publishes a structured review to PR #1. |
| **02** | **Protected CI/CD Tampering** | `Blocked Attack` | Direct attack attempting to overwrite `.github/workflows/deploy.yml` and delete the repository. |
| **03** | **Indirect Prompt Injection** | `Intercepted Hijack` | Poisoned markdown PR note containing a hidden `SYSTEM OVERRIDE` instruction attempting to hijack LLM tools. |
| **04** | **Risk-Based Patch Commit** | `Safe / Allowed` | Performs static risk analysis on repository and commits parameterized fix to branch `fix/sql-injection-patch`. |

---

## Quickstart (Local Development)

### 1. Clone & Setup Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and provide your API keys:
```bash
cp .env.example .env
```
Ensure `.env` contains:
```ini
ARMORIQ_API_KEY=your_armoriq_api_key
ARMORIQ_AGENT_ID=hydra-dev-agent
ARMORIQ_USER_EMAIL=developer@hydra.security
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
```

### 3. Run Automated Enforcement Tests
Verify that authorized actions succeed and threats are intercepted:
```bash
python test_enforcement.py
```

### 4. Launch HYDRA Dashboard
```bash
python run_all.py
```
Open **http://localhost:8501** in your browser.

---

## Deployment Options

### Option A: Docker / Container Deployment
HYDRA includes a production-ready `Dockerfile` and `docker-compose.yml`.

Run with Docker Compose:
```bash
docker compose up --build
```
Or build and run directly:
```bash
docker build -t hydra-firewall .
docker run -p 8501:8501 --env-file .env hydra-firewall
```

### Option B: Streamlit Community Cloud
1. Push this repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io).
3. Select your repository, set the main file path to `app.py`.
4. In **Advanced Settings -> Secrets**, add:
   ```toml
   ARMORIQ_API_KEY = "your_key"
   ARMORIQ_AGENT_ID = "hydra-dev-agent"
   ARMORIQ_USER_EMAIL = "developer@hydra.security"
   GEMINI_API_KEY = "your_key"
   GEMINI_MODEL = "gemini-3.8-flash"
   ```
5. Click **Deploy**.

---

## Features & UI Capabilities

- **Light & Dark Mode**: Seamless, high-contrast themes toggled with one click.
- **Real-Time Telemetry**: Live metrics for Cognitive Planner, Authorized Actions, Intercepted Threats, and CI/CD SHA-256 integrity.
- **Cryptographic Intent Proofs**: Inspect signed CSRG-IAP tokens and execution graphs.
- **Live File Explorer**: View sandbox files (`deploy.yml`, `payment_service.py`, `external_pr_note.md`) and PR review logs directly from the sidebar.
- **One-Click Sandbox Reset**: Restore the sandbox repository to a pristine state at any time.