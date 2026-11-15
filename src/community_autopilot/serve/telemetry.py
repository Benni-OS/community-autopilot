"""Real-Time Telemetry Engine for community-autopilot.

Captures issue triage latencies (P50, P90, P99), SLA priority distribution,
approval gate counts, and autonomous response counts.
"""

from __future__ import annotations

import statistics
import time
from typing import Any


class TelemetryEngine:
    """Collects real-time GitHub triage and SLA prioritization metrics."""

    def __init__(self, max_history: int = 500) -> None:
        self.max_history = max_history
        self.latencies_ms: list[float] = []
        self.priority_counts: dict[str, int] = {}
        self.gated_count: int = 0
        self.posted_count: int = 0
        self.start_time = time.time()

    def record_triage(
        self,
        latency_ms: float,
        priority: str,
        gated: bool = False,
        posted: bool = False,
    ) -> None:
        """Record metrics for a single issue triage decision."""
        self.latencies_ms.append(latency_ms)
        if len(self.latencies_ms) > self.max_history:
            self.latencies_ms.pop(0)

        self.priority_counts[priority] = self.priority_counts.get(priority, 0) + 1
        if gated:
            self.gated_count += 1
        if posted:
            self.posted_count += 1

    def _percentile(self, values: list[float], p: float) -> float:
        if not values:
            return 0.0
        sorted_v = sorted(values)
        idx = min(len(sorted_v) - 1, int(len(sorted_v) * p))
        return round(sorted_v[idx], 4)

    def get_summary(self) -> dict[str, Any]:
        """Return aggregated triage latency percentiles and SLA priority metrics."""
        uptime = max(0.001, time.time() - self.start_time)
        return {
            "uptime_seconds": round(uptime, 2),
            "total_triaged": len(self.latencies_ms),
            "gated_for_review": self.gated_count,
            "responses_posted": self.posted_count,
            "latency_p50_ms": self._percentile(self.latencies_ms, 0.50),
            "latency_p90_ms": self._percentile(self.latencies_ms, 0.90),
            "latency_p99_ms": self._percentile(self.latencies_ms, 0.99),
            "mean_latency_ms": (
                round(statistics.mean(self.latencies_ms), 4) if self.latencies_ms else 0.0
            ),
            "priority_distribution": dict(self.priority_counts),
        }
