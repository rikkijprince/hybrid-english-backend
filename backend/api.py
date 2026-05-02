from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import stripe
import os

from modules.booking.calendar_service import (
    get_available_slots,
    create_tentative_event,
    confirm_event,
    cancel_event,
    is_slot_still_available
)

from modules.booking.pricing_service import get_pricing
from modules.booking.payment_service import create_checkout_session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rikkijprince.github.io",
        "http://localhost:4000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Pricing
# -------------------------
@app.get("/api/price")
def api_price():
    return get_pricing()


# -------------------------
# Slots
# -------------------------
@app.get("/api/slots")
def api_slots():
    slots = get_available_slots()

    return [
        {
            "label": slot.strftime("%a %d %b | %H:%M"),
            "datetime": slot.isoformat()
        }
        for slot in slots
    ]


# -------------------------
# Booking
# -------------------------
class BookingRequest(BaseModel):
    slot: str


@app.post("/api/book")
def api_book(request: BookingRequest):
    selected_slot = datetime.fromisoformat(request.slot)

    if not is_slot_still_available(selected_slot):
        raise HTTPException(
            status_code=400,
            detail="Slot no longer available."
        )

    user = {
        "username": "Hybrid English Student"
    }

    event_id = create_tentative_event(user, selected_slot)

    pricing = get_pricing()
    amount = pricing["price_eur"]

    checkout_url, session_id = create_checkout_session(
        amount=amount,
        metadata={
            "event_id": event_id
        }
    )

    return {
        "checkout_url": checkout_url,
        "session_id": session_id
    }


# -------------------------
# Stripe Webhook
# -------------------------
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")


@app.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        event_id = session["metadata"]["event_id"]
        confirm_event(event_id)

    elif event["type"] in [
        "checkout.session.expired",
        "payment_intent.payment_failed"
    ]:
        session = event["data"]["object"]
        event_id = session["metadata"]["event_id"]
        cancel_event(event_id)

    return {"status": "success"}
