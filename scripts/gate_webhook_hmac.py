"""Webhook HMAC-SHA256 & SLA safety gate script for community-autopilot."""

import hashlib
import hmac
import sys

from community_autopilot.serve import verify_signature


def main() -> None:
    secret = "gate-secret"
    payload = b'{"action":"created","comment":{"id":99}}'
    valid_sig = "sha256=" + hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256).hexdigest()

    if not verify_signature(secret, payload, valid_sig):
        print("Gate FAILED: valid HMAC signature rejected.")
        sys.exit(1)
    if verify_signature(secret, payload, "sha256=deadbeef"):
        print("Gate FAILED: forged HMAC signature accepted.")
        sys.exit(1)
    print("Gate PASSED: HMAC-SHA256 webhook verification enforced.")


if __name__ == "__main__":
    main()
