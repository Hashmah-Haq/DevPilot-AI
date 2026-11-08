
import subprocess
import sys
from pathlib import Path


def run_unit_tests(project_folder, timeout=60):
    """
    Run pytest on a trusted local project.

    Returns test results without modifying source files.
    """

    folder = Path(project_folder).resolve()

    if not folder.is_dir():
        raise FileNotFoundError(
            f"Project folder not found: {folder}"
        )

    if timeout <= 0:
        raise ValueError("Timeout must be positive.")

    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        str(folder)
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(folder)
        )

        if result.returncode == 0:
            status = "passed"
        elif result.returncode == 1:
            status = "failed"
        elif result.returncode == 5:
            status = "no_tests_collected"
        else:
            status = "test_error"

        return {
            "status": status,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "exit_code": None,
            "stdout": "",
            "stderr": "Tests exceeded the time limit."
        }
