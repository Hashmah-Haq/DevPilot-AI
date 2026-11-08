
import ast
import json
import subprocess
import tempfile
from pathlib import Path


def syntax_analyzer(code):
    try:
        ast.parse(code)
        return {"status": "success", "issues": []}
    except SyntaxError as error:
        return {
            "status": "error",
            "issues": [{
                "line": error.lineno,
                "message": error.msg
            }]
        }


def ruff_analyzer(code):
    with tempfile.TemporaryDirectory() as folder:
        file_path = Path(folder) / "sample.py"
        file_path.write_text(code, encoding="utf-8")

        result = subprocess.run(
            ["ruff", "check", "--output-format", "json", str(file_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)

        return json.loads(result.stdout)


def security_analyzer(code):
    with tempfile.TemporaryDirectory() as folder:
        file_path = Path(folder) / "sample.py"
        file_path.write_text(code, encoding="utf-8")

        result = subprocess.run(
            ["bandit", "-f", "json", "-q", str(file_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)

        report = json.loads(result.stdout)
        return report.get("results", [])
