"""Serving, webhook, notification, and telemetry subpackage for community-autopilot."""

from community_autopilot.nemesis import NemesisClient, NemesisEvent
from community_autopilot.serve.telemetry import TelemetryEngine
from community_autopilot.slack import SlackNotifier
from community_autopilot.webhook import app, verify_signature

__all__ = [
    "NemesisClient",
    "NemesisEvent",
    "SlackNotifier",
    "TelemetryEngine",
    "app",
    "verify_signature",
]
