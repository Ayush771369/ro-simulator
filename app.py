import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Import model functions
from model import *

# Import plotting functions
from plots import (
    generate_oat_plots,
    generate_tornado,
    generate_heatmap,
    generate_simulation_dashboard
)

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="RO Simulator", layout="wide")

st.title("💧 Reverse Osmosis Process Simulator")

# -------------------------------
# SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("Input Parameters")

delta_P = st.sidebar.slider("Pressure ΔP (bar)", 10.0, 100.0, 60.0)
C = st.sidebar.slider("Concentration (mol/L)", 0.1, 1.5, 0.6)
T = st.sidebar.slider("Temperature (°C)", 5.0, 60.0, 25.0)

A = st.sidebar.number_input(
    "Water Permeability A",
    value=3.5e-12,
    format="%.2e"
)

B = st.sidebar.number_input(
    "Salt Permeability B",
    value=3.5e-8,
    format="%.2e"
)

Am = st.sidebar.slider("Membrane Area (m²)", 100, 5000, 1000)

# -------------------------------
# BASELINE (for plots)
# -------------------------------
baseline = {
    "delta_P": delta_P,
    "C": C,
    "T": T,
    "A": A,
    "B": B,
    "Am": Am
}

# -------------------------------
# TABS
# -------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Simulator",
    "OAT Analysis",
    "Tornado",
    "Heatmap",
    "Equations",
    "Process Dashboard"
])

# ============================================================
# TAB 1 — SIMULATOR
# ============================================================
with tab1:
    st.subheader("📊 Results")

    pi = osmotic_pressure_bar(C, T)
    Jw = water_flux_LMH(delta_P, C, T, A)
    R  = salt_rejection_pct(delta_P, C, T, A, B)
    Qp = permeate_flow_m3h(delta_P, C, T, A, B, Am)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Osmotic Pressure π (bar)", f"{pi:.2f}")
    col2.metric("Water Flux Jw (LMH)", f"{Jw:.2f}")
    col3.metric("Salt Rejection (%)", f"{R:.2f}")
    col4.metric("Flow Rate Qp (m³/h)", f"{Qp:.2f}")

    if delta_P < pi:
        st.warning("⚠️ Applied pressure is less than osmotic pressure → No filtration occurs!")

    st.divider()

    # Extra graph
    st.subheader("📈 Pressure vs Water Flux")

    pressure_range = np.linspace(20, 80, 50)
    flux_values = [water_flux_LMH(p, C, T, A) for p in pressure_range]

    fig, ax = plt.subplots()
    ax.plot(pressure_range, flux_values)
    ax.set_xlabel("Pressure (bar)")
    ax.set_ylabel("Water Flux (LMH)")
    ax.set_title("Effect of Pressure on Flux")

    st.pyplot(fig)

# ============================================================
# TAB 2 — OAT
# ============================================================
with tab2:
    st.subheader("📊 OAT Sensitivity Analysis")

    fig = generate_oat_plots(baseline)
    st.pyplot(fig)

# ============================================================
# TAB 3 — TORNADO
# ============================================================
with tab3:
    st.subheader("🌪️ Tornado Chart")

    fig = generate_tornado(baseline)
    st.pyplot(fig)

# ============================================================
# TAB 4 — HEATMAP
# ============================================================
with tab4:
    st.subheader("🔥 Sensitivity Heatmap")

    fig = generate_heatmap(baseline)
    st.pyplot(fig)

# ============================================================
# TAB 5 — EQUATIONS
# ============================================================
with tab5:
    st.header("📘 Governing Equations")

    st.subheader("Osmotic Pressure")
    st.latex(r"\pi = i \cdot C \cdot R \cdot T")

    st.markdown("""
    - π = Osmotic Pressure (bar)  
    - i = van’t Hoff factor  
    - C = Concentration  
    - R = Gas constant  
    - T = Temperature (K)
    """)

    st.divider()

    st.subheader("Water Flux")
    st.latex(r"J_w = A \cdot (\Delta P - \pi)")

    st.markdown("""
    - Jw = Water flux  
    - A = Membrane permeability  
    - ΔP = Applied pressure  
    """)

    st.divider()

    st.subheader("Salt Rejection")
    st.latex(r"R = \left(1 - \frac{C_p}{C_f}\right) \times 100")

    st.markdown("""
    - R = Salt rejection (%)  
    """)

    st.divider()

    st.subheader("Permeate Flow Rate")
    st.latex(r"Q_p = J_w \cdot A_m")

    st.markdown("""
    - Qp = Flow rate  
    """)

    st.divider()

    st.subheader("Model Code Logic")

    st.code("""
Jw = A * max((ΔP - π), 0)
Cp = B * Cs / (Jw + B)
R  = (1 - Cp / Cf) * 100
Qp = Jw * Am
""")

# ============================================================
# TAB 6 — PROCESS DASHBOARD
# ============================================================
with tab6:
    st.header("📊 Process Simulation Dashboard")

    st.markdown("""
    This dashboard visualizes the complete behavior of the reverse osmosis system
    under typical operating conditions.
    """)

    fig = generate_simulation_dashboard()
    st.pyplot(fig)