from community_autopilot.tools.bench_matrix import BenchMatrixRunner
from community_autopilot.tools.doctor import run_diagnostics


def test_doctor_diagnostics_healthy() -> None:
    report = run_diagnostics()
    assert report["package"] == "community-autopilot"
    assert report["healthy"] is True
    assert all(report["checks"].values())


def test_bench_matrix_runner() -> None:
    runner = BenchMatrixRunner(batch_sizes=[5, 10], reps=3)
    data = runner.run_matrix()
    assert data["reps"] == 3
    assert len(data["matrix_results"]) == 2
    md = runner.format_markdown_table(data)
    assert "| Batch Size | Mean Batch (ms) |" in md
