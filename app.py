import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from model import *
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

A = st.sidebar.number_input("Water Permeability A", value=3.5e-12, format="%.2e")
B = st.sidebar.number_input("Salt Permeability B", value=3.5e-8, format="%.2e")
Am = st.sidebar.slider("Membrane Area (m²)", 100, 5000, 1000)

# -------------------------------
# BASELINE
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
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Simulator",
    "Sensitivity Analysis",
    "Future Prospects"
])

# ============================================================
# TAB 1 — OVERVIEW
# ============================================================
with tab1:
    st.header("📘 Project Overview")

    st.markdown("""
This project presents a comprehensive simulation and analysis of a **Reverse Osmosis (RO) desalination system**, 
widely used for converting saline water into potable water. The simulator models key transport phenomena such as 
osmotic pressure, water flux, salt rejection, and permeate flow rate.

The platform integrates **real-time simulation, sensitivity analysis, and system-level visualization** to provide 
insight into how parameters like pressure, temperature, concentration, and membrane properties affect system performance. 
It serves both as an engineering tool and an educational interface for membrane separation processes.
""")

    st.divider()

    st.header("📐 Governing Equations")

    # Osmotic Pressure
    st.subheader("Osmotic Pressure")
    st.latex(r"\pi = i \cdot C \cdot R \cdot T")

    st.markdown("""
- π = Osmotic Pressure  
- i = van’t Hoff factor  
- C = Concentration  
- R = Gas constant  
- T = Temperature (K)  
""")

    st.divider()

    # Water Flux
    st.subheader("Water Flux")
    st.latex(r"J_w = A \cdot (\Delta P - \pi)")

    st.divider()

    # Salt Flux
    st.subheader("Salt Flux")
    st.latex(r"J_s = B \cdot (C_s - C_p)")

    st.markdown("""
- Js = Salt flux  
- B = Salt permeability  
- Cs = membrane surface concentration  
- Cp = permeate concentration  
""")

    st.divider()

    # Salt Rejection
    st.subheader("Salt Rejection")
    st.latex(r"R = \left(1 - \frac{C_p}{C_f}\right) \times 100")

    st.divider()

    # Flow Rate
    st.subheader("Permeate Flow Rate")
    st.latex(r"Q_p = J_w \cdot A_m")

# ============================================================
# TAB 2 — SIMULATOR
# ============================================================
with tab2:
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

    st.subheader("📊 Process Simulation Dashboard")

    fig = generate_simulation_dashboard()
    st.pyplot(fig)

# ============================================================
# TAB 3 — SENSITIVITY ANALYSIS
# ============================================================
with tab3:
    st.header("📊 Sensitivity Analysis")

    st.subheader("🔍 One-at-a-Time (OAT) Analysis")
    fig_oat = generate_oat_plots(baseline)
    st.pyplot(fig_oat)

    st.divider()

    st.subheader("🌪️ Tornado Chart")
    fig_tornado = generate_tornado(baseline)
    st.pyplot(fig_tornado)

    st.divider()

    st.subheader("🔥 Sensitivity Heatmap")
    fig_heatmap = generate_heatmap(baseline)
    st.pyplot(fig_heatmap)

# ============================================================
# TAB 4 — FUTURE PROSPECTS
# ============================================================
with tab4:
    st.header("🚀 Future Prospects")

    st.markdown("""
This project provides a strong foundation for developing a full-scale digital simulator of reverse osmosis systems. 
Several enhancements can be made to extend its capabilities toward industrial and research applications.

### 🔧 Model Enhancements
- Multi-stage RO system simulation  
- Energy consumption and efficiency modeling  
- Fouling and scaling effects  
- Pressure drop and realistic flow modeling  

### 📊 Advanced Analysis
- Multi-variable sensitivity analysis  
- Optimization of operating conditions  
- Uncertainty and robustness analysis  

### 🤖 AI Integration
- Machine learning for performance prediction  
- Smart parameter recommendation systems  
- Integration with real plant datasets  

### 🌐 Product Development
- Full-stack deployment (React + FastAPI)  
- User authentication and saved simulations  
- Data upload and custom simulations  
- Cloud-based engineering tool  

### 🧪 Research Extensions
- Extend to nanofiltration and ultrafiltration  
- Industrial plant-scale simulation  
- CFD-based flow modeling  

---

👉 This project can evolve into a **complete digital twin of membrane separation systems**, 
bridging theoretical modeling with real-world engineering applications.
""")