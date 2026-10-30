import pandas as pd
import numpy as np

# 1. Server Telemetry Logs
np.random.seed(42)
n_records = 300
timestamps = pd.date_range("2026-10-30 08:00:00", periods=n_records, freq="1min")
servers = np.random.choice(["node-us-east-1", "node-us-west-2", "node-eu-central-1", "node-ap-south-1"], size=n_records)
cpu_usage = np.random.normal(48, 12, size=n_records).clip(10, 99)
mem_usage = np.random.normal(62, 8, size=n_records).clip(20, 98)
latency_ms = np.random.exponential(45, size=n_records) + 15
status_codes = np.random.choice([200, 200, 200, 201, 304, 400, 404, 500, 503], size=n_records, p=[0.75, 0.1, 0.05, 0.03, 0.02, 0.02, 0.01, 0.01, 0.01])

# Inject 6 severe anomalies (DDoS/Spike simulation)
for idx in [25, 88, 142, 210, 275]:
    cpu_usage[idx] = 98.7
    latency_ms[idx] = 1850.5
    status_codes[idx] = 503

df_server = pd.DataFrame({
    "Timestamp": timestamps,
    "Server_Node": servers,
    "CPU_Usage_Pct": np.round(cpu_usage, 1),
    "Memory_Usage_Pct": np.round(mem_usage, 1),
    "Response_Latency_MS": np.round(latency_ms, 2),
    "HTTP_Status": status_codes
})
df_server.to_csv("data/server_system_telemetry.csv", index=False)

# 2. Financial Transactions Excel
n_tx = 250
tx_ids = [f"TXN-{10000+i}" for i in range(n_tx)]
amounts = np.random.exponential(120, size=n_tx) + 10
merchants = np.random.choice(["Amazon Cloud", "Stripe Gateway", "Uber Mobility", "Netflix Stream", "Apple Store", "Crypto Swift", "Shell Fuel"], size=n_tx)
card_types = np.random.choice(["Visa Platinum", "Mastercard World", "Amex Corporate"], size=n_tx)
risk_scores = np.random.uniform(1, 40, size=n_tx)

# Inject financial fraud outliers
for idx in [15, 67, 134, 199]:
    amounts[idx] = 9450.00
    risk_scores[idx] = 99.4

df_tx = pd.DataFrame({
    "Transaction_ID": tx_ids,
    "Merchant": merchants,
    "Card_Type": card_types,
    "Amount_USD": np.round(amounts, 2),
    "Fraud_Risk_Score": np.round(risk_scores, 1),
    "Is_Flagged": [True if s > 80 else False for s in risk_scores]
})
df_tx.to_excel("data/financial_fraud_analysis.xlsx", index=False)
print("Sample datasets generated successfully!")
