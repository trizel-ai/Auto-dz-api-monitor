# cern_api_monitor.py — Real-time CERN API Monitoring
import requests
import datetime

CERN_API_URL = "https://atlas-opendata.web.cern.ch/api/sample"  # مثال placeholder

def fetch_cern_data():
    response = requests.get(CERN_API_URL)
    if response.status_code == 200:
        data = response.json()
        return {
            "timestamp": str(datetime.datetime.utcnow()),
            "sample_event": data.get("event", "N/A")
        }
    else:
        return {"error": f"CERN API Error: {response.status_code}"}

def auto_dz_act_logic(data):
    return "✅ ACTIVE" if "event" in data else "❌ INACTIVE"

if __name__ == "__main__":
    result = fetch_cern_data()
    print("🔬 CERN API Monitor – AUTO DZ ACT")
    print("Timestamp:", result.get("timestamp"))
    print("Status:", auto_dz_act_logic(result))
    print("Data:", result)
