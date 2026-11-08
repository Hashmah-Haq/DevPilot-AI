
import json
from pathlib import Path

from tools.code_analyzer import (
    syntax_analyzer,
    ruff_analyzer,
    security_analyzer
)


def scan_project(folder_path):
    folder = Path(folder_path)

    if not folder.is_dir():
        raise FileNotFoundError(
            f"Project folder not found: {folder}"
        )

    results = {}
    total_files = 0
    total_findings = 0

    excluded_folders = {
        ".git", ".venv", "venv",
        "__pycache__", "site-packages",
        "node_modules"
    }

    for file_path in sorted(folder.rglob("*.py")):

        if any(
            part in excluded_folders
            for part in file_path.relative_to(folder).parts
        ):
            continue

        code = file_path.read_text(encoding="utf-8")

        syntax = syntax_analyzer(code)
        ruff = ruff_analyzer(code)
        security = security_analyzer(code)

        findings = (
            len(syntax["issues"]) +
            len(ruff) +
            len(security)
        )

        relative_name = str(
            file_path.relative_to(folder)
        )

        results[relative_name] = {
            "syntax": syntax,
            "ruff": ruff,
            "security": security,
            "total_findings": findings
        }

        total_files += 1
        total_findings += findings

    return {
        "project": folder.name,
        "files_scanned": total_files,
        "total_findings": total_findings,
        "files": results
    }
