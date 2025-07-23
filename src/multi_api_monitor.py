# multi_api_monitor.py — Unified Scientific Monitor

from nasa_api_monitor import fetch_nasa_data
from cern_api_monitor import fetch_cern_data
from planck_api_monitor import fetch_planck_data

from decision_logic import analyze_vs_series
from email_alert import send_email_alert


def run_unified_monitor():
    print("🧠 Unified Scientific Monitor: START\n")

    nasa_data = fetch_nasa_data()
    cern_data = fetch_cern_data()
    planck_data = fetch_planck_data()

    results = {
        "NASA": analyze_vs_series(nasa_data),
        "CERN": analyze_vs_series(cern_data),
        "PLANCK": analyze_vs_series(planck_data)
    }

    for source, result in results.items():
        status = result.get("status")
        vs_value = result["details"].get("vs_mean", 0)
        reason = result["details"].get("reason", "No reason provided")

        print(f"🔍 {source} → ∇S = {vs_value:.2f} | Status: {status}")

        if status == "ALERT":
            subject = f"🚨 STOE Alert from {source}: ∇S Threshold Breach"
            body = f"""
AUTO DZ ACT has detected a critical phase change in ∇S signal.

📡 Source: {source}
📈 ∇S Value: {vs_value:.2f}
📊 Status: {status}

Reason:
{reason}

🧠 STOE framework recommends initiating a follow-up investigation.
"""
            send_email_alert(subject, body)


if __name__ == "__main__":
    run_unified_monitor()
