
from tools.code_analyzer import (
    syntax_analyzer,
    ruff_analyzer,
    security_analyzer
)


def verify_code_fix(original_code, fixed_code):

    # Step 1: Analyze original code
    original_syntax = syntax_analyzer(original_code)
    original_quality = ruff_analyzer(original_code)
    original_security = security_analyzer(original_code)

    # Step 2: Analyze AI-generated code
    fixed_syntax = syntax_analyzer(fixed_code)
    fixed_quality = ruff_analyzer(fixed_code)
    fixed_security = security_analyzer(fixed_code)

    # Step 3: Count findings
    original_issues = (
        len(original_syntax["issues"])
        + len(original_quality)
        + len(original_security)
    )

    fixed_issues = (
        len(fixed_syntax["issues"])
        + len(fixed_quality)
        + len(fixed_security)
    )

    # Step 4: Compare results
    syntax_valid = fixed_syntax["status"] == "success"

    # Check whether any security findings remain
    security_clear = len(fixed_security) == 0

    # Check whether total findings decreased
    improved = fixed_issues < original_issues

    # Static checks only; not proof of correctness
    if not syntax_valid:
        status = "rejected_invalid_syntax"
    elif not security_clear:
        status = "needs_security_review"
    elif not improved:
        status = "no_measured_improvement"
    else:
        status = "static_checks_improved"

    return {
        "original_issues": original_issues,
        "fixed_issues": fixed_issues,
        "syntax_valid": syntax_valid,
        "security_clear": security_clear,
        "improved": improved,
        "status": status,
        "original_analysis": {
            "syntax": original_syntax,
            "quality": original_quality,
            "security": original_security
        },
        "fixed_analysis": {
            "syntax": fixed_syntax,
            "quality": fixed_quality,
            "security": fixed_security
        }
    }
