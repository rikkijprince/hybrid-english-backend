# hybrid-english-backend/backend/modules/booking/pricing_service.py
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
FEE_FILE = BASE_DIR / "fee.json"


def read_fee_file():
    print("🔍 Reading fee.json from:", FEE_FILE)

    if not os.path.exists(FEE_FILE):
        print("❌ fee.json NOT FOUND")
        return {
            "price_eur": None,
            "session_length": None
        }

    try:
        with open(FEE_FILE, "r", encoding="utf-8") as f:
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
