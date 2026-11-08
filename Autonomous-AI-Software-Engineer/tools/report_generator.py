
import json
from pathlib import Path
from datetime import datetime, timezone


def generate_project_report(
    execution_result,
    output_folder
):
    """
    Save AI workflow results as a structured JSON report.
    """

    if not isinstance(execution_result, dict):
        raise TypeError("Execution result must be a dictionary.")

    folder = Path(output_folder)
    folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    report = {
        "project": "Autonomous AI Software Engineer",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "user_request": execution_result.get(
            "user_request", ""
        ),
        "plan": execution_result.get("plan", {}),
        "executed_tasks": execution_result.get(
            "execution_log", []
        ),
        "agent_results": execution_result.get(
            "results", {}
        ),
        "workflow_status": execution_result.get(
            "status", "unknown"
        ),
        "limitations": [
            "AI-generated fixes are not automatically executed.",
            "Static checks do not prove functional correctness.",
            "Unit tests require a trusted testing environment."
        ]
    }

    report_path = folder / f"ai_report_{timestamp}.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False,
            default=str
        )

    return {
        "status": "report_saved",
        "report_path": str(report_path),
        "report": report
    }
