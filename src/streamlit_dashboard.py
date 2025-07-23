import streamlit as st
import datetime
from multi_api_monitor import run_all_monitors

st.set_page_config(page_title="AUTO DZ ACT Dashboard", layout="wide")

st.title("🌐 AUTO DZ ACT – Scientific Monitoring Dashboard")
st.markdown(f"Updated at: {datetime.datetime.utcnow()} UTC")

results = run_all_monitors()

for source, data in results.items():
    st.subheader(f"🔬 Source: {source}")
    for k, v in data.items():
        st.write(f"**{k}**: {v}")
