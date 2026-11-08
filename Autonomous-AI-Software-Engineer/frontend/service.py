"""Safe interface between the Streamlit dashboard and the existing analyzers."""
import ast
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports'


def analyze_code(code: str) -> dict:
    """Run static checks only. Never execute submitted code."""
    if not isinstance(code, str) or not code.strip():
        raise ValueError('Enter some Python code first.')
    if len(code) > 100_000:
        raise ValueError('Code exceeds the 100,000-character demo limit.')
    from tools.code_analyzer import syntax_analyzer, ruff_analyzer, security_analyzer
    syntax = syntax_analyzer(code)
    errors = {}
    try:
        quality = ruff_analyzer(code)
    except (FileNotFoundError, RuntimeError, OSError) as exc:
        quality = []
        errors['ruff'] = str(exc)
    try:
        security = security_analyzer(code)
    except (FileNotFoundError, RuntimeError, OSError) as exc:
        security = []
        errors['bandit'] = str(exc)
    return {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'syntax': syntax, 'quality': quality, 'security': security,
        'tool_errors': errors,
        'counts': {'syntax': len(syntax.get('issues', [])), 'quality': len(quality), 'security': len(security)},
        'status': 'partial' if errors else 'completed',
        'code_executed': False,
    }


def save_report(result: dict) -> Path:
    REPORTS.mkdir(exist_ok=True, parents=True)
    import uuid
    path = REPORTS / f"review_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.json"
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str), encoding='utf-8')
    return path


def load_reports() -> list[Path]:
    return sorted(REPORTS.glob('*.json'), key=lambda p: p.stat().st_mtime, reverse=True) if REPORTS.exists() else []


def optional_ai(task: str, code: str, request: str = ''):
    """AI runs only on explicit request; generated code is never executed."""
    if task == 'explain':
        from agents.code_explanation_agent import explain_code_issues
        return explain_code_issues(code)
    if task == 'fix':
        from agents.fix_pipeline import run_fix_pipeline
        return run_fix_pipeline(code)
    if task == 'plan':
        from agents.task_planner import create_task_plan
        return create_task_plan(request or 'Review and improve this Python code')
    if task == 'rag':
        from rag.rag_retriever import search_knowledge
        return search_knowledge(request or code[:300], top_k=3)
    raise ValueError('Unknown AI task')
