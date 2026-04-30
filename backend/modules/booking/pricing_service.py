# hybrid-english-backend/backend/modules/booking/pricing_service.py
import json
import os

FEE_FILE = os.path.join(os.path.dirname(__file__), "fee.json")


def read_fee_file():
    print("🔍 Reading fee.json from:", FEE_FILE)

    if not os.path.exists(FEE_FILE):
        print("❌ fee.json NOT FOUND")
        return {
            "price_eur": None,
            "session_length": None
        }

    try:
        with open(FEE_FILE, "r") as f:
            data = json.load(f)
            print("✅ fee.json loaded:", data)
            return data

    except Exception as e:
        print("❌ JSON ERROR:", str(e))
        return {
            "price_eur": None,
            "session_length": None
        }


def get_pricing():
    data = read_fee_file()

    return {
        "price_eur": data.get("price_eur"),
        "session_length": data.get("session_length")
    }
