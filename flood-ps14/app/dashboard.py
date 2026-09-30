"""Streamlit dashboard. Run: streamlit run app/dashboard.py"""
import os
import sys
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.run_all import run  # noqa: E402
from src.replay import replay  # noqa: E402

st.set_page_config(page_title="PS14 Flood Response", layout="wide")
st.title("Flood Prediction & Response - PS 14")
day = st.slider("Simulation day", 0, 119, 60)


@st.cache_data
def get(d):
    return run(d)


r = get(day)
v = pd.DataFrame(r["vulnerability"])
c1, c2, c3 = st.columns(3)
c1.metric("High-risk zones", int((v.tier == "HIGH").sum()))
c2.metric("Alerts issued", len(r["alerts"]))
c3.metric("Model AUC", f"{r['metrics']['auc']:.2f}" if r["metrics"]["auc"] else "n/a")
st.map(v.rename(columns={"lon": "longitude", "lat": "latitude"}))
st.subheader("Vulnerability ranking")
st.dataframe(v[["zone_id", "flood_prob", "population", "vulnerability", "tier"]])
col_a, col_b = st.columns(2)
col_a.subheader("Feature importance")
col_a.bar_chart(pd.Series(r["importance"]))
col_b.subheader("Top zone explanation")
col_b.json(r["top_zone_explanation"])
st.subheader("Resource allocation")
st.dataframe(pd.DataFrame(r["allocation"]))
st.subheader("Evacuation routes")
st.write({k: " -> ".join(p) for k, p in r["routes"].items()})
st.subheader("Social media distress signals")
st.bar_chart(pd.Series(r["social_signals"]))
st.subheader("Alerts")
st.dataframe(pd.DataFrame(r["alerts"]))
st.subheader("Event replay")
st.line_chart(pd.DataFrame(replay()).set_index("day"))
