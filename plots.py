import numpy as np
import matplotlib.pyplot as plt
from model import *

# ---------- OAT PLOT ----------
def generate_oat_plots(baseline):
    N = 100

    params = {
        "Pressure": np.linspace(35, 80, N),
        "Concentration": np.linspace(0.1, 1.2, N),
        "Temperature": np.linspace(5, 45, N),
        "A": np.linspace(1e-12, 7e-12, N),
        "B": np.linspace(0.5e-8, 8e-8, N),
    }

    fig, axes = plt.subplots(5, 4, figsize=(16, 12))

    for i, (param, values) in enumerate(params.items()):
        for j in range(4):
            y = []

            for val in values:
                dP = val if param == "Pressure" else baseline["delta_P"]
                C  = val if param == "Concentration" else baseline["C"]
                T  = val if param == "Temperature" else baseline["T"]
                A  = val if param == "A" else baseline["A"]
                B  = val if param == "B" else baseline["B"]

                pi = osmotic_pressure_bar(C, T)
                Jw = water_flux_LMH(dP, C, T, A)
                R  = salt_rejection_pct(dP, C, T, A, B)
                Qp = permeate_flow_m3h(dP, C, T, A, B, baseline["Am"])

                outputs = [Jw, R, Qp, pi]
                y.append(outputs[j])

            axes[i, j].plot(values, y)

    fig.tight_layout()
    return fig


# ---------- TORNADO ----------
def generate_tornado(baseline):
    variation = 0.2
    params = ["delta_P", "C", "T", "A", "B"]

    base_vals = [
        water_flux_LMH(**baseline),
        salt_rejection_pct(**baseline),
        permeate_flow_m3h(**baseline),
        osmotic_pressure_bar(baseline["C"], baseline["T"]),
    ]

    fig, ax = plt.subplots(figsize=(8, 6))

    for i, param in enumerate(params):
        low = baseline.copy()
        high = baseline.copy()

        low[param] *= (1 - variation)
        high[param] *= (1 + variation)

        low_val = water_flux_LMH(**low)
        high_val = water_flux_LMH(**high)

        ax.barh(param, high_val - low_val)

    return fig


# ---------- HEATMAP ----------
def generate_heatmap(baseline):
    import seaborn as sns

    data = np.random.rand(5, 4)  # placeholder (can replace with real SI)

    fig, ax = plt.subplots()
    sns.heatmap(data, annot=True, ax=ax)

    return fig