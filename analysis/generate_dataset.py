import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

SEED = 42
N = 4000
START_DATE = datetime(2026, 5, 1)
OUT = Path(__file__).resolve().parents[1] / "data" / "synthetic_payment_transactions.csv"

MARKETS = ["India", "UK", "UAE", "Singapore", "Spain", "Poland"]
MARKET_W = [0.34, 0.17, 0.14, 0.12, 0.12, 0.11]
SEGMENTS = ["SMB", "Mid-Market", "Enterprise"]
SEGMENT_W = [0.58, 0.29, 0.13]
METHODS = ["Card", "UPI", "Wallet", "Bank Transfer", "BNPL"]
BASE_SUCCESS = {"Card": 0.875, "UPI": 0.905, "Wallet": 0.925, "Bank Transfer": 0.895, "BNPL": 0.945}
MARKET_ADJUST = {"India": -0.008, "UK": 0.010, "UAE": -0.012, "Singapore": 0.012, "Spain": 0.000, "Poland": -0.004}
FAILURES = [
    ("issuer_decline", "issuer_bank", 0.24, True),
    ("insufficient_funds", "customer", 0.18, False),
    ("authentication_failed", "customer", 0.18, True),
    ("network_timeout", "gateway", 0.15, True),
    ("incorrect_details", "customer", 0.10, True),
    ("bank_downtime", "gateway", 0.08, True),
    ("merchant_configuration", "business", 0.07, False),
]


def choose(items, weights):
    return random.choices(items, weights=weights, k=1)[0]


def generate():
    random.seed(SEED)
    rows = []
    for i in range(1, N + 1):
        market = choose(MARKETS, MARKET_W)
        segment = choose(SEGMENTS, SEGMENT_W)
        if market == "India":
            method = choose(METHODS, [0.42, 0.36, 0.10, 0.08, 0.04])
        else:
            method = choose(METHODS, [0.67, 0.02, 0.12, 0.12, 0.07])

        customer_type = choose(["New", "Returning"], [0.33, 0.67])
        date = START_DATE + timedelta(days=random.randint(0, 119))

        if segment == "SMB":
            amount = max(4, random.lognormvariate(3.45, 0.62))
        elif segment == "Mid-Market":
            amount = max(8, random.lognormvariate(4.25, 0.55))
        else:
            amount = max(20, random.lognormvariate(5.05, 0.48))
        amount = round(min(amount, 1800), 2)

        p_success = BASE_SUCCESS[method] + MARKET_ADJUST[market]
        if customer_type == "New":
            p_success -= 0.012
        if segment == "Enterprise":
            p_success += 0.006

        success = random.random() < p_success
        if success:
            status, source, reason, retry = "Success", "", "", "No"
            latency = int(max(110, random.gauss(520, 165)))
            ticket = "Yes" if random.random() < 0.012 else "No"
        else:
            reason, source, _, retry_bool = choose(FAILURES, [x[2] for x in FAILURES])
            status = "Failed"
            retry = "Yes" if retry_bool else "No"
            latency = int(max(1100, random.gauss(3100, 700))) if reason in ("network_timeout", "bank_downtime") else int(max(150, random.gauss(710, 210)))
            ticket_p = 0.23 + (0.07 if customer_type == "New" else 0) + (0.09 if reason in ("merchant_configuration", "bank_downtime", "network_timeout") else 0)
            ticket = "Yes" if random.random() < ticket_p else "No"

        rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "transaction_id": f"TXN{i:06d}",
            "merchant_id": f"M{random.randint(1, 130):03d}",
            "market": market,
            "merchant_segment": segment,
            "customer_type": customer_type,
            "payment_method": method,
            "amount_usd": amount,
            "status": status,
            "failure_source": source,
            "failure_reason": reason,
            "retry_eligible": retry,
            "latency_ms": latency,
            "support_ticket": ticket,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    generate()
