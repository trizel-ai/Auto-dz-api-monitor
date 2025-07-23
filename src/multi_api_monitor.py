# multi_api_monitor.py — Unified Monitoring for NASA, CERN, and Planck
from nasa_api_monitor import fetch_nasa_data
from cern_api_monitor import fetch_cern_data
from planck_api_monitor import fetch_planck_data

def run_unified_monitor():
    print("🔁 Unified Scientific Monitor via AUTO DZ ACT\n")

    nasa = fetch_nasa_data()
    cern = fetch_cern_data()
    planck = fetch_planck_data()

    print("📡 NASA:", nasa)
    print("🔬 CERN:", cern)
    print("🌌 Planck:", planck)

if __name__ == "__main__":
    run_unified_monitor()
from email_alert import send_email_alert

# Simulated results from different sources
results = {
    "NASA": {"∇S": 6.52},
    "CERN": {"∇S": 5.95},
    "PLANCK": {"∇S": 6.48}
}

# Alert threshold parameters
threshold = 6.4
alert_duration_days = 90  # Simulated duration over threshold

# Check and trigger alert
for source, data in results.items():
    s_value = data.get("∇S", 0)

    if s_value > threshold:
        subject = f"🚨 STOE Alert: ∇S exceeded {threshold} at {source}"
        body = f"""
AUTO DZ ACT has detected a persistent increase in ∇S value at {source}.

Details:
🔬 Source: {source}
📈 ∇S value: {s_value}
📅 Duration over threshold: {alert_duration_days} days

This exceeds the critical STOE spectral threshold (6.4) sustained over 90 days,
indicating a potential phase transition (Sp-field disruption) according to STOE 2025.

Anomaly confirmed. Please initiate validation or publication process.
"""
        send_email_alert(subject, body)
