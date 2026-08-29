from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_payment_transactions.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
RECOVERY_ASSUMPTION = 0.25

df = pd.read_csv(DATA, parse_dates=["date"])
failed = df[df["status"] == "Failed"].copy()
success = df[df["status"] == "Success"].copy()
retry = failed[failed["retry_eligible"] == "Yes"].copy()

success_rate = len(success) / len(df)
failed_gmv = failed["amount_usd"].sum()
ticket_rate = (df["support_ticket"] == "Yes").mean()
retry_eligible_failures = len(retry)
projected_recovered_txns = round(retry_eligible_failures * RECOVERY_ASSUMPTION)
projected_success_rate = (len(success) + projected_recovered_txns) / len(df)
projected_recovered_gmv = retry["amount_usd"].sum() * RECOVERY_ASSUMPTION
lift_pp = (projected_success_rate - success_rate) * 100

method = df.groupby("payment_method").agg(
    attempts=("transaction_id", "count"),
    successes=("status", lambda s: (s == "Success").sum()),
    support_tickets=("support_ticket", lambda s: (s == "Yes").sum()),
)
method["success_rate"] = method["successes"] / method["attempts"]
method["support_ticket_rate"] = method["support_tickets"] / method["attempts"]
method["failed_gmv"] = failed.groupby("payment_method")["amount_usd"].sum()
method = method.sort_values("success_rate")
method.to_csv(OUT / "payment_method_summary.csv")

market = df.groupby("market").agg(
    attempts=("transaction_id", "count"),
    successes=("status", lambda s: (s == "Success").sum()),
)
market["success_rate"] = market["successes"] / market["attempts"]
market["failed_gmv"] = failed.groupby("market")["amount_usd"].sum()
market = market.sort_values("success_rate")
market.to_csv(OUT / "market_summary.csv")

failure = failed.groupby(["failure_reason", "failure_source"]).agg(
    failure_count=("transaction_id", "count"),
    failed_gmv=("amount_usd", "sum"),
).reset_index()
failure["share_of_failures"] = failure["failure_count"] / len(failed)
failure = failure.sort_values("failure_count", ascending=False)
failure.to_csv(OUT / "failure_summary.csv", index=False)

summary = pd.DataFrame([
    ["total_attempts", len(df)],
    ["success_rate", success_rate],
    ["failed_gmv_usd", failed_gmv],
    ["support_ticket_rate", ticket_rate],
    ["retry_eligible_failures", retry_eligible_failures],
    ["projected_success_rate_25pct_recovery", projected_success_rate],
    ["projected_recovered_gmv_usd", projected_recovered_gmv],
    ["success_rate_lift_percentage_points", lift_pp],
], columns=["metric", "value"])
summary.to_csv(OUT / "summary_metrics.csv", index=False)

print("Fintech Payment Reliability & Growth Analytics")
print(f"Total attempts: {len(df):,}")
print(f"Payment success rate: {success_rate:.2%}")
print(f"Failed GMV: ${failed_gmv:,.2f}")
print(f"Support-ticket rate: {ticket_rate:.2%}")
print(f"Lowest-performing method: {method.index[0]} ({method.iloc[0]['success_rate']:.2%})")
print(f"Lowest-performing market: {market.index[0]} ({market.iloc[0]['success_rate']:.2%})")
print(f"Top failure reason: {failure.iloc[0]['failure_reason']} ({failure.iloc[0]['share_of_failures']:.2%})")
print(f"25% retry-recovery scenario: +{lift_pp:.2f} pp success rate, ${projected_recovered_gmv:,.2f} recovered GMV")
