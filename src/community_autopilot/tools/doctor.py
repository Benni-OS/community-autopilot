"""Doctor & Runtime Diagnostics for community-autopilot.

Verifies Python runtime, HTTP/FastAPI/Pydantic dependencies, SLA priority
classification, and HMAC-SHA256 webhook signature verification.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import importlib.util
import json
import platform
import sys
from datetime import UTC, datetime, timedelta
from typing import Any

from community_autopilot.analyzer import Analyzer
from community_autopilot.config import Settings
from community_autopilot.models import Comment, Issue, IssueState, Priority
from community_autopilot.webhook import verify_signature


def probe_dependencies() -> dict[str, bool]:
    """Check availability of core community-autopilot runtime dependencies."""
    packages = ("httpx", "pydantic", "pydantic_settings", "fastapi", "uvicorn", "typer", "rich")
    return {pkg: importlib.util.find_spec(pkg) is not None for pkg in packages}


def run_diagnostics() -> dict[str, Any]:
    """Run full triage analyzer and webhook security self-checks."""
    settings = Settings(github_token="dry-run-token", nemesis_api_key="dry-run-key")
    analyzer = Analyzer(settings)

    now = datetime.now(UTC)
    sample_issue = Issue(
        repo="benni-os/mcp-forge",
        number=42,
        title="Sample SLA probe issue",
        body="Testing priority classification",
        author="contributor",
        state=IssueState.OPEN,
        labels=[],
        assignees=[],
        created_at=now - timedelta(hours=60),
        updated_at=now - timedelta(hours=50),
        html_url="https://github.com/benni-os/mcp-forge/issues/42",
        comments=[
            Comment(
                id=1,
                author="contributor",
                body="Any update on this?",
                created_at=now - timedelta(hours=50),
                html_url="https://github.com/benni-os/mcp-forge/issues/42#issuecomment-1",
                is_maintainer=False,
            )
        ],
    )
    priority = analyzer.prioritize(sample_issue)

    body = b'{"action":"opened"}'
    secret = "probe-secret"
    sig = "sha256=" + hmac.new(secret.encode(), msg=body, digestmod=hashlib.sha256).hexdigest()

    deps = probe_dependencies()
    checks = {
        "core_dependencies_ok": all(deps.values()),
        "sla_prioritizer_ok": priority == Priority.CRITICAL,
        "webhook_hmac_ok": verify_signature(secret, body, sig)
        and not verify_signature(secret, body, "sha256=invalid"),
    }

    return {
        "package": "community-autopilot",
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "dependencies": deps,
        "checks": checks,
        "healthy": all(checks.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="community-autopilot runtime diagnostics")
    parser.add_argument("--json", action="store_true", help="Emit JSON diagnostics report")
    args = parser.parse_args()

    report = run_diagnostics()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        status = "HEALTHY" if report["healthy"] else "DEGRADED"
        print(f"community-autopilot Doctor [{status}] | Python {report['python_version']}")
        for name, ok in report["checks"].items():
            print(f"  [{'OK' if ok else 'FAIL'}] {name}")
    if not report["healthy"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
