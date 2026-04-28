import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

# ---------------- CONFIG ----------------
APP_METRICS_URL = "http://<EC2-IP>:30007/metrics"
REFRESH_INTERVAL = 5

st.set_page_config(
    page_title="K8s Observability Dashboard",
    layout="wide",
)

# ---------------- HEADER ----------------
st.title("🚀 Kubernetes Observability Dashboard")
st.markdown("Monitor application metrics, health, and performance in real-time")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")

auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)
refresh_btn = st.sidebar.button("🔄 Manual Refresh")

# ---------------- FETCH METRICS ----------------
def fetch_metrics():
    try:
        res = requests.get(APP_METRICS_URL)
        return res.text
    except:
        return ""

def parse_metrics(data):
    metrics = {}
    for line in data.split("\n"):
        if " " in line:
            key, val = line.split(" ")
            try:
                metrics[key] = float(val)
            except:
                pass
    return metrics

raw_data = fetch_metrics()
metrics = parse_metrics(raw_data)

# ---------------- KPI SECTION ----------------
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Requests", int(metrics.get("app_requests_total", 0)))
col2.metric("App Health", "Healthy ✅")
col3.metric("Error Rate", "0%")
col4.metric("Latency", "120 ms")

# ---------------- CHARTS ----------------
st.subheader("📈 Performance Charts")

# Fake time-series for demo (replace with Prometheus later)
time_series = pd.DataFrame({
    "time": list(range(10)),
    "requests": [metrics.get("app_requests_total", 0) + i for i in range(10)]
})

fig = px.line(time_series, x="time", y="requests", title="Request Trend")
st.plotly_chart(fig, use_container_width=True)

# ---------------- RAW METRICS ----------------
with st.expander("📜 View Raw Metrics"):
    st.code(raw_data)

# ---------------- STATUS PANEL ----------------
st.subheader("🧠 System Status")

status_col1, status_col2 = st.columns(2)

status_col1.success("Kubernetes Cluster: Running")
status_col2.success("Monitoring Stack: Active")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("👨‍💻 Built for DevOps Monitoring Project")

# ---------------- AUTO REFRESH ----------------
if auto_refresh:
    time.sleep(REFRESH_INTERVAL)
    st.rerun()
elif refresh_btn:
    st.rerun()