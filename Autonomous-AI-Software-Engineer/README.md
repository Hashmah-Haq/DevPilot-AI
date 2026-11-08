# ⚡ DevPilot AI — Autonomous AI Software Engineer

A portfolio-ready **Python code analysis and agentic AI dashboard** built with Streamlit. It integrates your original multi-agent backend, Qwen2.5-0.5B-Instruct, FAISS retrieval, Ruff, Bandit, and Python AST.

## Features

- **Working static analysis:** syntax checking, Ruff lint findings, Bandit security findings.
- **Professional UI:** responsive sidebar, dark/light appearance, metrics, code workspace, tabs, reports and downloads.
- **Optional AI agents:** Qwen-assisted task planning, issue explanation and suggested fixes.
- **RAG search:** existing FAISS index and sentence-transformer embeddings.
- **Reports:** timestamped JSON artifacts, downloadable from the UI.
- **Safe by design:** the dashboard **never executes pasted code or AI-generated fixes**.

## Quick start (Python 3.10–3.12 recommended)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run frontend/app.py
```

Open the local address shown in the terminal (typically http://localhost:8501).

**For optional Qwen agents and FAISS RAG:**

```bash
pip install -r requirements-ai.txt
```

The first AI run may download models from Hugging Face and take several minutes on CPU. Internet access and sufficient memory are required. The original Qwen model is **not bundled** in this ZIP.

## Google Colab

Upload and extract the ZIP to `/content`, install `requirements.txt` (and optionally `requirements-ai.txt`), then start Streamlit:

```python
%cd /content/Autonomous-AI-Software-Engineer
!pip -q install -r requirements.txt
!python -m streamlit run frontend/app.py --server.address 0.0.0.0 --server.port 8501 &
```

Colab proxy URLs sometimes return 404 even when Streamlit is healthy. **Local run is the recommended reliable demo setup.** If exposing through a temporary tunnel, use only non-sensitive sample code and stop the tunnel after recording.

## Demo recording walkthrough

1. Open **Overview** and show the dashboard metrics and toolkit cards.
2. Open **Code Workspace**, leave the included sample with `undefined_variable`, and click **Run Static Analysis**.
3. Show the Ruff **F821** finding, syntax status, and security tab. Download the JSON report.
4. Open **Reports** and show the saved analysis.
5. Toggle the appearance in the sidebar. Optionally show **AI Agents** and **RAG Knowledge** if AI dependencies are installed.

## Repository structure

```text
frontend/app.py             Streamlit dashboard
frontend/service.py         Backend interface + report storage
agents/                     Original agent implementations
rag/                        Original FAISS index, documents and retriever
tools/                      Original analysis and verification tools
examples/                   Demo code and unit tests
reports/                    Saved JSON reports
requirements.txt            Minimal working dashboard dependencies
requirements-ai.txt         Optional AI/RAG dependencies
```

## Validation and limitations

- Static checks do not guarantee program correctness, safety, or freedom from vulnerabilities.
- AI-generated code is **suggested**, never executed or functionally validated in the dashboard.
- Running untrusted Python tests outside a sandbox is unsafe; this dashboard does not provide a sandbox.
- Optional model-based workflows may fail on machines with insufficient memory or without internet access.
- The app has no authentication: use it locally and avoid uploading secrets or private code to public demos.
- Some original demo tests intentionally fail; see `examples/unit_test_demo/test_failure_demo.py`.

## License

See `LICENSE` for the project source license. Third-party dependencies and model weights have their own licenses.

## One-click local Windows launch (recommended for screenshots)

Extract the ZIP and **double-click `START_DASHBOARD.bat`**. The launcher creates a local virtual environment, installs the base requirements on first run, starts Streamlit on a free localhost port, and opens the browser automatically. Python 3.10+ and internet access for first-time installation are prerequisites. Keep the terminal window open. **No Colab proxy, Cloudflare tunnel, or public URL is needed.** If launch fails, inspect `launcher_error.log`.

On Linux/macOS, run `bash START_DASHBOARD.sh` with Python 3 and venv installed.

The basic code workspace uses real AST/Ruff/Bandit checks. Qwen and FAISS features require additional dependencies from `requirements-ai.txt`, model downloads, and sufficient RAM. AI-generated fixes are not executed or guaranteed correct.
