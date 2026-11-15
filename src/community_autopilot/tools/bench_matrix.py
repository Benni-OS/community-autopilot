"""Matrix Benchmark Suite for community-autopilot.

Sweeps synthetic GitHub issue batches through Analyzer.prioritize() and
Analyzer.build_context() to measure triage throughput (issues/sec).
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
from datetime import UTC, datetime, timedelta
from typing import Any

from community_autopilot.analyzer import Analyzer
from community_autopilot.config import Settings
from community_autopilot.models import Comment, Issue, IssueState


class BenchMatrixRunner:
    """Executes a multi-batch GitHub issue triage benchmark matrix."""

    def __init__(self, batch_sizes: list[int] | None = None, reps: int = 10) -> None:
        self.batch_sizes = batch_sizes or [10, 50, 100]
        self.reps = max(1, reps)

    def _build_sample_issue(self, idx: int) -> Issue:
        now = datetime.now(UTC)
        return Issue(
            repo="benni-os/mcp-forge",
            number=idx + 1,
            title=f"Issue #{idx + 1}: Support async streaming",
            body="Detailed reproduction steps for streaming transport.",
            author="contributor",
            state=IssueState.OPEN,
            labels=["enhancement"],
            assignees=[],
            created_at=now - timedelta(hours=30),
            updated_at=now - timedelta(hours=30),
            html_url=f"https://github.com/benni-os/mcp-forge/issues/{idx + 1}",
            comments=[
                Comment(
                    id=idx + 1,
                    author="contributor",
                    body="Following up on this request.",
                    created_at=now - timedelta(hours=25),
                    html_url=f"https://github.com/benni-os/mcp-forge/issues/{idx + 1}#issuecomment-1",
                    is_maintainer=False,
                )
            ],
        )

    def run_matrix(self) -> dict[str, Any]:
        """Run issue prioritization and context building across batch sizes."""
        settings = Settings(github_token="bench-token", nemesis_api_key="bench-key")
        analyzer = Analyzer(settings)
        results: list[dict[str, Any]] = []

        for batch in self.batch_sizes:
            issues = [self._build_sample_issue(i) for i in range(batch)]
            latencies_ms: list[float] = []
            for _ in range(self.reps):
                t0 = time.perf_counter()
                for issue in issues:
                    analyzer.prioritize(issue)
                    analyzer.build_context(issue)
                latencies_ms.append((time.perf_counter() - t0) * 1000.0)

            mean_ms = statistics.mean(latencies_ms)
            issues_per_sec = round((batch * 1000.0) / max(1e-6, mean_ms), 1)
            results.append(
                {
                    "batch_size": batch,
                    "mean_ms": round(mean_ms, 4),
                    "per_issue_ms": round(mean_ms / batch, 5),
                    "issues_per_sec": issues_per_sec,
                }
            )

        return {
            "package": "community-autopilot",
            "reps": self.reps,
            "matrix_results": results,
            "timestamp": int(time.time()),
        }

    @staticmethod
    def format_markdown_table(data: dict[str, Any]) -> str:
        """Render markdown summary table from matrix results."""
        lines = [
            f"# community-autopilot Triage Matrix Benchmark ({data['reps']} reps)",
            "",
            "| Batch Size | Mean Batch (ms) | Per Issue (ms) | Throughput (issues/s) |",
            "|---:|---:|---:|---:|",
        ]
        for row in data.get("matrix_results", []):
            lines.append(
                f"| {row['batch_size']} | {row['mean_ms']} | {row['per_issue_ms']} | {row['issues_per_sec']} |"
            )
        return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="community-autopilot Matrix Benchmark")
    parser.add_argument("--reps", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    runner = BenchMatrixRunner(reps=args.reps)
    res = runner.run_matrix()
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(runner.format_markdown_table(res))


if __name__ == "__main__":
    main()
