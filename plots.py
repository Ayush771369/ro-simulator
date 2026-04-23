import numpy as np
import matplotlib.pyplot as plt
from model import *

# ---------- OAT PLOT ----------
def generate_oat_plots(baseline):
    import numpy as np
    import matplotlib.pyplot as plt

    N = 100

    params = {
        "Pressure ΔP (bar)": np.linspace(35, 80, N),
        "Concentration C (mol/L)": np.linspace(0.1, 1.2, N),
        "Temperature T (°C)": np.linspace(5, 45, N),
        "Permeability A": np.linspace(1e-12, 7e-12, N),
        "Salt Perm. B": np.linspace(0.5e-8, 8e-8, N),
    }

    outputs = [
        ("Water Flux Jw", "LMH"),
        ("Salt Rejection R", "%"),
        ("Permeate Flow Qp", "m³/h"),
        ("Osmotic Pressure π", "bar")
    ]

    fig, axes = plt.subplots(5, 4, figsize=(18, 14))

    for i, (param_name, values) in enumerate(params.items()):
        for j, (out_name, unit) in enumerate(outputs):

            y = []

            for val in values:
                dP = val if "Pressure" in param_name else baseline["delta_P"]
                C  = val if "Concentration" in param_name else baseline["C"]
                T  = val if "Temperature" in param_name else baseline["T"]
                A  = val if "Permeability A" in param_name else baseline["A"]
                B  = val if "Salt Perm" in param_name else baseline["B"]

                pi = osmotic_pressure_bar(C, T)
                Jw = water_flux_LMH(dP, C, T, A)
                R  = salt_rejection_pct(dP, C, T, A, B)
                Qp = permeate_flow_m3h(dP, C, T, A, B, baseline["Am"])

                outputs_vals = [Jw, R, Qp, pi]
                y.append(outputs_vals[j])

            ax = axes[i, j]

            ax.plot(values, y, linewidth=1.8)
            ax.grid(True, alpha=0.3)

            # -------------------------------
            # LABELS (IMPORTANT PART)
            # -------------------------------
            if i == 0:
                ax.set_title(f"{out_name} ({unit})", fontsize=9)

            if j == 0:
                ax.set_ylabel(param_name, fontsize=8)

            if i == 4:
                ax.set_xlabel(param_name, fontsize=8)

            # Optional: cleaner ticks
            ax.tick_params(labelsize=7)

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
    import numpy as np
    import matplotlib.pyplot as plt

    VARIATION = 0.20

    # -------------------------------
    # Labels
    # -------------------------------
    param_labels = [
        "Applied Pressure ΔP",
        "Feed Concentration C",
        "Temperature T",
        "Water Perm. A",
        "Salt Perm. B",
    ]

    output_labels = [
        "Jw (L/m²·h)",
        "Salt Rejection (%)",
        "Permeate Flow (m³/h)",
        "Osmotic Pressure (bar)"
    ]

    # -------------------------------
    # Helper function
    # -------------------------------
    def compute_outputs(b):
        pi = osmotic_pressure_bar(b["C"], b["T"])
        Jw = water_flux_LMH(b["delta_P"], b["C"], b["T"], b["A"])
        R  = salt_rejection_pct(b["delta_P"], b["C"], b["T"], b["A"], b["B"])
        Qp = permeate_flow_m3h(b["delta_P"], b["C"], b["T"], b["A"], b["B"], b["Am"])
        return [Jw, R, Qp, pi]

    base_out = compute_outputs(baseline)

    param_keys = ["delta_P", "C", "T", "A", "B"]

    SI_matrix = np.zeros((len(param_keys), len(output_labels)))

    # -------------------------------
    # Sensitivity Index Calculation
    # -------------------------------
    for i, key in enumerate(param_keys):
        for j in range(len(output_labels)):

            low = baseline.copy()
            high = baseline.copy()

            low[key] *= (1 - VARIATION)
            high[key] *= (1 + VARIATION)

            low_out = compute_outputs(low)[j]
            high_out = compute_outputs(high)[j]

            base_val = base_out[j]

            lo_change = (low_out - base_val) / (base_val + 1e-12)
            hi_change = (high_out - base_val) / (base_val + 1e-12)

            SI = (abs(lo_change) + abs(hi_change)) / 2 / VARIATION
            SI_matrix[i, j] = SI

    # -------------------------------
    # PLOTTING
    # -------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))

    # Use light colormap for black text visibility
    im = ax.imshow(SI_matrix, cmap="YlOrRd", aspect="auto")

    # Axis labels
    ax.set_xticks(range(len(output_labels)))
    ax.set_xticklabels(output_labels, fontsize=10)

    ax.set_yticks(range(len(param_labels)))
    ax.set_yticklabels(param_labels, fontsize=10)

    # -------------------------------
    # BLACK TEXT ANNOTATIONS (FIXED)
    # -------------------------------
    for i in range(len(param_labels)):
        for j in range(len(output_labels)):
            val = SI_matrix[i, j]
            ax.text(
                j, i, f"{val:.2f}",
                ha="center",
                va="center",
                fontsize=10,
                color="black",
                fontweight="bold"
            )

    # Title
    ax.set_title(
        "Sensitivity Index Heatmap\nHigher value = output is MORE sensitive",
        fontsize=12
    )

    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Sensitivity Index (|ΔOutput%| / |ΔInput%|)")

    fig.tight_layout()

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