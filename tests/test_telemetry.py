from community_autopilot.core import Analyzer, Issue, Priority, Settings
from community_autopilot.serve import TelemetryEngine, verify_signature


def test_telemetry_records_and_summarizes() -> None:
    tel = TelemetryEngine(max_history=10)
    tel.record_triage(latency_ms=1.5, priority="HIGH", gated=True, posted=False)
    tel.record_triage(latency_ms=0.8, priority="LOW", gated=False, posted=True)

    summary = tel.get_summary()
    assert summary["total_triaged"] == 2
    assert summary["gated_for_review"] == 1
    assert summary["responses_posted"] == 1
    assert summary["priority_distribution"] == {"HIGH": 1, "LOW": 1}


def test_core_and_serve_reexports() -> None:
    assert Analyzer is not None
    assert Issue is not None
    assert Priority.CRITICAL is not None
    assert Settings is not None
    assert verify_signature is not None
