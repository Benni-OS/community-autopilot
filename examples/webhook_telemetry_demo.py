"""Webhook HMAC verification + TelemetryEngine example for community-autopilot."""

import hashlib
import hmac
import json

from community_autopilot.serve import TelemetryEngine, verify_signature


def main() -> None:
    secret = "benni-webhook-secret"
    payload = b'{"action":"opened","issue":{"number":42}}'
    signature = "sha256=" + hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256).hexdigest()

    is_valid = verify_signature(secret, payload, signature)
    telemetry = TelemetryEngine()
    telemetry.record_triage(latency_ms=1.45, priority="HIGH", gated=True, posted=False)

    print("Webhook Signature Valid:", is_valid)
    print("Telemetry:", json.dumps(telemetry.get_summary(), indent=2))


if __name__ == "__main__":
    main()
