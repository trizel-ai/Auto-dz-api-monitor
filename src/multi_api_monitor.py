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
