# Architecture — `community-autopilot`

`community-autopilot` is an autonomous GitHub issue triage and maintainer responder with NEMESIS event tracing, SLA prioritization, HMAC-SHA256 webhook verification, and Slack operations alerts.

## Subpackage Layout

- `community_autopilot.core`:
  - Re-exports core domain primitives (`Analyzer`, `Settings`, `AutopilotRun`, `Issue`, `Comment`, `DraftResponse`, `Priority`, `GitHubWatcher`, `Responder`, and prompt templates).
- `community_autopilot.serve`:
  - `telemetry.py`: `TelemetryEngine` tracking P50/P90/P99 triage latencies, SLA priority distribution, gated drafts, and posted responses.
  - Re-exports `app` & `verify_signature` (FastAPI webhook server), `NemesisClient`, and `SlackNotifier`.
- `community_autopilot.tools`:
  - `doctor.py`: Runtime diagnostics probing dependencies, SLA priority classification, and webhook HMAC verification.
  - `bench_matrix.py`: `BenchMatrixRunner` sweeping synthetic issue batches through `Analyzer` prioritization and context assembly.
