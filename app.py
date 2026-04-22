import streamlit as st
from model import *
from plots import *

st.set_page_config(layout="wide")

st.title("💧 RO Process Simulator")

# Sidebar inputs
delta_P = st.sidebar.slider("Pressure", 10.0, 100.0, 60.0)
C = st.sidebar.slider("Concentration", 0.1, 1.5, 0.6)
T = st.sidebar.slider("Temperature", 5.0, 60.0, 25.0)
A = st.sidebar.number_input("A", value=3.5e-12, format="%.2e")
B = st.sidebar.number_input("B", value=3.5e-8, format="%.2e")
Am = st.sidebar.slider("Area", 100, 5000, 1000)

baseline = {
    "delta_P": delta_P,
    "C": C,
    "T": T,
    "A": A,
    "B": B,
    "Am": Am
}

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Simulator",
    "OAT Analysis",
    "Tornado",
    "Heatmap"
])

# ---------- TAB 1 ----------
with tab1:
    pi = osmotic_pressure_bar(C, T)
    Jw = water_flux_LMH(delta_P, C, T, A)
    R  = salt_rejection_pct(delta_P, C, T, A, B)
    Qp = permeate_flow_m3h(delta_P, C, T, A, B, Am)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("π", f"{pi:.2f}")
    col2.metric("Jw", f"{Jw:.2f}")
    col3.metric("R", f"{R:.2f}")
    col4.metric("Qp", f"{Qp:.2f}")

# ---------- TAB 2 ----------
with tab2:
    st.subheader("OAT Sensitivity Analysis")
    fig = generate_oat_plots(baseline)
    st.pyplot(fig)

# ---------- TAB 3 ----------
with tab3:
    st.subheader("Tornado Chart")
    fig = generate_tornado(baseline)
    st.pyplot(fig)

# ---------- TAB 4 ----------
with tab4:
    st.subheader("Sensitivity Heatmap")
    fig = generate_heatmap(baseline)
    st.pyplot(fig)