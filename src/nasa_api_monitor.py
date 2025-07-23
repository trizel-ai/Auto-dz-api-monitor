# nasa_api_monitor.py — Real-time NASA API Monitoring via AUTO DZ ACT

import requests
import datetime

# NASA Open API endpoint for Earth assets (example placeholder)
NASA_API_URL = "https://api.nasa.gov/planetary/apod"
API_KEY = "DEMO_KEY"  # ⚠️ Replace with your personal API key from https://api.nasa.gov

def fetch_nasa_data():
    response = requests.get(NASA_API_URL, params={"api_key": API_KEY})
    if response.status_code == 200:
        data = response.json()
        return {
            "timestamp": str(datetime.datetime.utcnow()),
            "title": data.get("title", "N/A"),
            "date": data.get("date", "N/A"),
            "media_type": data.get("media_type", "N/A"),
        }
    else:
        return {"error": f"NASA API Error: {response.status_code}"}

def auto_dz_act_logic(data):
    status = "✅ ACTIVE" if "title" in data else "⚠️ INACTIVE"
    return status

if __name__ == "__main__":
    result = fetch_nasa_data()
    print("📡 NASA API Real-Time Monitor – AUTO DZ ACT")
    print("Timestamp:", result.get("timestamp", "N/A"))
    print("Status:", auto_dz_act_logic(result))
    print("Data:", result)
