import streamlit as st
from model import *

st.set_page_config(page_title="RO Simulator", layout="wide")

st.title("💧 Reverse Osmosis Process Simulator")

# Sidebar inputs
st.sidebar.header("Input Parameters")

delta_P = st.sidebar.slider("Pressure ΔP (bar)", 10.0, 100.0, 60.0)
C = st.sidebar.slider("Concentration (mol/L)", 0.1, 1.5, 0.6)
T = st.sidebar.slider("Temperature (°C)", 5.0, 60.0, 25.0)
A = st.sidebar.number_input("Water Permeability A", value=3.5e-12, format="%.2e")
B = st.sidebar.number_input("Salt Permeability B", value=3.5e-8, format="%.2e")
Am = st.sidebar.slider("Membrane Area (m²)", 100, 5000, 1000)

# Compute outputs
pi = osmotic_pressure_bar(C, T)
Jw = water_flux_LMH(delta_P, C, T, A)
R  = salt_rejection_pct(delta_P, C, T, A, B)
Qp = permeate_flow_m3h(delta_P, C, T, A, B, Am)

# Show results
st.subheader("📊 Results")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Osmotic Pressure π (bar)", f"{pi:.2f}")
col2.metric("Water Flux Jw (LMH)", f"{Jw:.2f}")
col3.metric("Salt Rejection (%)", f"{R:.2f}")
col4.metric("Flow Rate Qp (m³/h)", f"{Qp:.2f}")

# Warning condition
if delta_P < pi:
    st.warning("⚠️ Applied pressure is less than osmotic pressure — no filtration occurs!")


import numpy as np
import matplotlib.pyplot as plt

st.subheader("📈 Pressure vs Water Flux")

pressure_range = np.linspace(20, 80, 50)
flux_values = [water_flux_LMH(p, C, T, A) for p in pressure_range]

fig, ax = plt.subplots()
ax.plot(pressure_range, flux_values)
ax.set_xlabel("Pressure (bar)")
ax.set_ylabel("Water Flux (LMH)")
ax.set_title("Effect of Pressure on Flux")

st.pyplot(fig)