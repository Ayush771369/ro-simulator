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

    st.subheader("Osmotic Pressure")
    st.latex(r"\pi = i \cdot C \cdot R \cdot T")

    st.divider()

    st.subheader("Water Flux")
    st.latex(r"J_w = A \cdot (\Delta P - \pi)")

    st.divider()

    st.subheader("Salt Flux")
    st.latex(r"J_s = B \cdot (C_s - C_p)")

    st.divider()

    st.subheader("Salt Rejection")
    st.latex(r"R = \left(1 - \frac{C_p}{C_f}\right) \times 100")

    st.divider()

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

    # -------------------------------
    # PROCESS DASHBOARD
    # -------------------------------
    st.subheader("📊 Process Simulation Dashboard")
    fig = generate_simulation_dashboard()
    st.pyplot(fig)

    # -------------------------------
    # KEY OBSERVATIONS (NEW)
    # -------------------------------
    st.divider()
    st.header("📌 Key Simulation Observations")

    st.markdown("""
- **Osmotic Pressure vs. Concentration:**  
  Osmotic pressure increases linearly with salt concentration as described by the van’t Hoff equation.  
  Seawater at 0.6 mol/L gives π ≈ 29.75 bar, confirming that RO systems must operate above 30 bar.

- **Water Flux vs. Applied Pressure:**  
  Below the osmotic pressure threshold (~30 bar), no water flux occurs.  
  Above this threshold, flux increases linearly with applied pressure, following the solution-diffusion model.

- **Salt Rejection vs. Pressure:**  
  As applied pressure increases, water flux increases while salt flux remains approximately constant (concentration-driven),  
  resulting in improved salt rejection reaching ~99.6% at higher pressures.

- **Permeate Flow vs. Membrane Area:**  
  Total water production scales linearly with membrane area.  
  A 1000 m² system at 60 bar produces significant permeate flow, demonstrating scalability.

- **Temperature Effect:**  
  Osmotic pressure increases proportionally with absolute temperature.  
  Higher temperatures increase osmotic pressure, requiring higher operating pressures.
""")

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

### 🔧 Model Enhancements
- Multi-stage RO systems  
- Energy consumption modeling  
- Fouling and scaling effects  

### 📊 Advanced Analysis
- Optimization of operating conditions  
- Multi-variable sensitivity analysis  

### 🤖 AI Integration
- Machine learning for performance prediction  
- Smart recommendation systems  

### 🌐 Product Development
- Full-stack deployment  
- User data storage and simulations  

### 🧪 Research Extensions
- Extend to other membrane processes  
- Industrial-scale simulation  

---

👉 This project can evolve into a **digital twin of membrane systems** bridging theory and real-world applications.
""")