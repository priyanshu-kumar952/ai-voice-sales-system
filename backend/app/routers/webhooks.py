import hashlib
import hmac
import httpx
from datetime import datetime, timezone

from fastapi import APIRouter, Header, HTTPException, Request

from app.core.config import settings
from app.models.call import CallCreate, CallUpdate
from app.services.call_service import CallService


router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)


@router.post("/retell")
async def retell_webhook(
    request: Request,
    x_webhook_signature: str | None = Header(default=None),
):
    body = await request.body()

    if not x_webhook_signature:
        raise HTTPException(
            status_code=401,
            detail="Missing webhook signature",
        )

    expected_signature = hmac.new(
        settings.webhook_secret.encode(),
        body,
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

    payload = await request.json()

    if payload.get("event") == "call_started":
        call = CallService.create_call(
            CallCreate(
                call_id=payload["call_id"],
                phone_number=payload.get("phone_number"),
                status="started",
            )
        )

        return {
            "success": True,
            "message": "Call started",
            "call": call,
        }

    if payload.get("event") == "call_ended":
        call = CallService.update_call(
            payload["call_id"],
            CallUpdate(
                status="completed",
                ended_at=datetime.now(timezone.utc),
                duration_seconds=payload.get("duration_seconds"),
                transcript=payload.get("transcript"),
            ),
        )

        if call is None:
            raise HTTPException(
                status_code=404,
                detail="Call not found",
            )

        n8n_payload = {
            "event": "call_ended",
            "call_id": payload["call_id"],
            "phone_number": payload.get("phone_number"),
            "duration_seconds": payload.get("duration_seconds"),
            "transcript": payload.get("transcript"),
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            n8n_response = await client.post(
                settings.n8n_webhook_url,
                json=n8n_payload,
                headers={
                    "X-N8N-Webhook-Secret": settings.n8n_webhook_secret,
                },
            )

        if n8n_response.status_code >= 400:
            raise HTTPException(
                status_code=502,
                detail="Failed to forward call to n8n",
            )

        return {
            "success": True,
            "message": "Call ended and forwarded to n8n",
            "call": call,
        }

    return {
        "success": True,
        "message": "Webhook received",
        "event": payload,
    }