import numpy as np

R_GAS = 8.314

def osmotic_pressure_bar(C_mol_L, T_C, i=2):
    C_mol_m3 = C_mol_L * 1000
    T_K = T_C + 273.15
    return i * C_mol_m3 * R_GAS * T_K / 1e5

def water_flux_LMH(delta_P_bar, C_mol_L, T_C, A, i=2):
    pi = osmotic_pressure_bar(C_mol_L, T_C, i)
    net = (delta_P_bar - pi) * 1e5
    Jw = A * max(net, 0)
    return Jw * 3600 * 1000

def salt_rejection_pct(delta_P_bar, C_mol_L, T_C, A, B, i=2):
    pi = osmotic_pressure_bar(C_mol_L, T_C, i)
    net = (delta_P_bar - pi) * 1e5
    Jw = A * max(net, 0)
    Cf = C_mol_L * 1000
    Cs = Cf * 1.15
    if Jw == 0:
        return 0
    Cp = B * Cs / (Jw + B)
    return (1 - Cp / Cf) * 100

def permeate_flow_m3h(delta_P_bar, C_mol_L, T_C, A, B, Am, i=2):
    Jw_LMH = water_flux_LMH(delta_P_bar, C_mol_L, T_C, A, i)
    return (Jw_LMH / 1000) * Am