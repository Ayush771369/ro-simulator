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
    import matplotlib.pyplot as plt

    variation = 0.2
    params = ["delta_P", "C", "T", "A", "B"]

    def compute(b):
        return water_flux_LMH(
            b["delta_P"],
            b["C"],
            b["T"],
            b["A"]
        )

    base_val = compute(baseline)

    fig, ax = plt.subplots(figsize=(8, 6))

    for param in params:
        low = baseline.copy()
        high = baseline.copy()

        low[param] *= (1 - variation)
        high[param] *= (1 + variation)

        low_val = compute(low)
        high_val = compute(high)

        ax.barh(param, high_val - low_val)

    ax.set_title("Tornado Chart (Impact on Water Flux)")
    return fig
# ---------- HEATMAP ----------
def generate_heatmap(baseline):
    import seaborn as sns

    data = np.random.rand(5, 4)  # placeholder (can replace with real SI)

    fig, ax = plt.subplots()
    sns.heatmap(data, annot=True, ax=ax)

    return fig

def generate_simulation_dashboard():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec

    R_GAS = 8.314
    i = 2
    A = 3.5e-12
    B = 3.5e-8

    def osmotic_pressure(C, T):
        return i * C * 1000 * R_GAS * T

    def water_flux(P, pi):
        return A * np.maximum(P - pi, 0)

    def rejection(Jw, Cs):
        return 100 * (1 - (B * Cs / (Jw + B)) / Cs)

    def flow(Jw, Am):
        return Jw * Am

    # Base values
    T = 298.15
    C = 0.6
    pi = osmotic_pressure(C, T)

    # Ranges
    C_range = np.linspace(0.01, 1.2, 200)
    pi_vals = osmotic_pressure(C_range, T) / 1e5

    P_range = np.linspace(0, 80, 200)
    P_Pa = P_range * 1e5
    Jw = water_flux(P_Pa, pi) * 3600 * 1000

    # Rejection
    P2 = np.linspace(30, 80, 200)
    Jw2 = water_flux(P2 * 1e5, pi)
    Cs = C * 1000 * 1.15
    Cp = B * Cs / (Jw2 + B)
    R = 100 * (1 - Cp / (C * 1000))

    # Flow
    Am_range = np.linspace(10, 5000, 200)
    Jw60 = water_flux(60e5, pi)
    Qp = flow(Jw60, Am_range) * 3600

    # Temp
    T_range = np.linspace(5, 45, 100)
    pi_T = osmotic_pressure(C, T_range + 273.15) / 1e5

    # Plot
    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(2, 3)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(C_range, pi_vals)
    ax1.set_title("π vs C")

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(P_range, Jw)
    ax2.set_title("Jw vs Pressure")

    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(P2, R)
    ax3.set_title("Rejection vs Pressure")

    ax4 = fig.add_subplot(gs[1, 0])
    ax4.plot(Am_range, Qp)
    ax4.set_title("Flow vs Area")

    ax5 = fig.add_subplot(gs[1, 1])
    ax5.plot(T_range, pi_T)
    ax5.set_title("π vs Temperature")

    return fig