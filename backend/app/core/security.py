import hashlib
import hmac

from fastapi import Header, HTTPException

from app.core.config import settings


def verify_webhook_signature(
    x_webhook_signature: str | None = Header(default=None),
    raw_body: bytes = b"",
):
    if not x_webhook_signature:
        raise HTTPException(
            status_code=401,
            detail="Missing webhook signature",
        )

    expected_signature = hmac.new(
        settings.webhook_secret.encode(),
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(
        x_webhook_signature,
        expected_signature,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook signature",
        )

    return True