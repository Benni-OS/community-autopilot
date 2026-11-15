"""Triage throughput benchmark script for community-autopilot."""

from community_autopilot.tools.bench_matrix import BenchMatrixRunner


def main() -> None:
    runner = BenchMatrixRunner(batch_sizes=[10, 50, 100], reps=10)
    data = runner.run_matrix()
    print(runner.format_markdown_table(data))


if __name__ == "__main__":
    main()
