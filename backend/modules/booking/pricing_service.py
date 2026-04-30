# hybrid-english-backend/backend/modules/booking/pricing_service.py

import json
import os

FEE_FILE = os.path.join(os.path.dirname(__file__), "fee.json")


def read_fee_file():
    print("🔍 Trying to read fee.json...")
    print("📁 Expected path:", FEE_FILE)

    # Check if file exists
    if not os.path.exists(FEE_FILE):
        print("❌ fee.json DOES NOT EXIST at this path!")
        return {
            "price_eur": None,
            "session_length": None
        }

    try:
        with open(FEE_FILE, "r") as f:
            data = json.load(f)
            print("✅ fee.json loaded successfully:", data)
            return data

    except Exception as e:
        print("❌ ERROR reading fee.json:", str(e))
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
